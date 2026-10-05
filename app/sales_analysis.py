import pandas as pd


def analyze_sales(csv_path: str):
    df = pd.read_csv(csv_path)
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    product = df.groupby("Product", as_index=False).agg(Quantity=("Quantity", "sum"), Revenue=("Revenue", "sum"))
    product = product.sort_values("Revenue", ascending=False)
    daily = df.groupby("Date", as_index=False)["Revenue"].sum()
    return {
        "total_revenue": float(df["Revenue"].sum()),
        "total_units": int(df["Quantity"].sum()),
        "top_products": product.to_dict("records"),
        "daily_revenue": daily.to_dict("records"),
    }
