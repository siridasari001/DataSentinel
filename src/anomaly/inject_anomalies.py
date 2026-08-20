"""
DataSentinel - Anomaly Injection

Creates controlled anomalous customer records so that
the DataSentinel ML detector can be tested.
"""

from pathlib import Path

import pandas as pd


def inject_age_anomalies(
    input_file,
    output_file,
    anomaly_count=50
):
    """
    Inject unrealistic customer ages into a copy
    of the dataset.
    """

    df = pd.read_csv(input_file)

    # Select random rows
    rows_to_corrupt = df.sample(
        n=anomaly_count,
        random_state=42
    ).index

    # Create extreme age values
    extreme_ages = [
        150,
        180,
        200,
        999,
        -10
    ]

    # Repeat extreme values if necessary
    for position, row_index in enumerate(
        rows_to_corrupt
    ):
        df.loc[
            row_index,
            "age"
        ] = extreme_ages[
            position % len(extreme_ages)
        ]

    # Save corrupted dataset
    df.to_csv(
        output_file,
        index=False
    )

    print(
        f"Injected {anomaly_count:,} "
        f"age anomalies."
    )

    print(
        "Example anomalous ages:"
    )

    print(
        df.loc[
            rows_to_corrupt,
            ["customer_id", "age"]
        ].head(10)
    )

    print(
        f"\nSaved anomalous dataset to:\n"
        f"{output_file}"
    )


if __name__ == "__main__":

    project_root = (
        Path(__file__).resolve().parents[2]
    )

    input_file = (
        project_root
        / "data"
        / "raw"
        / "customers.csv"
    )

    output_file = (
        project_root
        / "data"
        / "processed"
        / "customers_anomalies.csv"
    )

    inject_age_anomalies(
        input_file,
        output_file,
        anomaly_count=50
    )