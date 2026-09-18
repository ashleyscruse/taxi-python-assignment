#!/usr/bin/env python3
"""Regenerate module.ipynb, the in-class follow-along notebook."""
import json, pathlib
HERE = pathlib.Path(__file__).parent

def md(t): return {"cell_type": "markdown", "metadata": {}, "source": t.strip("\n").splitlines(keepends=True)}
def code(t): return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": t.strip("\n").splitlines(keepends=True)}

CELLS = [
md("""
# Taxi data on a supercomputer

Every yellow cab trip in New York City in 2023. Thirty-eight million of them.

We are going to ask the data some questions, in pandas, on a machine at the Texas
Advanced Computing Center. Run the cells in order. Stop when something is interesting.
"""),

md("""
## 1. Where are we?

Nobody opened a terminal, so it is fair to ask what we are actually running on.
"""),
code("""
import os, glob, socket, time
import pandas as pd

print("Machine:", socket.gethostname())
print("Cores available to us:", os.cpu_count())
print("Our folder:", os.getcwd())
"""),

md("""
## 2. The data is already here

You did not download it, and you are not going to. It is staged on Vista, read only,
and every one of us is reading the same copy.
"""),
code("""
DATA = "/work/10539/ashleyscruse/vista/taxi-python-assignment/data_csv"
AIRPORTS = [1, 132, 138]   # Newark, JFK, LaGuardia

files = sorted(glob.glob(f"{DATA}/trips_2023-*.csv"))
for f in files:
    print(os.path.basename(f), f"{os.path.getsize(f)/1e6:.0f} MB")
print(f"\\n{len(files)} months, {sum(os.path.getsize(f) for f in files)/1e9:.1f} GB total")
"""),

md("""
## 3. Start with one month

Always. You test your thinking on something small and fast, then you scale it up. This is
true whether you have a laptop or a supercomputer.
"""),
code("""
jan = pd.read_csv(files[0])
jan["is_airport"] = jan["pickup_zone_id"].isin(AIRPORTS)

print(f"{len(jan):,} trips in January")
jan.head()
"""),

md("""
## 4. Ask it some questions

Four questions, four lines of pandas. If you know SQL, you already know all of these;
they just have different names.
"""),
code("""
# How many trips start at an airport?
jan["is_airport"].value_counts(normalize=True).round(3)
"""),
code("""
# Do airport trips look different?
jan.groupby("is_airport")[["fare", "distance_miles", "tip"]].mean().round(2)
"""),
code("""
# When do people fly? Pull the hour out of the timestamp.
jan["hour"] = pd.to_datetime(jan["pickup_time"], format="%Y-%m-%d %H:%M:%S").dt.hour
jan[jan["is_airport"]].groupby("hour").size()
"""),
code("""
# zone_id is a number. zones.csv turns it into a name. This is a SQL JOIN.
zones = pd.read_csv(f"{DATA}/zones.csv")
named = jan.merge(zones, left_on="pickup_zone_id", right_on="zone_id", how="left")

named[named["is_airport"]].groupby("zone_name")["fare"].agg(["count", "mean"]).round(2)
"""),

md("""
**Stop and look at that last one.** JFK and LaGuardia do not behave the same way. Hold on
to that; it is the whole homework.
"""),

md("""
## 5. Now the whole year

One month was 3 million rows and took a couple of seconds. Here is all twelve.

This is the cell your laptop cannot run. Watch the clock and watch the memory number.
"""),
code("""
t = time.time()
df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)
df["is_airport"] = df["pickup_zone_id"].isin(AIRPORTS)

print(f"{len(df):,} trips loaded in {time.time() - t:.0f} seconds")
print(f"Holding {df.memory_usage(deep=True).sum()/1e9:.1f} GB in memory right now.")
"""),
code("""
# The same question as before, now against the entire year.
df.groupby("is_airport")[["fare", "distance_miles", "tip"]].mean().round(2)
"""),

md("""
### What just happened

You held every taxi trip in New York City for a year in memory at once and asked it a
question. A good laptop has 16 GB of memory and would have given up partway through the
load.

That is the only thing a supercomputer really gives you here: the problem stopped being
too big. You did not learn a scheduler, a shell, or a new language to get it.
"""),

md("""
## 6. Your turn

The commission has a follow-up question, and it is your homework:

> **Should airport fares be priced differently from non-airport fares?**

You have seen enough to start. The homework page lists the sub-questions, what to submit,
and how it is graded. Open `taxi_starter.ipynb` in this same folder when you are ready.
"""),
]

nb = {"cells": CELLS,
      "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                   "language_info": {"name": "python", "version": "3"}},
      "nbformat": 4, "nbformat_minor": 5}
(HERE / "module.ipynb").write_text(json.dumps(nb, indent=1) + "\n")
print("wrote module.ipynb")
