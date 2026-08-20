"""
DataSentinel - Customer Anomaly Detector

Uses Isolation Forest to detect unusual customer behavior.
"""

from pathlib import Path

import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_anomalies(file_path, output_file):
    """
    Detect unusual customer behavior using Isolation Forest.
    """

    # --------------------------------------------------
    # Load customer feature dataset
    # --------------------------------------------------

    df = pd.read_csv(file_path)

    # --------------------------------------------------
    # Features used for anomaly detection
    # --------------------------------------------------

    feature_columns = [
        "age",
        "number_of_orders",
        "total_spent",
        "average_order_value"
    ]

    X = df[feature_columns].copy()

    # --------------------------------------------------
    # Create Isolation Forest model
    # --------------------------------------------------

    model = IsolationForest(
        n_estimators=200,
        contamination=0.02,
        random_state=42
    )

    # --------------------------------------------------
    # Fit model and predict anomalies
    # --------------------------------------------------

    df["anomaly_prediction"] = model.fit_predict(X)

    # Isolation Forest:
    #   1  = normal
    #  -1  = anomaly

    df["is_anomaly"] = (
        df["anomaly_prediction"] == -1
    )

    # --------------------------------------------------
    # Calculate anomaly statistics
    # --------------------------------------------------

    anomalies_detected = int(
        df["is_anomaly"].sum()
    )

    total_rows = len(df)

    anomaly_rate = (
        anomalies_detected / total_rows
    ) * 100

    # --------------------------------------------------
    # Determine status
    # --------------------------------------------------

    if anomaly_rate <= 1:
        status = "HEALTHY"
    elif anomaly_rate <= 5:
        status = "WARNING"
    else:
        status = "CRITICAL"

    # --------------------------------------------------
    # Save results
    # --------------------------------------------------

    df.to_csv(
        output_file,
        index=False
    )

    # --------------------------------------------------
    # Print report
    # --------------------------------------------------

    print(
        "\nCUSTOMER BEHAVIOR ANOMALY REPORT"
    )

    print(
        "-----------------------------------"
    )

    print(
        f"Dataset: "
        f"{Path(file_path).name}"
    )

    print(
        f"Customers analyzed: "
        f"{total_rows:,}"
    )

    print(
        f"Anomalies detected: "
        f"{anomalies_detected:,}"
    )

    print(
        f"Anomaly rate: "
        f"{anomaly_rate:.2f}%"
    )

    print(
        f"Status: {status}"
    )

    print(
        f"\nFeatures analyzed:"
    )

    for feature in feature_columns:
        print(
            f"  - {feature}"
        )

    print(
        f"\nSaved anomaly results to:\n"
        f"{output_file}"
    )


if __name__ == "__main__":

    # --------------------------------------------------
    # Project root
    # --------------------------------------------------

    project_root = (
        Path(__file__).resolve().parents[2]
    )

    # --------------------------------------------------
    # Input dataset
    # --------------------------------------------------

    input_file = (
        project_root
        / "data"
        / "processed"
        / "customer_features.csv"
    )

    # --------------------------------------------------
    # Output dataset
    # --------------------------------------------------

    output_file = (
        project_root
        / "data"
        / "processed"
        / "customer_behavior_anomalies.csv"
    )

    # --------------------------------------------------
    # Run anomaly detection
    # --------------------------------------------------

    detect_anomalies(
        input_file,
        output_file
    )