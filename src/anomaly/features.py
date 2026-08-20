"""
DataSentinel - Customer Behavior Features

Combines customer and order data to create behavioral
features for anomaly detection.
"""

from pathlib import Path

import pandas as pd


def build_customer_features(
    customers_file,
    orders_file,
    output_file
):
    """
    Create customer-level behavioral features
    from customer and order data.
    """

    # --------------------------------------------------
    # Load datasets
    # --------------------------------------------------

    customers = pd.read_csv(
        customers_file
    )

    orders = pd.read_csv(
        orders_file
    )

    # --------------------------------------------------
    # Convert order date
    # --------------------------------------------------

    orders["order_date"] = pd.to_datetime(
        orders["order_date"]
    )

    # --------------------------------------------------
    # Keep completed orders for spending metrics
    # --------------------------------------------------

    completed_orders = orders[
        orders["status"] == "Completed"
    ].copy()

    # --------------------------------------------------
    # Aggregate order behavior by customer
    # --------------------------------------------------

    order_features = (
        completed_orders
        .groupby("customer_id")
        .agg(
            number_of_orders=(
                "order_id",
                "count"
            ),
            total_spent=(
                "total_amount",
                "sum"
            ),
            average_order_value=(
                "total_amount",
                "mean"
            )
        )
        .reset_index()
    )

    # --------------------------------------------------
    # Merge customer information
    # --------------------------------------------------

    customer_features = customers.merge(
        order_features,
        on="customer_id",
        how="left"
    )

    # --------------------------------------------------
    # Customers with no completed orders
    # --------------------------------------------------

    numeric_columns = [
        "number_of_orders",
        "total_spent",
        "average_order_value"
    ]

    customer_features[
        numeric_columns
    ] = customer_features[
        numeric_columns
    ].fillna(0)

    # --------------------------------------------------
    # Round monetary values
    # --------------------------------------------------

    customer_features[
        "total_spent"
    ] = customer_features[
        "total_spent"
    ].round(2)

    customer_features[
        "average_order_value"
    ] = customer_features[
        "average_order_value"
    ].round(2)

    # --------------------------------------------------
    # Save feature dataset
    # --------------------------------------------------

    customer_features.to_csv(
        output_file,
        index=False
    )

    # --------------------------------------------------
    # Report
    # --------------------------------------------------

    print(
        "\nCUSTOMER BEHAVIOR FEATURES"
    )
    print(
        "----------------------------"
    )

    print(
        f"Customers: "
        f"{len(customer_features):,}"
    )

    print(
        f"Completed orders analyzed: "
        f"{len(completed_orders):,}"
    )

    print(
        "\nFeatures created:"
    )

    print(
        "  number_of_orders"
    )

    print(
        "  total_spent"
    )

    print(
        "  average_order_value"
    )

    print(
        f"\nSaved feature dataset to:\n"
        f"{output_file}"
    )


if __name__ == "__main__":

    # --------------------------------------------------
    # Project paths
    # --------------------------------------------------

    project_root = (
        Path(__file__).resolve().parents[2]
    )

    customers_file = (
        project_root
        / "data"
        / "raw"
        / "customers.csv"
    )

    orders_file = (
        project_root
        / "data"
        / "raw"
        / "orders.csv"
    )

    output_file = (
        project_root
        / "data"
        / "processed"
        / "customer_features.csv"
    )

    # --------------------------------------------------
    # Build features
    # --------------------------------------------------

    build_customer_features(
        customers_file,
        orders_file,
        output_file
    )