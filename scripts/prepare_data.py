"""Run from any working directory; defaults are relative to project root."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.pump_data import prepare


def main():
    parser = argparse.ArgumentParser(description="Audit CSVs and create shared segment split manifests")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data/raw")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "outputs/preparation")
    parser.add_argument("--config", type=Path, default=ROOT / "configs/split.json")
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    audit = prepare(args.data_dir, args.output_dir, config)
    print(json.dumps(audit, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
