"""
Project: Sales Data Analysis
Description: Analyze sales dataset to calculate total revenue,
best-selling product, and generate a markdown report.
Author: Mayuri Wawale
"""

import pandas as pd

# -----------------------------
# Step 1: Load Data
# -----------------------------

try:
    df = pd.read_csv("sales_data.csv")
    print("Dataset loaded successfully!\n")
except FileNotFoundError:
    print("Error: sales_data.csv not found.")
    exit()

# -----------------------------
# Step 2: Explore Data
# -----------------------------

print("Dataset Shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nMissing Values:\n", df.isnull().sum())

# -----------------------------
# Step 3: Clean Data
# -----------------------------

# Remove duplicates
df.drop_duplicates(inplace=True)

# Handle missing values
df["Quantity"].fillna(0, inplace=True)
df["Price"].fillna(df["Price"].mean(), inplace=True)

# Convert Date column (if exists)
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"])

# -----------------------------
# Step 4: Create Revenue Column
# -----------------------------

df["Revenue"] = df["Quantity"] * df["Price"]

# -----------------------------
# Step 5: Calculate Metrics
# -----------------------------

total_revenue = df["Revenue"].sum()
total_quantity = df["Quantity"].sum()
total_orders = len(df)
average_order_value = df["Revenue"].mean()

best_product_quantity = (
    df.groupby("Product")["Quantity"].sum().idxmax()
)

best_product_revenue = (
    df.groupby("Product")["Revenue"].sum().idxmax()
)

top_products = (
    df.groupby("Product")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

# -----------------------------
# Step 6: Generate Markdown Report
# -----------------------------

report = f"""
# 📊 Sales Data Analysis Report

## 📌 Overview
This report summarizes key insights from the sales dataset.

---

## 📈 Key Metrics

- **Total Revenue:** ₹{total_revenue:,.2f}
- **Total Quantity Sold:** {total_quantity}
- **Total Orders:** {total_orders}
- **Average Order Value:** ₹{average_order_value:,.2f}

---

## 🏆 Best Performing Products

- **Best Product (by Quantity):** {best_product_quantity}
- **Best Product (by Revenue):** {best_product_revenue}

---

## 🔝 Top 5 Products by Revenue

{top_products.to_string()}

---

## ✅ Conclusion

The analysis identifies key revenue drivers and best-selling products.
This insight can support inventory planning, marketing strategies,
and business growth decisions.
"""

with open("analysis_report.md", "w", encoding="utf-8") as f:
    f.write(report)

print("\nAnalysis complete! Report saved as analysis_report.md")
