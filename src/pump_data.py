"""Dependency-free, explicit provenance and segment-level split preparation."""
from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import Counter
from datetime import datetime
from pathlib import Path

CHANNELS = ("AI0_Vibration", "AI1_Vibration", "AI2_Current")
REQUIRED = ("TimeStamp", *CHANNELS, "Equipment_state")


def read_rows(path: Path, expected_label: int):
    rows, seen = [], {}
    duplicates = 0
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not set(REQUIRED).issubset(reader.fieldnames or []):
            raise ValueError(f"{path.name}: required columns missing")
        for line, raw in enumerate(reader, start=2):
            try:
                timestamp = datetime.fromisoformat(raw["TimeStamp"].strip())
                sensors = tuple(float(raw[name]) for name in CHANNELS)
                label = float(raw["Equipment_state"])
                if label != expected_label or not all(map(math.isfinite, sensors)):
                    raise ValueError("unexpected label or nonfinite sensor")
            except (ValueError, TypeError, AttributeError) as exc:
                raise ValueError(f"{path.name}:{line}: invalid timestamp/sensor/label") from exc
            signature = (*sensors, int(label))
            if timestamp in seen:
                if seen[timestamp] != signature:
                    raise ValueError(f"{path.name}:{line}: conflicting duplicate timestamp")
                duplicates += 1
                continue
            seen[timestamp] = signature
            rows.append({"timestamp": timestamp, "sensors": sensors,
                         "label": int(label), "source_line": line})
    if not rows:
        raise ValueError(f"{path.name}: no valid records")
    rows.sort(key=lambda row: row["timestamp"])
    return rows, duplicates


def group_rows(rows, gap_seconds):
    if gap_seconds <= 0:
        raise ValueError("gap_seconds must be positive")
    groups = []
    for row in rows:
        if not groups or (row["timestamp"] - groups[-1][-1]["timestamp"]).total_seconds() > gap_seconds:
            groups.append([])
        groups[-1].append(row)
    return groups


def split_names(count, train_fraction, validation_fraction):
    if not (0 < train_fraction < 1 and 0 < validation_fraction < 1
            and train_fraction + validation_fraction < 1):
        raise ValueError("fractions must be positive and sum to less than one")
    n_train = int(count * train_fraction)
    n_validation = int(count * validation_fraction)
    if min(n_train, n_validation, count - n_train - n_validation) < 1:
        raise ValueError("too few segments for the requested split")
    return (["train"] * n_train + ["validation"] * n_validation
            + ["test"] * (count - n_train - n_validation))


def prepare(data_dir: Path, output_dir: Path, config: dict):
    if config["strategy"] != "chronological_within_each_source":
        raise ValueError("unsupported split strategy")
    audit = {"config": config, "files": {}, "limitations": [
        "Labels and recording dates are confounded; this is not date holdout.",
        "Acquisition segments are not verified press cycles or independent faults.",
        "Previously inspected recordings do not constitute a new blind test.",
        "Timestamp, source, label and segment identifiers are not model features."
    ]}
    segments, memberships = [], []
    for source, filename, label in (("normal", "press_data_normal.csv", 0),
                                    ("anomaly", "outlier_data.csv", 1)):
        path = data_dir / filename
        rows, duplicates = read_rows(path, label)
        groups = group_rows(rows, config["gap_seconds"])
        splits = split_names(len(groups), config["train_fraction"], config["validation_fraction"])
        row_counts, segment_counts = Counter(), Counter()
        for i, (group, split) in enumerate(zip(groups, splits)):
            segment_id = f"{source}_{i:04d}"
            segments.append({"segment_id": segment_id, "source": source, "label": label,
                             "start": group[0]["timestamp"].isoformat(),
                             "end": group[-1]["timestamp"].isoformat(),
                             "rows": len(group), "split": split})
            segment_counts[split] += 1
            row_counts[split] += len(group)
            for row in group:
                memberships.append({"source": source, "source_line": row["source_line"],
                                    "timestamp": row["timestamp"].isoformat(),
                                    "segment_id": segment_id, "label": label, "split": split})
        audit["files"][filename] = {
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "raw_rows": len(rows) + duplicates, "clean_rows": len(rows),
            "exact_duplicates_removed": duplicates, "segments": len(groups),
            "dates": sorted({r["timestamp"].date().isoformat() for r in rows}),
            "rows_by_split": dict(row_counts), "segments_by_split": dict(segment_counts),
        }
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, records in (("segments.csv", segments), ("rows.csv", memberships)):
        with (output_dir / name).open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(records[0]))
            writer.writeheader()
            writer.writerows(records)
    (output_dir / "audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    return audit
