---
layout: default
title: The Lab
tagline: Get a notebook on the supercomputer and follow along
---

[Home](./)  |  **Lab**  |  [Homework](homework.html)

This is what we do together in class. Three steps to get set up, then we analyze taxi data on a supercomputer.

---

## Step 1: Get a notebook running on Vista

1. Go to [morehouse.tapis.io](https://morehouse.tapis.io) and sign in with your TACC account.
2. Submit the Jupyter job. Wait until it reads RUNNING.
3. Open `tapisjob.out`, find the `JUPYTER_URL` line, and paste that URL into your browser.

JupyterLab opens, running on a compute node at TACC. That is the supercomputer. No SSH, no scheduler, no install.

## Step 2: Pull the lab into your folder

In JupyterLab, click **File → New → Notebook**, and choose the Python 3 kernel.

Paste this into the first cell and run it (Shift+Enter):

```python
!git clone https://github.com/ashleyscruse/taxi-python-assignment.git ~/taxi-lab
```

Then look in the file browser on the left. The folder is there.

That is the whole distribution step. The lab now lives in your own folder on Vista, and it is yours to edit and break.

## Step 3: Open the lab notebook

In the file browser on the left, open `taxi-lab` → `notebooks` → `lab.ipynb`.

Run the cells in order and follow along. We will stop and talk between sections.

---

## What we cover in the lab

| Section | What you learn |
|---|---|
| 1 | Proving you are actually on a supercomputer, and what it has |
| 2 | Finding data that is already there, instead of downloading it |
| 3 | Reading one month with pandas, and why you always start small |
| 4 | Counting, grouping, averaging, and merging a lookup table |
| 5 | Loading all 38 million rows at once, which your laptop cannot do |
| 6 | What to take into the homework |

## Then the homework

The [homework](homework.html) asks a new question of the same data, and you answer it on your own.

---

## For instructors

This lab is a GitHub repository, and students pull it with the one line in step 2.

If your cluster's compute nodes cannot reach GitHub, stage a copy in a world readable
folder on Vista and have students run this instead:

```python
import shutil, os
shutil.copytree("/work/10539/ashleyscruse/vista/taxi-python-assignment",
                os.path.expanduser("~/taxi-lab"))
```

To run it for your own class:

1. Fork or clone this repo.
2. Stage the CSVs once with `scripts/export_csv.py`, and put a copy of the repo somewhere world readable on Vista.
3. Change `SHARED` in the step 2 cell to your path.

Everything else is unchanged. No student account needs anything installed.
