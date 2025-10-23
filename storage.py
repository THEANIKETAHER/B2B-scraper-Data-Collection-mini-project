import json
import csv
from pathlib import Path

def jsonl_to_csv(jsonl_path, csv_path):
    Path(csv_path).parent.mkdir(parents=True, exist_ok=True)
    rows = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            rows.append(json.loads(line))
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with open(csv_path, "w", newline="", encoding="utf-8") as fout:
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    print(f"✅ CSV saved at: {csv_path}")

