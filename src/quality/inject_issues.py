"""
DataSentinel - Data Issue Simulator

Creates controlled data-quality problems so that
DataSentinel can test whether it detects them.
"""

from pathlib import Path
import pandas as pd


def inject_missing_emails(input_file, output_file, missing_rate=0.10):
    """
    Randomly removes email values from a dataset.
    """

    df = pd.read_csv(input_file)

    number_to_corrupt = int(
        len(df) * missing_rate
    )

    rows_to_corrupt = df.sample(
        n=number_to_corrupt,
        random_state=42
    ).index

    df.loc[
        rows_to_corrupt,
        "email"
    ] = None

    df.to_csv(
        output_file,
        index=False
    )

    print(
        f"Injected missing emails into "
        f"{number_to_corrupt:,} rows."
    )

    print(
        f"Saved corrupted dataset to:\n"
        f"{output_file}"
    )


def inject_duplicate_rows(
    input_file,
    output_file,
    duplicate_rate=0.05
):
    """
    Adds duplicate customer rows to a dataset.
    """

    df = pd.read_csv(input_file)

    number_to_duplicate = int(
        len(df) * duplicate_rate
    )

    duplicate_rows = df.sample(
        n=number_to_duplicate,
        random_state=42
    )

    corrupted_df = pd.concat(
        [df, duplicate_rows],
        ignore_index=True
    )

    corrupted_df.to_csv(
        output_file,
        index=False
    )

    print(
        f"Injected {number_to_duplicate:,} "
        f"duplicate rows."
    )

    print(
        f"Original rows: {len(df):,}"
    )

    print(
        f"New rows: {len(corrupted_df):,}"
    )

    print(
        f"Saved corrupted dataset to:\n"
        f"{output_file}"
    )


def inject_schema_change(
    input_file,
    output_file
):
    """
    Removes the state column from a dataset
    to simulate a schema-breaking change.
    """

    df = pd.read_csv(input_file)

    if "state" in df.columns:
        df = df.drop(columns=["state"])

    df.to_csv(
        output_file,
        index=False
    )

    print(
        "Removed 'state' column to simulate "
        "a schema change."
    )

    print(
        f"Original columns: 7"
    )

    print(
        f"New columns: {len(df.columns)}"
    )

    print(
        f"Saved corrupted dataset to:\n"
        f"{output_file}"
    )


if __name__ == "__main__":

    project_root = Path(__file__).resolve().parents[2]

    # Original clean dataset
    input_file = (
        project_root
        / "data"
        / "raw"
        / "customers.csv"
    )

    # --------------------------------------------------
    # Issue 1: Missing Emails
    # --------------------------------------------------

    missing_email_output = (
        project_root
        / "data"
        / "processed"
        / "customers_corrupted.csv"
    )

    inject_missing_emails(
        input_file,
        missing_email_output,
        missing_rate=0.10
    )

    # --------------------------------------------------
    # Issue 2: Duplicate Rows
    # --------------------------------------------------

    duplicate_output = (
        project_root
        / "data"
        / "processed"
        / "customers_duplicates.csv"
    )

    inject_duplicate_rows(
        input_file,
        duplicate_output,
        duplicate_rate=0.05
    )

    # --------------------------------------------------
    # Issue 3: Schema Change
    # --------------------------------------------------

    schema_output = (
        project_root
        / "data"
        / "processed"
        / "customers_schema_broken.csv"
    )

    inject_schema_change(
        input_file,
        schema_output
    )