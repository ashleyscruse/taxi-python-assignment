---
layout: default
title: Airport Pricing
tagline: Your homework assignment
---

[Home](./)  |  [Lab](lab.html)  |  **Homework**

You're a data analyst at the NYC Taxi & Limousine Commission. The commission has a follow-up question:

**Should airport fares be priced differently from non-airport fares?**

Same 2023 yellow cab trips. Same question as the SQL version. This time the data is CSV files and your tool is pandas, and you will not open a terminal once.

Airport zones: `pickup_zone_id` in `[1, 132, 138]`, which are Newark, JFK, and LaGuardia.

---

## Step 1: Get a notebook on the supercomputer

1. Go to [morehouse.tapis.io](https://morehouse.tapis.io) and sign in with your TACC account.
2. Submit the Jupyter job (the JSON is on the course page). Wait until it reads RUNNING.
3. Open `tapisjob.out`, copy the `JUPYTER_URL` line, and paste it into your browser.

You now have a Jupyter notebook running on a compute node at TACC. No SSH, no `idev`, no scheduler.

## Step 2: Point at the data

The CSVs are already on Vista, shared and read only. You do not copy them and you do not download them. Put this at the top of your notebook:

```python
import pandas as pd
import glob

DATA = "/work/10539/ashleyscruse/vista/taxi-python-assignment/data_csv"

print(sorted(glob.glob(f"{DATA}/trips_2023-*.csv")))
```

Twelve monthly files, about 250 MB each, plus `zones.csv`.

## Step 3: Start with one month

Get your analysis working on January before you run the year. This is how real analysts work, and it will save you a lot of waiting.

```python
jan = pd.read_csv(f"{DATA}/trips_2023-01.csv")
print(f"{len(jan):,} trips")
jan.head()
```

Columns: `pickup_time`, `dropoff_time`, `passengers`, `distance_miles`, `pickup_zone_id`, `dropoff_zone_id`, `fare`, `tip`, `total`, `payment_type`.

## Step 4: Load the whole year

When your analysis works on January, run it on all of 2023:

```python
AIRPORTS = [1, 132, 138]

df = pd.concat(
    (pd.read_csv(f) for f in sorted(glob.glob(f"{DATA}/trips_2023-*.csv"))),
    ignore_index=True,
)
df["is_airport"] = df["pickup_zone_id"].isin(AIRPORTS)
print(f"{len(df):,} trips loaded")
```

That is 38 million rows held in memory at once. Your laptop cannot do this. The node you are on can, and it takes a few minutes. Notice how long it takes, because one of your reflection questions is about exactly this.

---

## Sub-questions to guide your analysis

Use these to break the big question into code you can write. Each one builds part of the case.

### 1. How big a slice of the business are airport trips?

Count them, and get the percentage of all trips. Hint: `df["is_airport"].value_counts()` and `value_counts(normalize=True)`.

### 2. How are airport trips different in fare, distance, and tip?

Compare averages between the two groups:

```python
df.groupby("is_airport")[["fare", "distance_miles", "tip"]].mean().round(2)
```

### 3. Are airport trips concentrated at certain hours of the day?

Pull the hour out of the timestamp, then count airport pickups by hour:

```python
df["hour"] = pd.to_datetime(df["pickup_time"]).dt.hour
df[df["is_airport"]].groupby("hour").size()
```

`pd.to_datetime` on 38 million rows is slow. If it crawls, add `format="%Y-%m-%d %H:%M:%S"` and it will speed up considerably. Understanding why is worth a sentence in your reflection.

### 4. Are airport riders more likely to pay by credit card than cash?

Compare the payment mix for each group. Payment codes: 1 is credit card, 2 is cash, 3 is no charge, 4 is dispute.

```python
df.groupby("is_airport")["payment_type"].value_counts(normalize=True).round(3)
```

### 5. Which airport is which? (the JOIN, in pandas)

`pickup_zone_id` is a number. `zones.csv` turns it into a neighborhood name. Merging two tables on a shared column is what a SQL `JOIN` does:

```python
zones = pd.read_csv(f"{DATA}/zones.csv")
named = df.merge(zones, left_on="pickup_zone_id", right_on="zone_id", how="left")
named[named["is_airport"]].groupby("zone_name")["fare"].agg(["count", "mean"]).round(2)
```

JFK and LaGuardia do not behave the same way. That matters for a pricing recommendation.

You're welcome to ask additional questions of the data if they help your case.

---

## Save your results

Each answer gets written to a CSV in your own folder on Vista:

```python
import os

OUT = os.path.expanduser("~/taxi-homework")
os.makedirs(OUT, exist_ok=True)

result_1 = df.groupby("is_airport")[["fare", "distance_miles", "tip"]].mean().round(2)
result_1.to_csv(f"{OUT}/query_1.csv")
```

Repeat for each sub-question: `query_2.csv`, `query_3.csv`, and so on. A `to_csv` on a result of a `groupby` keeps the group labels, so your file will make sense to someone who did not write it.

## Get your results onto your laptop

Go back to the Tapis tab, open **Files**, browse to `taxi-homework`, select your CSVs, and click download.

That is it. No `scp`, no second terminal window, no path you have to copy by hand.

---

## Submission

Submit a single ZIP or folder containing:

1. **Your notebook** (`.ipynb`), with the cells run so the output is visible
2. **The CSV files** of your results
3. **Your recommendation** (1 to 2 paragraphs). Should airport fares be priced differently? Cite specific numbers from your analysis.
4. **A short reflection** (about 150 words):
   - What finding surprised you?
   - What data did you wish you had?
   - When did the supercomputer actually matter for this assignment, and when did it not?

---

## What good work looks like

A strong submission:

- Takes a clear position (yes, no, or depends on X)
- Uses specific numbers from your analysis to support it
- Acknowledges what the data cannot tell you (driver welfare, demand elasticity, alternative transit, outer boroughs)
- Suggests what additional data would strengthen the case

There is no single correct answer. You are graded on the quality of your reasoning and your use of evidence, not on the direction of your recommendation.

---

## Reference: the same idea in both languages

You learned this in SQL. Here is the translation, so neither one feels like a separate skill.

| What you want | SQL | pandas |
|---|---|---|
| All the data | `SELECT * FROM trips` | `pd.read_csv(path)` |
| First few rows | `SELECT * FROM trips LIMIT 5` | `df.head()` |
| Count rows | `SELECT COUNT(*) FROM trips` | `len(df)` |
| Pick columns | `SELECT fare, tip FROM trips` | `df[["fare", "tip"]]` |
| Filter rows | `WHERE distance_miles > 10` | `df[df["distance_miles"] > 10]` |
| Filter on a list | `WHERE pickup_zone_id IN (1,132,138)` | `df["pickup_zone_id"].isin([1,132,138])` |
| Group and average | `GROUP BY x ... AVG(fare)` | `df.groupby("x")["fare"].mean()` |
| Sort | `ORDER BY fare DESC` | `df.sort_values("fare", ascending=False)` |
| Join two tables | `JOIN zones z ON t.pickup_zone_id = z.zone_id` | `df.merge(zones, left_on="pickup_zone_id", right_on="zone_id")` |
| Save a result | `.once out.csv` then the query | `result.to_csv("out.csv")` |

The database version and this version give the same answers. They are two ways of asking, and now you have both.
