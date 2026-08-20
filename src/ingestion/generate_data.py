"""
DataSentinel - Synthetic E-commerce Data Generator

Generates realistic e-commerce datasets for testing
data quality and anomaly detection.
"""

from pathlib import Path
import numpy as np
import pandas as pd


# --------------------------------------------------
# Configuration
# --------------------------------------------------

RANDOM_SEED = 42
NUM_CUSTOMERS = 5000
NUM_PRODUCTS = 500
NUM_ORDERS = 15000
NUM_ORDER_ITEMS = 30000
NUM_PAYMENTS = 15000
NUM_INVENTORY_RECORDS = 5000

np.random.seed(RANDOM_SEED)


# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw"

RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Generate Customers
# --------------------------------------------------

def generate_customers():
    customer_ids = [
        f"CUST{str(i).zfill(5)}"
        for i in range(1, NUM_CUSTOMERS + 1)
    ]

    first_names = [
        "Ava", "Liam", "Emma", "Noah", "Olivia",
        "Ethan", "Sophia", "Mason", "Mia", "Lucas",
        "Isabella", "James", "Amelia", "Henry", "Harper"
    ]

    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones",
        "Garcia", "Miller", "Davis", "Wilson", "Taylor",
        "Anderson", "Thomas", "Moore", "Martin", "Jackson"
    ]

    first = np.random.choice(first_names, NUM_CUSTOMERS)
    last = np.random.choice(last_names, NUM_CUSTOMERS)

    names = [
        f"{f} {l}"
        for f, l in zip(first, last)
    ]

    emails = [
        f"{name.lower().replace(' ', '.')}@example.com"
        for name in names
    ]

    cities = [
        "Dallas", "Austin", "Houston", "Fort Worth",
        "Arlington", "Plano", "Frisco", "Denton"
    ]

    states = ["TX"]

    customers = pd.DataFrame({
        "customer_id": customer_ids,
        "name": names,
        "email": emails,
        "age": np.random.randint(18, 75, NUM_CUSTOMERS),
        "city": np.random.choice(cities, NUM_CUSTOMERS),
        "state": np.random.choice(states, NUM_CUSTOMERS),
        "signup_date": pd.to_datetime(
            np.random.choice(
                pd.date_range("2023-01-01", "2026-06-30"),
                NUM_CUSTOMERS
            )
        )
    })

    return customers


# --------------------------------------------------
# Generate Products
# --------------------------------------------------

def generate_products():
    product_ids = [
        f"PROD{str(i).zfill(4)}"
        for i in range(1, NUM_PRODUCTS + 1)
    ]

    categories = [
        "Electronics",
        "Home",
        "Clothing",
        "Beauty",
        "Sports",
        "Books"
    ]

    suppliers = [
        "NorthStar Supply",
        "BlueRiver Wholesale",
        "Metro Distribution",
        "PrimeGoods",
        "Summit Suppliers"
    ]

    products = pd.DataFrame({
        "product_id": product_ids,
        "product_name": [
            f"Product {i}"
            for i in range(1, NUM_PRODUCTS + 1)
        ],
        "category": np.random.choice(
            categories,
            NUM_PRODUCTS
        ),
        "price": np.round(
            np.random.uniform(10, 500, NUM_PRODUCTS),
            2
        ),
        "supplier": np.random.choice(
            suppliers,
            NUM_PRODUCTS
        )
    })

    return products


# --------------------------------------------------
# Generate Orders
# --------------------------------------------------

def generate_orders(customers):
    order_ids = [
        f"ORD{str(i).zfill(6)}"
        for i in range(1, NUM_ORDERS + 1)
    ]

    payment_methods = [
        "Credit Card",
        "Debit Card",
        "PayPal",
        "Apple Pay",
        "Google Pay"
    ]

    statuses = [
        "Completed",
        "Completed",
        "Completed",
        "Shipped",
        "Processing",
        "Cancelled"
    ]

    orders = pd.DataFrame({
        "order_id": order_ids,
        "customer_id": np.random.choice(
            customers["customer_id"],
            NUM_ORDERS
        ),
        "order_date": pd.to_datetime(
            np.random.choice(
                pd.date_range(
                    "2026-01-01",
                    "2026-08-14"
                ),
                NUM_ORDERS
            )
        ),
        "status": np.random.choice(
            statuses,
            NUM_ORDERS
        ),
        "total_amount": np.round(
            np.random.lognormal(
                mean=4.1,
                sigma=0.7,
                size=NUM_ORDERS
            ),
            2
        ),
        "payment_method": np.random.choice(
            payment_methods,
            NUM_ORDERS
        )
    })

    return orders


# --------------------------------------------------
# Generate Order Items
# --------------------------------------------------

def generate_order_items(orders, products):
    order_item_ids = [
        f"ITEM{str(i).zfill(7)}"
        for i in range(1, NUM_ORDER_ITEMS + 1)
    ]

    selected_orders = np.random.choice(
        orders["order_id"],
        NUM_ORDER_ITEMS
    )

    selected_products = np.random.choice(
        products["product_id"],
        NUM_ORDER_ITEMS
    )

    product_price_lookup = products.set_index(
        "product_id"
    )["price"]

    selected_prices = [
        product_price_lookup[product_id]
        for product_id in selected_products
    ]

    quantities = np.random.randint(
        1,
        6,
        NUM_ORDER_ITEMS
    )

    order_items = pd.DataFrame({
        "order_item_id": order_item_ids,
        "order_id": selected_orders,
        "product_id": selected_products,
        "quantity": quantities,
        "unit_price": np.round(
            selected_prices,
            2
        )
    })

    return order_items


# --------------------------------------------------
# Generate Payments
# --------------------------------------------------

def generate_payments(orders):
    payment_ids = [
        f"PAY{str(i).zfill(6)}"
        for i in range(1, NUM_PAYMENTS + 1)
    ]

    payment_statuses = [
        "Completed",
        "Completed",
        "Completed",
        "Pending",
        "Failed"
    ]

    payments = pd.DataFrame({
        "payment_id": payment_ids,
        "order_id": orders["order_id"].values,
        "payment_date": orders["order_date"].values,
        "amount": orders["total_amount"].values,
        "payment_method": orders["payment_method"].values,
        "status": np.random.choice(
            payment_statuses,
            NUM_PAYMENTS
        )
    })

    return payments


# --------------------------------------------------
# Generate Inventory
# --------------------------------------------------

def generate_inventory(products):
    inventory_product_ids = np.random.choice(
        products["product_id"],
        NUM_INVENTORY_RECORDS
    )

    warehouses = [
        "WH-DAL-01",
        "WH-AUS-01",
        "WH-HOU-01",
        "WH-FTW-01"
    ]

    inventory = pd.DataFrame({
        "product_id": inventory_product_ids,
        "warehouse_id": np.random.choice(
            warehouses,
            NUM_INVENTORY_RECORDS
        ),
        "inventory_date": pd.to_datetime(
            np.random.choice(
                pd.date_range(
                    "2026-07-01",
                    "2026-08-14"
                ),
                NUM_INVENTORY_RECORDS
            )
        ),
        "stock_quantity": np.random.randint(
            0,
            1000,
            NUM_INVENTORY_RECORDS
        )
    })

    return inventory


# --------------------------------------------------
# Save datasets
# --------------------------------------------------

def save_dataset(dataframe, filename):
    filepath = RAW_DATA_PATH / filename
    dataframe.to_csv(filepath, index=False)

    print(
        f"Created {filename}: "
        f"{len(dataframe):,} rows"
    )


# --------------------------------------------------
# Main pipeline
# --------------------------------------------------

def main():
    print("\nStarting DataSentinel data generation...\n")

    customers = generate_customers()
    products = generate_products()
    orders = generate_orders(customers)
    order_items = generate_order_items(
        orders,
        products
    )
    payments = generate_payments(orders)
    inventory = generate_inventory(products)

    save_dataset(
        customers,
        "customers.csv"
    )

    save_dataset(
        products,
        "products.csv"
    )

    save_dataset(
        orders,
        "orders.csv"
    )

    save_dataset(
        order_items,
        "order_items.csv"
    )

    save_dataset(
        payments,
        "payments.csv"
    )

    save_dataset(
        inventory,
        "inventory.csv"
    )

    print("\nData generation completed successfully! 🚀")
    print(f"Files saved to: {RAW_DATA_PATH}")


if __name__ == "__main__":
    main()