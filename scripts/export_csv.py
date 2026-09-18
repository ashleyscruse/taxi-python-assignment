#!/usr/bin/env python3
"""Export nyc_taxi.db into the monthly CSVs the Python version of the assignment reads.

Run once, on a Vista login node, from the folder that holds data/nyc_taxi.db:

    python3 scripts/export_csv.py

Produces data_csv/trips_2023-MM.csv (12 files, ~250 MB each) and data_csv/zones.csv.
Chunked, so it never holds 38 million rows in memory. Takes 15-25 minutes.

Twelve files rather than one is deliberate: students start with a single month on
muscle memory from class, then discover that the whole year is the part that needs
the node.
"""
import sqlite3
import pathlib
import sys

import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent.parent
DB = HERE / "data" / "nyc_taxi.db"
OUT = HERE / "data_csv"

if not DB.is_file():
    sys.exit(f"No database at {DB}. Run scripts/setup_data.sh first.")

OUT.mkdir(exist_ok=True)
conn = sqlite3.connect(DB)

# zones is tiny; straight out it goes.
pd.read_sql("SELECT * FROM zones", conn).to_csv(OUT / "zones.csv", index=False)
print("wrote zones.csv")

for month in range(1, 13):
    tag = f"2023-{month:02d}"
    dest = OUT / f"trips_{tag}.csv"
    if dest.exists():
        print(f"{dest.name} already there, skipping")
        continue

    query = "SELECT * FROM trips WHERE pickup_time >= ? AND pickup_time < ?"
    start = f"{tag}-01"
    end = f"2024-01-01" if month == 12 else f"2023-{month + 1:02d}-01"

    rows = 0
    header = True
    for chunk in pd.read_sql(query, conn, params=(start, end), chunksize=500_000):
        chunk.to_csv(dest, mode="w" if header else "a", header=header, index=False)
        header = False
        rows += len(chunk)
    print(f"wrote {dest.name}: {rows:,} rows")

conn.close()
print(f"\nDone. CSVs in {OUT}")
