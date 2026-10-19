import pandas as pd
from typing import TypedDict

class SalesRecord(TypedDict):
    Order_id: int
    Revenue: float
    Category: str

def summarize_sales(records: list[SalesRecord]) -> dict | str:
    """Summarize sales records.

    Args:
        records: A list of sales records with required keys:
            - Order_id: int
            - Revenue: float
            - Category: str

    Returns:
        dict with total_revenue, number_of_orders,
        avg_order_value, and revenue_by_category."""

    if not records:
        return "No records found"

    for record in records:
        if not isinstance(record, dict):
            raise TypeError("Each record must be a dictionary.")

        required = {"Order_id", "Revenue", "Category"}
        missing = required - record.keys()
        if missing:
            raise ValueError(f"Missing required fields: {sorted(missing)}")

    df = pd.DataFrame(records)

    raw_revenue = df["Revenue"]
    numeric_revenue = pd.to_numeric(raw_revenue, errors="coerce")

    missing_revenue_count = numeric_revenue.isna().sum()
    valid_revenue = df.loc[numeric_revenue.notna()]
    negative_revenue_count = (valid_revenue['Revenue'] < 0).sum()
    negative_revenue = valid_revenue.loc[valid_revenue['Revenue'] < 0,"Revenue"].sum()
    total_revenue = valid_revenue['Revenue'].sum()
    number_of_orders = valid_revenue['Order_id'].count()
    avg_order_value = total_revenue / number_of_orders if number_of_orders else 0

    missing_category_count = int(df["Category"].isna().sum())
    df["Category"] = df["Category"].fillna("Uncategorized")
    revenue_by_category = {}
    revenue_by_category = (
            df.groupby('Category')['Revenue'].sum().to_dict()
        )
    return {
        "total_revenue": total_revenue,
        "number_of_orders": number_of_orders,
        "avg_order_value": avg_order_value,
        "revenue_by_category": revenue_by_category,
        "missing_revenue_count": missing_revenue_count,
        "negative_revenue_count": negative_revenue_count,
        "negative_revenue": negative_revenue,
        "missing_category_count": missing_category_count
    }

records = [
    {"Order_id": 1, "Revenue": 100.0, "Category": "Electronics"},
    {"Order_id": 2, "Revenue": 200.0, "Category": "Clothing"},
    {"Order_id": 3, "Revenue": 150.0, "Category": "Electronics"},
    {"Order_id": 4, "Revenue": None, "Category": "Clothing"},
    {"Order_id": 5, "Revenue": -50.0, "Category": None},
    {"Order_id": 5, "Revenue": -50.0, "Category": "Electronics"},
    {"Order_id": 6, "Revenue": -300.0, "Category": "Clothing"},
]
summary = summarize_sales(records)
# print(f"Sales reported total revenue of {summary['total_revenue']}M with {summary['number_of_orders']} orders, an average order value of {summary['avg_order_value']}M, and revenue by category: {summary['revenue_by_category']}.")
print(summary)