import csv
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from src.pump_data import CHANNELS, group_rows, read_rows, split_names


class DataTests(unittest.TestCase):
    def test_gaps_do_not_join_or_drop_rows(self):
        t = datetime(2022, 7, 12)
        rows = [{"timestamp": t + timedelta(seconds=s)} for s in (0, .1, .2, 4, 4.1, 8)]
        groups = group_rows(rows, .15)
        self.assertEqual([len(g) for g in groups], [3, 2, 1])
        self.assertEqual([r for g in groups for r in g], rows)

    def test_split_is_chronological_and_complete(self):
        names = split_names(21, .7, .15)
        self.assertEqual(names, ["train"] * 14 + ["validation"] * 3 + ["test"] * 4)

    def test_too_few_segments_fail(self):
        with self.assertRaises(ValueError):
            split_names(2, .7, .15)

    def write_csv(self, path, records):
        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["", "TimeStamp", *CHANNELS, "Equipment_state"])
            writer.writerows(records)

    def test_duplicate_ignores_export_index(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "data.csv"
            self.write_csv(path, [[0, "2022-07-12 00:00:00", 1, 2, 3, 0],
                                  [1, "2022-07-12 00:00:00", 1, 2, 3, 0]])
            rows, removed = read_rows(path, 0)
            self.assertEqual((len(rows), removed), (1, 1))

    def test_conflicting_timestamp_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "data.csv"
            self.write_csv(path, [[0, "2022-07-12 00:00:00", 1, 2, 3, 0],
                                  [1, "2022-07-12 00:00:00", 9, 2, 3, 0]])
            with self.assertRaisesRegex(ValueError, "conflicting"):
                read_rows(path, 0)


if __name__ == "__main__":
    unittest.main()
