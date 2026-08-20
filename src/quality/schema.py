"""
DataSentinel - Schema Validation

Checks whether a dataset contains the expected columns
and whether those columns have the expected data types.
"""

from pathlib import Path

import pandas as pd
from pandas.api.types import (
    is_datetime64_any_dtype,
    is_integer_dtype,
    is_string_dtype
)


# --------------------------------------------------
# Expected Customer Schema
# --------------------------------------------------

EXPECTED_SCHEMA = {
    "customer_id": "string",
    "name": "string",
    "email": "string",
    "age": "integer",
    "city": "string",
    "state": "string",
    "signup_date": "datetime"
}


# --------------------------------------------------
# Data Type Validation
# --------------------------------------------------

def check_data_type(series, expected_type):
    """
    Check whether a Pandas Series matches the
    expected logical data type.
    """

    if expected_type == "string":
        return is_string_dtype(series)

    if expected_type == "integer":
        return is_integer_dtype(series)

    if expected_type == "datetime":
        return is_datetime64_any_dtype(series)

    return False


# --------------------------------------------------
# Schema Validation
# --------------------------------------------------

def validate_schema(file_path):
    """
    Validate columns and data types against the
    expected customer schema.
    """

    df = pd.read_csv(
        file_path,
        parse_dates=["signup_date"]
    )

    expected_columns = set(
        EXPECTED_SCHEMA.keys()
    )

    actual_columns = set(
        df.columns
    )

    # Find missing columns
    missing_columns = sorted(
        expected_columns - actual_columns
    )

    # Find unexpected columns
    unexpected_columns = sorted(
        actual_columns - expected_columns
    )

    # Check data types
    type_mismatches = []

    for column, expected_type in EXPECTED_SCHEMA.items():

        if column not in df.columns:
            continue

        if not check_data_type(
            df[column],
            expected_type
        ):
            type_mismatches.append({
                "column": column,
                "expected": expected_type,
                "actual": str(
                    df[column].dtype
                )
            })

    # --------------------------------------------------
    # Determine Status
    # --------------------------------------------------

    if (
        not missing_columns
        and not unexpected_columns
        and not type_mismatches
    ):
        status = "HEALTHY"

    elif (
        missing_columns
        or type_mismatches
    ):
        status = "CRITICAL"

    else:
        status = "WARNING"

    results = {
        "dataset": Path(file_path).name,
        "expected_columns": len(
            expected_columns
        ),
        "actual_columns": len(
            actual_columns
        ),
        "missing_columns": missing_columns,
        "unexpected_columns": unexpected_columns,
        "type_mismatches": type_mismatches,
        "status": status
    }

    return results


# --------------------------------------------------
# Run Validation
# --------------------------------------------------

if __name__ == "__main__":

    project_root = Path(__file__).resolve().parents[2]
    customers_file = (
        project_root
        / "data"
        / "processed"
        / "customers_schema_broken.csv"
    )
    

    results = validate_schema(
        customers_file
    )

    print("\nSCHEMA VALIDATION REPORT")
    print("----------------------------")

    print(
        f"Dataset: "
        f"{results['dataset']}"
    )

    print(
        f"Expected columns: "
        f"{results['expected_columns']}"
    )

    print(
        f"Actual columns: "
        f"{results['actual_columns']}"
    )

    if results["missing_columns"]:
        print(
            "Missing columns: "
            f"{results['missing_columns']}"
        )
    else:
        print(
            "Missing columns: None"
        )

    if results["unexpected_columns"]:
        print(
            "Unexpected columns: "
            f"{results['unexpected_columns']}"
        )
    else:
        print(
            "Unexpected columns: None"
        )

    if results["type_mismatches"]:

        print("Type mismatches:")

        for mismatch in results[
            "type_mismatches"
        ]:
            print(
                f"  {mismatch['column']}: "
                f"expected {mismatch['expected']}, "
                f"found {mismatch['actual']}"
            )

    else:

        print(
            "Type mismatches: None"
        )

    print(
        f"Status: {results['status']}"
    )