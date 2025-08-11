import csv
import json
from typing import Dict, Iterable, Optional, List

# Columns we treat as potential timestamp fields to be replaced
CANDIDATE_TS_COLS: List[str] = ["timestamp", "created_at", "time", "ts"]

def read_csv_as_dicts(path: str) -> Iterable[Dict]:
    """Stream rows from a CSV file as dicts."""
    with open(path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield dict(row)

def pick_timestamp_field(sample_row: Dict) -> Optional[str]:
    for key in sample_row.keys():
        if key.lower() in CANDIDATE_TS_COLS:
            return key
    return None

def serialize_record(record: Dict) -> bytes:
    """Serialize to JSON bytes for Kafka."""
    return json.dumps(record, ensure_ascii=False).encode("utf-8")
