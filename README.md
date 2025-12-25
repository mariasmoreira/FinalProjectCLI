# FinalProjectCLI

This repository is a command line interface for data analysis

It contains:

- `expcli.py` – the main script which contains the command line interface for analysis using expstats.py. It allows users to quickly list participants, generate summaries, compare groups, and produce reports directly from the terminal.
- `expstats.py` – script with all the analysis functions including list-participants, summary, compare-groups and report commands.
- Pasta `examples/` – 4 CSV files for testing, in the correct format.

Available commands include:

- `list-participants` - Lists all participant IDs found in a CSV file or folder of CSVs

- `summary`- Prints summary statistics for a single CSV file

- `compare-groups` - Compares two groups of participants (two folders or sets of CSV files)

- `report` - Generates a full report for one or more CSVs, saving it to a file

# Installation

```python
git clone https://github.com/mariasmoreira/FinalProjectCLI
cd FinalProjectCLI
```

(Optional) Create a virtual environment

```python
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
``` 

Usage example:
```python

python expcli.py generate_report ../FinalProjectCLI/examples/condA_P001.csv report.txt 
``` 