"""
DataSentinel - Database Layer

Stores DataSentinel quality-check results in a SQLite database.
"""

from pathlib import Path
import sqlite3
from datetime import datetime


# --------------------------------------------------
# Database location
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATABASE_DIR = PROJECT_ROOT / "database"
DATABASE_FILE = DATABASE_DIR / "datasentinel.db"


# --------------------------------------------------
# Create database and tables
# --------------------------------------------------

def create_database():
    """Create the DataSentinel SQLite database and tables."""

    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    # Main report table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quality_reports (
            report_id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_name TEXT NOT NULL,
            created_at TEXT NOT NULL,
            overall_status TEXT NOT NULL
        )
    """)

    # Individual quality checks
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quality_checks (
            check_id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER NOT NULL,
            check_type TEXT NOT NULL,
            status TEXT NOT NULL,
            metric_name TEXT,
            metric_value REAL,
            FOREIGN KEY (report_id)
                REFERENCES quality_reports(report_id)
        )
    """)

    connection.commit()
    connection.close()

    print("Database created successfully!")
    print(f"Database location: {DATABASE_FILE}")


# --------------------------------------------------
# Insert a quality report
# --------------------------------------------------

def save_quality_report(
    dataset_name,
    overall_status,
    checks
):
    """
    Save a complete DataSentinel quality report.

    Parameters
    ----------
    dataset_name : str
        Name of the dataset being analyzed.

    overall_status : str
        Overall report status.

    checks : list of dictionaries
        Individual quality-check results.
    """

    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    created_at = datetime.now().isoformat(
        timespec="seconds"
    )

    # Insert main report
    cursor.execute("""
        INSERT INTO quality_reports (
            dataset_name,
            created_at,
            overall_status
        )
        VALUES (?, ?, ?)
    """, (
        dataset_name,
        created_at,
        overall_status
    ))

    report_id = cursor.lastrowid

    # Insert individual checks
    for check in checks:

        cursor.execute("""
            INSERT INTO quality_checks (
                report_id,
                check_type,
                status,
                metric_name,
                metric_value
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            report_id,
            check["check_type"],
            check["status"],
            check["metric_name"],
            check["metric_value"]
        ))

    connection.commit()
    connection.close()

    print()
    print("Quality report saved successfully!")
    print(f"Report ID: {report_id}")

    return report_id


# --------------------------------------------------
# Display saved reports
# --------------------------------------------------

def show_reports():
    """Display all saved DataSentinel reports."""

    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            report_id,
            dataset_name,
            created_at,
            overall_status
        FROM quality_reports
        ORDER BY report_id DESC
    """)

    reports = cursor.fetchall()

    connection.close()

    print()
    print("DATASENTINEL DATABASE REPORTS")
    print("=" * 60)

    if not reports:
        print("No reports have been saved yet.")
        return

    for report in reports:

        report_id = report[0]
        dataset_name = report[1]
        created_at = report[2]
        status = report[3]

        print(
            f"Report ID: {report_id} | "
            f"Dataset: {dataset_name} | "
            f"Status: {status}"
        )

        print(
            f"Created: {created_at}"
        )

        print("-" * 60)


# --------------------------------------------------
# Display quality checks for a report
# --------------------------------------------------

def show_checks(report_id):
    """Display individual checks for a specific report."""

    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            check_type,
            status,
            metric_name,
            metric_value
        FROM quality_checks
        WHERE report_id = ?
    """, (report_id,))

    checks = cursor.fetchall()

    connection.close()

    print()
    print(f"QUALITY CHECKS FOR REPORT {report_id}")
    print("=" * 60)

    if not checks:
        print("No quality checks found.")
        return

    for check in checks:

        check_type = check[0]
        status = check[1]
        metric_name = check[2]
        metric_value = check[3]

        print(
            f"{check_type}: "
            f"{status}"
        )

        if metric_name is not None:
            print(
                f"  {metric_name}: "
                f"{metric_value}"
            )

        print("-" * 60)


# --------------------------------------------------
# Test database
# --------------------------------------------------

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("           DATASENTINEL DATABASE")
    print("=" * 60)

    # Create database
    create_database()

    # Create a sample report
    sample_checks = [

        {
            "check_type": "Completeness",
            "status": "WARNING",
            "metric_name": "completeness_score",
            "metric_value": 98.57
        },

        {
            "check_type": "Duplicates",
            "status": "CRITICAL",
            "metric_name": "duplicate_rate",
            "metric_value": 4.76
        },

        {
            "check_type": "Schema",
            "status": "CRITICAL",
            "metric_name": "missing_columns",
            "metric_value": 1
        },

        {
            "check_type": "Anomaly Detection",
            "status": "WARNING",
            "metric_name": "anomaly_rate",
            "metric_value": 2.00
        }
    ]

    report_id = save_quality_report(
        dataset_name="customers.csv",
        overall_status="CRITICAL",
        checks=sample_checks
    )

    # Display reports
    show_reports()

    # Display checks
    show_checks(report_id)

    print()
    print("=" * 60)
    print("           DATABASE TEST COMPLETE")
    print("=" * 60)