"""
DataSentinel - Data Quality Summary Report

Runs the main DataSentinel quality checks and stores
the results in the SQLite database.
"""

from pathlib import Path
import sys
import pandas as pd


# Make the project root available to Python
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from database.database import save_quality_report

# --------------------------------------------------
# Completeness Check
# --------------------------------------------------

def calculate_completeness(file_path):
    """Calculate missing values and completeness score."""

    df = pd.read_csv(file_path)

    total_cells = df.shape[0] * df.shape[1]
    total_missing = int(df.isnull().sum().sum())

    if total_cells == 0:
        score = 0
    else:
        score = (
            1 - (total_missing / total_cells)
        ) * 100

    if score >= 100:
        status = "HEALTHY"
    elif score >= 95:
        status = "WARNING"
    else:
        status = "CRITICAL"

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "missing": total_missing,
        "score": round(score, 2),
        "status": status
    }


# --------------------------------------------------
# Duplicate Check
# --------------------------------------------------

def calculate_duplicates(file_path):
    """Calculate duplicate rows."""

    df = pd.read_csv(file_path)

    duplicate_rows = int(df.duplicated().sum())

    if len(df) == 0:
        duplicate_rate = 0
    else:
        duplicate_rate = (
            duplicate_rows / len(df)
        ) * 100

    if duplicate_rows == 0:
        status = "HEALTHY"
    elif duplicate_rate <= 2:
        status = "WARNING"
    else:
        status = "CRITICAL"

    return {
        "rows": len(df),
        "duplicates": duplicate_rows,
        "rate": round(duplicate_rate, 2),
        "status": status
    }


# --------------------------------------------------
# Schema Check
# --------------------------------------------------

def check_schema(file_path):
    """Validate the customer dataset schema."""

    df = pd.read_csv(file_path)

    expected_columns = [
        "customer_id",
        "name",
        "email",
        "city",
        "state",
        "signup_date",
        "age"
    ]

    actual_columns = list(df.columns)

    missing_columns = [
        column
        for column in expected_columns
        if column not in actual_columns
    ]

    unexpected_columns = [
        column
        for column in actual_columns
        if column not in expected_columns
    ]

    if missing_columns or unexpected_columns:
        status = "CRITICAL"
    else:
        status = "HEALTHY"

    return {
        "expected": len(expected_columns),
        "actual": len(actual_columns),
        "missing": missing_columns,
        "unexpected": unexpected_columns,
        "status": status
    }


# --------------------------------------------------
# Anomaly Check
# --------------------------------------------------

def analyze_anomalies(file_path):
    """Analyze behavioral anomaly results."""

    df = pd.read_csv(file_path)

    anomaly_column = None

    possible_columns = [
        "is_anomaly",
        "anomaly",
        "anomaly_flag",
        "outlier",
        "is_outlier"
    ]

    for column in possible_columns:
        if column in df.columns:
            anomaly_column = column
            break

    if anomaly_column is not None:

        values = df[anomaly_column]

        if values.dtype == bool:

            anomaly_count = int(
                values.sum()
            )

        elif pd.api.types.is_numeric_dtype(values):

            anomaly_count = int(
                (values != 0).sum()
            )

        else:

            anomaly_count = int(
                values.astype(str)
                .str.lower()
                .isin([
                    "true",
                    "yes",
                    "anomaly",
                    "outlier",
                    "1"
                ])
                .sum()
            )

        anomaly_rate = (
            anomaly_count / len(df) * 100
            if len(df) > 0
            else 0
        )

        if anomaly_rate == 0:
            status = "HEALTHY"
        elif anomaly_rate <= 2:
            status = "WARNING"
        else:
            status = "CRITICAL"

    else:

        anomaly_count = None
        anomaly_rate = None
        status = "WARNING"

    return {
        "rows": len(df),
        "anomalies": anomaly_count,
        "rate": anomaly_rate,
        "status": status
    }


# --------------------------------------------------
# Overall Status
# --------------------------------------------------

def calculate_overall_status(statuses):
    """Determine the overall DataSentinel status."""

    if "CRITICAL" in statuses:
        return "CRITICAL"

    if "WARNING" in statuses:
        return "WARNING"

    return "HEALTHY"


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    # --------------------------------------------------
    # Project paths
    # --------------------------------------------------

    project_root = Path(__file__).resolve().parents[2]

    raw_data = (
        project_root
        / "data"
        / "raw"
    )

    processed_data = (
        project_root
        / "data"
        / "processed"
    )

    customers_file = (
        raw_data
        / "customers.csv"
    )

    corrupted_file = (
        processed_data
        / "customers_corrupted.csv"
    )

    duplicates_file = (
        processed_data
        / "customers_duplicates.csv"
    )

    broken_schema_file = (
        processed_data
        / "customers_schema_broken.csv"
    )

    anomaly_file = (
        processed_data
        / "customer_behavior_anomalies.csv"
    )

    # --------------------------------------------------
    # Run all checks
    # --------------------------------------------------

    completeness = calculate_completeness(
        corrupted_file
    )

    duplicates = calculate_duplicates(
        duplicates_file
    )

    schema = check_schema(
        broken_schema_file
    )

    anomaly_results = analyze_anomalies(
        anomaly_file
    )

    # --------------------------------------------------
    # Determine overall status
    # --------------------------------------------------

    statuses = [
        completeness["status"],
        duplicates["status"],
        schema["status"],
        anomaly_results["status"]
    ]

    overall_status = calculate_overall_status(
        statuses
    )

    # --------------------------------------------------
    # Print Report
    # --------------------------------------------------

    print()
    print("=" * 60)
    print("              DATASENTINEL QUALITY REPORT")
    print("=" * 60)

    # --------------------------------------------------
    # Completeness
    # --------------------------------------------------

    print()
    print("1. COMPLETENESS")
    print("-" * 60)

    print(
        f"Rows analyzed       : "
        f"{completeness['rows']:,}"
    )

    print(
        f"Columns analyzed    : "
        f"{completeness['columns']}"
    )

    print(
        f"Missing values      : "
        f"{completeness['missing']:,}"
    )

    print(
        f"Completeness score  : "
        f"{completeness['score']}/100"
    )

    print(
        f"Status              : "
        f"{completeness['status']}"
    )

    # --------------------------------------------------
    # Duplicates
    # --------------------------------------------------

    print()
    print("2. DUPLICATE DETECTION")
    print("-" * 60)

    print(
        f"Rows analyzed       : "
        f"{duplicates['rows']:,}"
    )

    print(
        f"Duplicate rows      : "
        f"{duplicates['duplicates']:,}"
    )

    print(
        f"Duplicate rate      : "
        f"{duplicates['rate']}%"
    )

    print(
        f"Status              : "
        f"{duplicates['status']}"
    )

    # --------------------------------------------------
    # Schema
    # --------------------------------------------------

    print()
    print("3. SCHEMA VALIDATION")
    print("-" * 60)

    print(
        f"Expected columns    : "
        f"{schema['expected']}"
    )

    print(
        f"Actual columns      : "
        f"{schema['actual']}"
    )

    print(
        f"Missing columns     : "
        f"{schema['missing'] if schema['missing'] else 'None'}"
    )

    print(
        f"Unexpected columns  : "
        f"{schema['unexpected'] if schema['unexpected'] else 'None'}"
    )

    print(
        f"Status              : "
        f"{schema['status']}"
    )

    # --------------------------------------------------
    # Anomalies
    # --------------------------------------------------

    print()
    print("4. BEHAVIORAL ANOMALY DETECTION")
    print("-" * 60)

    print(
        f"Customers analyzed : "
        f"{anomaly_results['rows']:,}"
    )

    if anomaly_results["anomalies"] is not None:

        print(
            f"Anomalies detected : "
            f"{anomaly_results['anomalies']:,}"
        )

        print(
            f"Anomaly rate       : "
            f"{anomaly_results['rate']:.2f}%"
        )

    else:

        print(
            "Anomalies detected : "
            "See anomaly detector report"
        )

        print(
            "Anomaly rate       : "
            "See anomaly detector report"
        )

    print(
        f"Status              : "
        f"{anomaly_results['status']}"
    )

    # --------------------------------------------------
    # Overall Status
    # --------------------------------------------------

    print()
    print("5. OVERALL DATA QUALITY")
    print("-" * 60)

    print(
        f"Overall Status      : "
        f"{overall_status}"
    )

    # --------------------------------------------------
    # Save Results to Database
    # --------------------------------------------------

    checks = [

        {
            "check_type": "Completeness",
            "status": completeness["status"],
            "metric_name": "completeness_score",
            "metric_value": completeness["score"]
        },

        {
            "check_type": "Duplicates",
            "status": duplicates["status"],
            "metric_name": "duplicate_rate",
            "metric_value": duplicates["rate"]
        },

        {
            "check_type": "Schema",
            "status": schema["status"],
            "metric_name": "missing_columns",
            "metric_value": len(schema["missing"])
        },

        {
            "check_type": "Anomaly Detection",
            "status": anomaly_results["status"],
            "metric_name": "anomaly_rate",
            "metric_value": (
                anomaly_results["rate"]
                if anomaly_results["rate"] is not None
                else 0
            )
        }
    ]

    print()
    print("-" * 60)
    print("Saving quality results to database...")

    report_id = save_quality_report(
        dataset_name="customers.csv",
        overall_status=overall_status,
        checks=checks
    )

    print(
        f"Database report ID: {report_id}"
    )

    # --------------------------------------------------
    # Finished
    # --------------------------------------------------

    print()
    print("=" * 60)
    print("           DATASENTINEL REPORT COMPLETE")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()