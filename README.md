# Python Data Analytics Software for Students

This repository contains an open-source, Python-based data analytics software designed for students to learn probability and statistics (English language only).

## Features

- Descriptive statistics (mean, median, variance, std dev, min, max)
- Hypothesis testing (t-test, z-test, chi-square - core logic)
- Probability distributions (normal, binomial - core logic)
- Linear regression and Pearson correlation (core logic)
- CSV, XLSX, ODS data import (CSV fully integrated in UI)
- Interactive 2D visualizations (Histogram integrated)
- PDF and PNG report generation (PNG for plots integrated)


## Documentation

- User manual is available in `docs/user_manual.md`.
- The developer guide is in `docs/developer_guide.md`.


# User Manual

## Introduction
Welcome to the Data Analytics Software! This guide (English only) will help you understand how to use the application for statistical analysis.

## System Requirements
- Windows, macOS, or Linux
- Python 3.8+
- Dependencies listed in `requirements.txt`

## Installation
1.  Generate the software repository.
2.  Navigate to the project root directory.
3.  (Recommended) Create and activate a Python virtual environment.
4.  Install required libraries: `pip install -r requirements.txt`

## Getting Started
1.  Launch from the project root: `python src/main.py` or `python -m src.main`
2.  The main window will appear.

## Interface Overview
- **Menu Bar**: File (Open, Save Report, Exit), Analysis, Help (View Help, About).
- **Toolbar**: Quick access (Open).
- **Controls Panel**: Select column for analysis, run Descriptive Stats, plot Histogram.
- **Data Display Area**: Table view of loaded data.
- **Results Area**: Text box for statistical results.
- **Plot Area**: Displays generated plots.
- **Status Bar**: Shows status messages.

## Loading Data
1.  `File > Open Data File...` or Open icon.
2.  Select a CSV, XLSX, or ODS file.

## Performing Analysis
### Descriptive Statistics
1.  Load data.
2.  Select a numeric column in "Controls Panel".
3.  Click "Run Descriptive Stats". Results appear in "Results Area".

## Visualizations
### Histogram
1.  Load data.
2.  Select a numeric column in "Controls Panel".
3.  Click "Plot Histogram". Plot appears in "Plot Area".

## Generating Reports
### Save Plot as PNG
1.  After plot generation, `File > Save Plot as PNG...`.

### Save Report as PDF
1.  After analysis/plot, `File > Save Report as PDF...`.

## Help
- `Help > View Help`: Opens this user manual.
- `Help > About`: Software information.

## Troubleshooting
- **File not loading**: Check file validity. Error messages provide details.
- **Analysis/Plot not working**: Ensure selected column is numeric.
- **ModuleNotFoundError**: Ensure dependencies are installed and running from project root.
