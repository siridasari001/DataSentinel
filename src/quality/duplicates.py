"""
DataSentinel - Duplicate Detection

Checks datasets for duplicate rows and calculates
a duplicate rate.
"""

from pathlib import Path
import pandas as pd


def check_duplicates(file_path):
    """
    Analyze duplicate rows in a CSV dataset.
    """

    df = pd.read_csv(file_path)

    total_rows = len(df)

    duplicate_rows = df.duplicated().sum()

    if total_rows == 0:
        duplicate_rate = 0
    else:
        duplicate_rate = (
            duplicate_rows / total_rows
        ) * 100

    # Classify duplicate quality
    if duplicate_rate == 0:
        status = "HEALTHY"
    elif duplicate_rate <= 1:
        status = "WARNING"
    else:
        status = "CRITICAL"

    results = {
        "dataset": Path(file_path).name,
        "rows": total_rows,
        "duplicate_rows": int(duplicate_rows),
        "duplicate_rate": round(
            duplicate_rate,
            2
        ),
        "status": status
    }

    return results


if __name__ == "__main__":

    project_root = Path(__file__).resolve().parents[2]

    duplicates_file = (
        project_root
        / "data"
        / "processed"
        / "customers_duplicates.csv"
    )

    results = check_duplicates(
        duplicates_file
    )

    print("\nDUPLICATE DATA QUALITY REPORT")
    print("----------------------------")
    print(f"Dataset: {results['dataset']}")
    print(f"Rows: {results['rows']:,}")
    print(
        f"Duplicate rows: "
        f"{results['duplicate_rows']}"
    )
    print(
        f"Duplicate rate: "
        f"{results['duplicate_rate']}%"
    )
    print(f"Status: {results['status']}")