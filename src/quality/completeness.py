"""
DataSentinel - Completeness Quality Check

Checks datasets for missing values and calculates
a completeness score.
"""

from pathlib import Path
import pandas as pd


def check_completeness(file_path):
    """
    Analyze missing values in a CSV dataset.
    """

    df = pd.read_csv(file_path)

    total_cells = df.shape[0] * df.shape[1]

    missing_by_column = df.isnull().sum()

    total_missing = missing_by_column.sum()

    if total_cells == 0:
        completeness_score = 0
    else:
        completeness_score = (
            1 - (total_missing / total_cells)
        ) * 100

    # Classify data quality
    if completeness_score >= 100:
        status = "HEALTHY"
    elif completeness_score >= 95:
        status = "WARNING"
    else:
        status = "CRITICAL"

    results = {
        "dataset": Path(file_path).name,
        "rows": df.shape[0],
        "columns": df.shape[1],
        "total_missing": int(total_missing),
        "completeness_score": round(
            completeness_score,
            2
        ),
        "status": status
    }

    return results


if __name__ == "__main__":

    project_root = Path(__file__).resolve().parents[2]

    customers_file = (
        project_root
        / "data"
        / "processed"
        / "customers_corrupted.csv"
    )

    results = check_completeness(customers_file)

    print("\nDATA QUALITY REPORT")
    print("----------------------------")
    print(f"Dataset: {results['dataset']}")
    print(f"Rows: {results['rows']:,}")
    print(f"Columns: {results['columns']}")
    print(f"Missing values: {results['total_missing']}")
    print(
        f"Completeness Score: "
        f"{results['completeness_score']}/100"
    )
    print(f"Status: {results['status']}")