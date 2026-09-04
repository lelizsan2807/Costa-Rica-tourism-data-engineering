# Costa Rica Tourism Data Engineering

A reproducible **ETL pipeline for transforming Costa Rican tourism and demographic data from a semi-structured Excel workbook into clean, validated, analytics-ready datasets**.

The project demonstrates a complete data engineering workflow:

**Extract → Transform → Validate → Load**

The pipeline processes quarterly data from **Q3 2010 through Q1 2026**, creates normalized fact tables, exports them as CSV files, and loads them into a SQLite database for downstream analysis.

---

## 📌 Project Overview

The source dataset is an Excel workbook containing tourism-related socioeconomic and employment information organized in a semi-structured format.

Unlike a conventional tabular dataset, the workbook contains:

* Multi-level year and quarter headers
* Category labels distributed across rows
* Multiple demographic and socioeconomic sections
* Observations represented across columns
* Spanish-language categories

The purpose of this project is to convert that structure into a consistent relational data model that can be used for analytics, reporting, and further data science work.

---

## 🏗️ Data Pipeline

```text
                     ┌─────────────────────┐
                     │   turismo.xlsx      │
                     │    Raw Excel Data   │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │      EXTRACT        │
                     │                     │
                     │ • Load Excel        │
                     │ • Extract periods   │
                     │ • Extract tables    │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │     TRANSFORM       │
                     │                     │
                     │ • Clean text       │
                     │ • Convert values   │
                     │ • Normalize data   │
                     │ • Create period ID │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │      VALIDATE       │
                     │                     │
                     │ • Period coverage  │
                     │ • Required fields  │
                     │ • Duplicates       │
                     │ • Negative values  │
                     │ • Business rules   │
                     └──────────┬──────────┘
                                │
                                ▼
              ┌────────────────┴────────────────┐
              │                                 │
              ▼                                 ▼
     ┌─────────────────┐              ┌─────────────────┐
     │   CSV OUTPUTS   │              │  SQLite Database│
     │                 │              │                 │
     │ Fact tables     │              │ dim_period      │
     │                 │              │ fact_* tables   │
     └─────────────────┘              └─────────────────┘
```

---

## 🎯 Objectives

This project was designed to:

1. Build a reproducible ETL pipeline using Python.
2. Process semi-structured Excel data programmatically.
3. Convert quarterly observations into a normalized data model.
4. Implement automated data-quality validation.
5. Create reusable period dimensions and fact tables.
6. Export clean datasets as CSV.
7. Store normalized data in SQLite.
8. Provide a reliable foundation for future tourism analytics.

---

## 📂 Repository Structure

```text
Costa-Rica-tourism-data-engineering/
│
├── data/
│   └── raw/
│       └── turismo.xlsx
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── extract.py
│   ├── transform.py
│   ├── validate.py
│   ├── load.py
│   └── pipeline.py
│
├── README.md
├── .gitignore
└── .gitattributes
```

The repository separates the raw input data from the Python source code, while generated processed data and logs are configured to live outside the raw-data directory.

---

## 🔄 ETL Components

### 1. Extract

`src/extract.py`

The extraction layer reads the `C2 Total` worksheet from the Excel workbook without assuming a conventional header row.

It is responsible for:

* Loading the Excel workbook with pandas
* Reading the semi-structured worksheet
* Identifying years and quarters
* Converting Roman-numeral quarters (`I`, `II`, `III`, `IV`) into quarter numbers
* Creating standardized periods such as `2010-Q3`
* Extracting observations according to the table definitions

The pipeline explicitly handles the workbook's multi-level header structure rather than treating the Excel file as a simple flat table.

---

### 2. Transform

`src/transform.py`

The transformation layer standardizes the extracted data.

Key transformations include:

* Removing unnecessary whitespace
* Standardizing `period`, `dimension`, and `category`
* Converting Excel `"-"` values into missing values
* Converting observations to numeric values
* Storing numeric observations as `float`
* Rejecting negative observations
* Creating a reusable period dimension

These transformations turn the original semi-structured observations into analytics-friendly records.

---

### 3. Validate

`src/validate.py`

Data validation is a core part of the pipeline rather than an afterthought.

The pipeline validates:

* Expected quarterly periods
* Required columns
* Missing key fields
* Duplicate observations
* Period coverage
* Negative values
* Demographic reconciliation

The expected period range is:

```text
2010-Q3 → 2026-Q1
```

The demographic validation also checks that, for each period:

```text
Total = Hombre + Mujer
```

This provides a business-level consistency check in addition to standard schema and data-quality validation.

---

### 4. Load

`src/load.py`

The loading layer produces two types of outputs:

#### CSV

Each fact table is exported as a separate CSV file under:

```text
data/processed/
```

#### SQLite

The normalized datasets are loaded into:

```text
data/processed/tourism.db
```

The SQLite database contains a reusable `dim_period` table and the project's fact tables. Fact tables retain the period information and associate each observation with a `period_id`.

---

## 🗃️ Data Model

The project uses a simple dimensional-model approach.

### Dimension

#### `dim_period`

Contains the time dimension used throughout the dataset.

Typical fields include:

| Column      | Description                      |
| ----------- | -------------------------------- |
| `period_id` | Unique period identifier         |
| `year`      | Year                             |
| `quarter`   | Quarter number                   |
| `period`    | Formatted period, e.g. `2024-Q1` |

### Fact Tables

#### `fact_demographics`

Contains demographic characteristics such as:

* Total population
* Sex

  * Hombre
  * Mujer
* Geographic zone

  * Urbana
  * Rural
* Age groups

#### `fact_employment_structure`

Contains employment characteristics such as:

* Employment position
* Occupation qualification
* Establishment size

#### `fact_work_conditions`

Contains indicators related to:

* Hours worked
* Subemployment
* Employment formality
* Work-related insurance

#### `fact_income`

Contains income-related indicators such as:

* Income level
* Average monthly income

The table definitions and categories are centrally maintained in `src/config.py`, making the extraction logic easier to maintain when the source workbook changes.

---

## 🛠️ Technology Stack

| Technology | Purpose                               |
| ---------- | ------------------------------------- |
| Python     | ETL implementation                    |
| Pandas     | Data extraction and transformation    |
| openpyxl   | Excel workbook support through pandas |
| SQLite     | Analytical/local relational storage   |
| Logging    | Pipeline monitoring and diagnostics   |

---

## 🚀 Getting Started

### Prerequisites

Install Python 3.9+ and create a virtual environment.

```bash
python -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

---

### Install dependencies

Install the required Python packages:

```bash
pip install pandas openpyxl
```

---

### Run the pipeline

From the repository root:

```bash
cd src
python pipeline.py
```

The pipeline executes the complete workflow:

1. Load the Excel workbook
2. Extract quarterly periods
3. Validate the period dimension
4. Extract the configured fact tables
5. Clean and standardize observations
6. Validate each fact table
7. Export CSV files
8. Run demographic business validation
9. Load the SQLite database
10. Verify the database

This execution order is defined directly in `src/pipeline.py`.

---

## 📊 Expected Outputs

After a successful run, the processed directory will contain files similar to:

```text
data/
└── processed/
    ├── fact_demographics.csv
    ├── fact_employment_structure.csv
    ├── fact_work_conditions.csv
    ├── fact_income.csv
    └── tourism.db
```

The exact generated files depend on the configured pipeline and source data.

---

## 📝 Logging

The project uses Python logging to provide both console output and persistent pipeline logs.

Logs are stored under:

```text
logs/
└── pipeline.log
```

The configuration defines both a file handler and a console handler, making it possible to monitor pipeline execution interactively while retaining a historical execution log.

---

## 🔍 Data Quality Strategy

The project applies several levels of validation.

### Structural validation

Checks that expected columns exist:

```text
period
year
quarter
dimension
category
value
```

### Completeness validation

Key dimensions cannot contain missing values.

### Uniqueness validation

Duplicate combinations of:

```text
period + dimension + category
```

are rejected.

### Coverage validation

Every fact table must contain the expected time periods.

### Numeric validation

Negative observations are rejected.

### Business validation

Demographic totals are reconciled:

```text
Hombre + Mujer = Total
```

This layered approach helps prevent bad data from reaching the final analytical database.

---

## 💡 Example Analytical Questions

Once the SQLite database or CSV files have been generated, the data can support questions such as:

* How have tourism-related socioeconomic indicators changed over time?
* How does the composition of the population change across quarters?
* What percentage of observations correspond to formal versus informal employment?
* How have working hours evolved over time?
* How have income levels changed?
* What demographic groups show the largest changes?
* How do urban and rural populations compare?
* Are changes in employment conditions associated with changes in income?

The repository is therefore structured as a **data-engineering foundation**, rather than a visualization-only project.

---

## 🔮 Potential Extensions

Future improvements could include:

* Add automated tests with `pytest`
* Add a `requirements.txt` or `pyproject.toml`
* Add Docker support
* Add CI/CD with GitHub Actions
* Add a data dictionary
* Add automated source-data ingestion
* Add incremental loading
* Add database constraints and foreign keys
* Add SQL analytics queries
* Build a Power BI, Tableau, or Streamlit dashboard
* Add data profiling reports
* Add pipeline orchestration with Airflow or Prefect
* Add unit and integration tests for every ETL stage

---

## 📚 Data Source

The repository uses the `turismo.xlsx` workbook stored under:

```text
data/raw/turismo.xlsx
```

The current extraction configuration reads the `C2 Total` worksheet.

---

## 👤 Author

**lelizsan2807**
---

## ⭐ Project Summary

This project demonstrates how to transform a complex, semi-structured Excel source into a reliable analytical data platform using Python.

**Raw Excel → Extraction → Transformation → Validation → CSV + SQLite**

The main engineering principles demonstrated are:

* Reproducible ETL
* Separation of pipeline stages
* Data normalization
* Automated data-quality checks
* Business-rule validation
* Structured logging
* Relational data modeling
* Analytics-ready outputs
