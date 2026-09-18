# Taxi Data in Python

A teaching module and homework assignment: analyze 38 million New York City taxi trips
with pandas, on a supercomputer, from a web browser.

**Course site: [ashleyscruse.github.io/taxi-python-assignment](https://ashleyscruse.github.io/taxi-python-assignment/)**

Students never open a terminal. They launch JupyterLab through a web portal, pull this
repository into their own folder with one line, and work through the notebooks.

## What is here

| | |
|---|---|
| `docs/` | The course site: the in-class module, and the homework |
| `notebooks/module.ipynb` | The in-class follow-along |
| `notebooks/taxi_starter.ipynb` | The homework starter, setup pre-filled |
| `scripts/export_csv.py` | Builds the monthly CSVs the notebooks read |

## The data

2023 NYC yellow cab trips, published by the NYC Taxi & Limousine Commission: about 38
million rows across twelve monthly CSV files, plus a zone lookup table. The notebooks
read a copy staged on a shared filesystem, so nobody downloads anything.

## The same assignment in SQL

There is a SQL version of this question, using the same data:
[SQL on HPC](https://github.com/ashleyscruse/gosha-sql-assignment). The two are meant to
be taught side by side. The reasoning is the point; the language is not.

## For instructors

See the "For instructors" section of the [module page](https://ashleyscruse.github.io/taxi-python-assignment/module.html)
for how to stage the data and point the notebooks at your own filesystem.
