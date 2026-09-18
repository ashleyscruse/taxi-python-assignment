#!/usr/bin/env python3
"""Regenerate taxi_starter.ipynb, the notebook students open for the Python homework."""
import json, pathlib

HERE = pathlib.Path(__file__).parent

def md(t): return {"cell_type": "markdown", "metadata": {}, "source": t.strip("\n").splitlines(keepends=True)}
def code(t): return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": t.strip("\n").splitlines(keepends=True)}

CELLS = [
md("""
# Airport pricing: should airport fares be different?

You are a data analyst at the NYC Taxi & Limousine Commission. Answer the question with
evidence from 38 million 2023 yellow cab trips.

The setup cells are done for you. Your work starts at section 3.
"""),

md("## 1. Where are we, and where is the data?"),
code("""
import os, glob, socket
import pandas as pd

DATA = "/work/10539/ashleyscruse/vista/taxi-python-assignment/data_csv"
AIRPORTS = [1, 132, 138]   # Newark, JFK, LaGuardia

OUT = os.path.expanduser("~/taxi-homework")
os.makedirs(OUT, exist_ok=True)

print("Running on:", socket.gethostname())
print("Results go to:", OUT)
print()
for f in sorted(glob.glob(f"{DATA}/trips_2023-*.csv")):
    print(os.path.basename(f), f"{os.path.getsize(f)/1e6:.0f} MB")
"""),

md("""
## 2. Start with one month

Get your analysis working on January first. Running the whole year on code that has a
typo in it is how you lose an afternoon.
"""),
code("""
jan = pd.read_csv(f"{DATA}/trips_2023-01.csv")
jan["is_airport"] = jan["pickup_zone_id"].isin(AIRPORTS)

print(f"{len(jan):,} trips in January")
jan.head()
"""),

md("""
## 3. Your analysis

Work out your answers on `jan` here. The homework page lists five sub-questions to guide
you. Add as many cells as you need.
"""),
code("""
# Sub-question 1: how big a slice of the business are airport trips?

"""),
code("""
# Sub-question 2: how do fare, distance, and tip differ?

"""),

md("""
## 4. Run it on the whole year

Once your analysis is right, load all twelve months and run it again. This cell takes a
few minutes and holds 38 million rows in memory at once. Time it, because your reflection
asks when the supercomputer actually mattered.
"""),
code("""
import time

t = time.time()
df = pd.concat(
    (pd.read_csv(f) for f in sorted(glob.glob(f"{DATA}/trips_2023-*.csv"))),
    ignore_index=True,
)
df["is_airport"] = df["pickup_zone_id"].isin(AIRPORTS)
print(f"{len(df):,} trips loaded in {time.time() - t:.0f} seconds")
print(f"Holding about {df.memory_usage(deep=True).sum()/1e9:.1f} GB in memory.")
"""),

md("## 5. Save each result as a CSV"),
code("""
result_1 = df.groupby("is_airport")[["fare", "distance_miles", "tip"]].mean().round(2)
result_1.to_csv(f"{OUT}/query_1.csv")
print(result_1)
print(f"\\nSaved to {OUT}/query_1.csv")
"""),

md("""
## 6. Your recommendation

Write it here, in this cell, in one or two paragraphs. Should airport fares be priced
differently from non-airport fares? Cite the specific numbers you found.

**Your recommendation:**

**Your reflection (about 150 words):** What surprised you? What data did you wish you
had? When did the supercomputer actually matter, and when did it not?
"""),
]

nb = {"cells": CELLS,
      "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                   "language_info": {"name": "python", "version": "3"}},
      "nbformat": 4, "nbformat_minor": 5}

(HERE / "taxi_starter.ipynb").write_text(json.dumps(nb, indent=1) + "\n")
print("wrote taxi_starter.ipynb")
