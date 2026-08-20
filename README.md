# 🛡️ DataSentinel

## Data Quality & Anomaly Detection Platform

DataSentinel is a Python-based data quality monitoring platform designed to detect common data-quality problems and behavioral anomalies in datasets.

The platform analyzes datasets for:

- Missing values
- Duplicate records
- Schema violations
- Behavioral anomalies
- Customer behavior patterns

Quality results are stored in a SQLite database and presented through an interactive Streamlit dashboard.

---

## ✨ Features

### 1. Completeness Analysis

DataSentinel calculates the percentage of non-missing values in a dataset.

It reports:

- Total rows
- Total columns
- Missing values
- Completeness score
- Quality status

Example:

```text
Dataset: customers_corrupted.csv
Rows: 5,000
Columns: 7
Missing values: 500
Completeness Score: 98.57/100
Status: WARNING
```

---

### 2. Duplicate Detection

The duplicate detection module identifies duplicate records and calculates the duplicate rate.

Example:

```text
Dataset: customers_duplicates.csv
Rows: 5,250
Duplicate rows: 250
Duplicate rate: 4.76%
Status: WARNING
```

---

### 3. Schema Validation

DataSentinel validates datasets against an expected customer schema.

It checks:

- Expected columns
- Actual columns
- Missing columns
- Unexpected columns

Example:

```text
Dataset: customers_schema_broken.csv
Expected columns: 7
Actual columns: 6
Missing columns: ['state']
Status: CRITICAL
```

---

### 4. Behavioral Anomaly Detection

The anomaly detection module identifies unusual customer behavior using customer-level behavioral features.

The system analyzes behavioral information such as:

- Number of orders
- Total spending
- Average order value

Example:

```text
Dataset: customers_anomalies.csv
Rows: 5,000
Anomaly Rate: 0.80%
Status: WARNING
```

---

### 5. Feature Engineering

DataSentinel creates customer-level behavioral features from customer and order data.

Generated features include:

```text
number_of_orders
total_spent
average_order_value
```

These features are used by the anomaly detection pipeline.

---

### 6. Issue Simulation

DataSentinel includes controlled data corruption scripts that simulate real-world data quality problems.

The project can generate:

- Missing email values
- Duplicate records
- Schema changes
- Artificial behavioral anomalies

This allows the detection modules to be tested against known problems.

---

### 7. SQLite Reporting Database

Quality reports are stored in a SQLite database.

The reporting layer records information such as:

- Dataset name
- Report date
- Overall status
- Quality metrics

This allows previous quality reports to be displayed in the dashboard.

---

### 8. Interactive Streamlit Dashboard

The Streamlit dashboard provides a visual interface for exploring data quality.

The dashboard displays:

- Number of reports generated
- Latest report
- Overall quality status
- Report date
- Dataset quality score
- Completeness
- Duplicate rate
- Schema status
- Anomaly rate
- Quality metrics
- Dataset information

Users can select different datasets and inspect their quality results interactively.

---

## 🏗️ Project Architecture

```text
DataSentinel/
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   │   └── customer and transaction datasets
│   │
│   └── processed/
│       ├── customer_features.csv
│       ├── customers_anomalies.csv
│       ├── customers_corrupted.csv
│       ├── customers_duplicates.csv
│       └── customers_schema_broken.csv
│
├── database/
│   └── database.py
│
├── src/
│   ├── anomaly/
│   │   ├── detector.py
│   │   ├── features.py
│   │   └── inject_anomalies.py
│   │
│   ├── ingestion/
│   │   └── generate_data.py
│   │
│   ├── quality/
│   │   ├── completeness.py
│   │   ├── duplicates.py
│   │   ├── inject_issues.py
│   │   └── schema.py
│   │
│   └── reporting/
│       └── quality_report.py
│
├── .gitignore
└── README.md
```

---

## 🔄 DataSentinel Workflow

```text
                 ┌──────────────────┐
                 │   Raw Datasets   │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Quality Analysis │
                 └────────┬─────────┘
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
       Completeness   Duplicates     Schema
             │            │            │
             └────────────┼────────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Feature Creation │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ Anomaly Detection│
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ SQLite Reporting │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │    Streamlit     │
                 │    Dashboard     │
                 └──────────────────┘
```

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core application and analysis |
| Pandas | Data processing and analysis |
| SQLite | Quality report storage |
| Streamlit | Interactive dashboard |
| NumPy | Numerical analysis and anomaly detection |
| Pathlib | Project file and path management |
| Git | Version control |
| GitHub | Source code hosting |

---

## 📊 Example Quality Results

DataSentinel was tested using intentionally corrupted datasets to verify that each quality check correctly identifies known issues.

| Dataset | Test | Result |
|---|---|---|
| `customers_corrupted.csv` | Missing values | 🟡 Warning |
| `customers_duplicates.csv` | Duplicate records | 🟡 Warning |
| `customers_schema_broken.csv` | Schema violation | 🔴 Critical |
| `customers_anomalies.csv` | Behavioral anomalies | 🟡 Warning |

### Completeness Test

```text
Dataset: customers_corrupted.csv
Rows: 5,000
Columns: 7
Completeness: 98.57%
Status: WARNING
```

### Duplicate Test

```text
Dataset: customers_duplicates.csv
Rows: 5,250
Duplicate rows: 250
Duplicate rate: 4.76%
Status: WARNING
```

### Schema Test

```text
Dataset: customers_schema_broken.csv
Expected columns: 7
Actual columns: 6
Missing columns: ['state']
Status: CRITICAL
```

### Anomaly Test

```text
Dataset: customers_anomalies.csv
Rows: 5,000
Anomaly rate: 0.80%
Status: WARNING
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/siridasari001/DataSentinel.git
cd DataSentinel
```

### 2. Create a Virtual Environment

Windows:

```bash
python -m venv .venv
```

Activate the environment:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install pandas numpy streamlit
```

### 4. Run the Streamlit Dashboard

From the project root:

```bash
python -m streamlit run dashboard/app.py
```

The dashboard will open locally in your browser.

---

## 🧪 Running the Quality Checks

### Completeness

```bash
python src/quality/completeness.py
```

### Duplicate Detection

```bash
python src/quality/duplicates.py
```

### Schema Validation

```bash
python src/quality/schema.py
```

### Behavioral Anomaly Detection

```bash
python src/anomaly/detector.py
```

### Feature Engineering

```bash
python src/anomaly/features.py
```

### Quality Reporting

```bash
python src/reporting/quality_report.py
```

---

## 🎯 Project Goals

DataSentinel was designed to demonstrate how automated data-quality monitoring can be incorporated into a data-processing workflow.

The project focuses on:

- Automated quality validation
- Reproducible issue detection
- Data-quality scoring
- Behavioral anomaly identification
- Persistent quality reporting
- Interactive data visualization

---

## 🔮 Future Improvements

Potential future improvements include:

- Automated scheduled dataset monitoring
- Email or Slack alerts for critical quality issues
- Additional anomaly detection algorithms
- Machine-learning-based data-quality prediction
- REST API integration
- Cloud deployment
- Historical quality trend visualization
- Automated data remediation

---

## 👩‍💻 Author

**Siri Dasari**

MS Computer Science  
University of North Texas

GitHub: [siridasari001](https://github.com/siridasari001)

---

## 📄 License

This project is intended for educational and portfolio purposes.
