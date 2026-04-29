"""
============================================================
  Automated Data Cleaning & Formatting Script
  Input  : raw_ecommerce_data.csv  (messy dataset)
  Tools  : Python, Pandas
  Output : cleaned_ecommerce_data.csv
           cleaning_report.txt
============================================================
"""

import pandas as pd
import numpy as np
import os

# ── Configuration ────────────────────────────────────────
INPUT_FILE   = "raw_ecommerce_data.csv"
OUTPUT_CSV   = "cleaned_ecommerce_data.csv"
REPORT_FILE  = "cleaning_report.txt"

# Country name standardization map
COUNTRY_MAP = {
    "USA"            : "United States",
    "US"             : "United States",
    "UK"             : "United Kingdom",
    "U.K."           : "United Kingdom",
    "U.S."           : "United States",
    "U.S.A."         : "United States",
}

# Valid order statuses
VALID_STATUSES = ["Completed", "Pending", "Shipped", "Cancelled"]


# ── Logger ───────────────────────────────────────────────
class CleaningLog:
    """Tracks all cleaning actions for the final report."""
    def __init__(self):
        self.entries = []

    def log(self, step: str, detail: str) -> None:
        entry = f"  [{step}] {detail}"
        print(entry)
        self.entries.append(entry)

    def save(self, filename: str) -> None:
        with open(filename, "w") as f:
            f.write("=" * 55 + "\n")
            f.write("  DATA CLEANING REPORT\n")
            f.write(f"  Input  : {INPUT_FILE}\n")
            f.write(f"  Output : {OUTPUT_CSV}\n")
            f.write("=" * 55 + "\n\n")
            for entry in self.entries:
                f.write(entry + "\n")
        print(f"\n  ✅  Report saved to '{filename}'")


log = CleaningLog()


# ── Step 1: Load Data ────────────────────────────────────
def load_data(filepath: str) -> pd.DataFrame:
    print("=" * 55)
    print("  Automated Data Cleaning & Formatting Script")
    print("=" * 55)
    print(f"\n── Step 1: Loading Data ───────────────────────────")

    df = pd.read_csv(filepath)
    log.log("LOAD", f"Loaded '{filepath}' → {df.shape[0]} rows × {df.shape[1]} columns")
    log.log("LOAD", f"Columns: {list(df.columns)}")
    return df


# ── Step 2: Remove Duplicates ────────────────────────────
def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    print(f"\n── Step 2: Removing Duplicates ────────────────────")
    before = len(df)

    # Exact duplicates
    df = df.drop_duplicates()
    exact = before - len(df)

    # Fuzzy duplicates — same email + product + date
    before2 = len(df)
    df["_date_norm"] = pd.to_datetime(df["Order_Date"], dayfirst=True, errors="coerce").dt.date
    df = df.drop_duplicates(subset=["Email", "Product", "_date_norm"], keep="first")
    df = df.drop(columns=["_date_norm"])
    fuzzy = before2 - len(df)

    log.log("DUPLICATES", f"Exact duplicates removed   : {exact}")
    log.log("DUPLICATES", f"Fuzzy duplicates removed   : {fuzzy}")
    log.log("DUPLICATES", f"Rows after deduplication   : {len(df)}")
    return df


# ── Step 3: Fix Column Formatting ───────────────────────
def fix_formatting(df: pd.DataFrame) -> pd.DataFrame:
    print(f"\n── Step 3: Fixing Formatting ──────────────────────")

    # Strip whitespace from all string columns
    str_cols = df.select_dtypes(include="object").columns
    for col in str_cols:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace("nan", np.nan)
    log.log("FORMAT", "Stripped leading/trailing whitespace from all columns")

    # Fix Customer_Name — proper title case
    df["Customer_Name"] = df["Customer_Name"].str.title()
    log.log("FORMAT", "Customer_Name → converted to Title Case")

    # Fix Category — proper title case
    df["Category"] = df["Category"].str.title()
    log.log("FORMAT", "Category → converted to Title Case")

    # Fix Status — standardize to Title Case
    df["Status"] = df["Status"].str.title()
    log.log("FORMAT", f"Status → standardized to Title Case {VALID_STATUSES}")

    # Standardize Country names
    df["Country"] = df["Country"].replace(COUNTRY_MAP)
    log.log("FORMAT", f"Country → standardized abbreviations (USA→United States, UK→United Kingdom)")

    return df


# ── Step 4: Fix Data Types ───────────────────────────────
def fix_data_types(df: pd.DataFrame) -> pd.DataFrame:
    print(f"\n── Step 4: Fixing Data Types ──────────────────────")

    # Fix Order_Date — handles both YYYY-MM-DD and DD/MM/YYYY
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], dayfirst=True, errors="coerce")
    df["Order_Date"] = df["Order_Date"].dt.strftime("%Y-%m-%d")
    log.log("TYPES", "Order_Date → unified to YYYY-MM-DD format")

    # Fix Price — numeric
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce").round(2)
    log.log("TYPES", "Price → converted to float, rounded to 2 decimals")

    # Fix Quantity — integer
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").astype("Int64")
    log.log("TYPES", "Quantity → converted to integer")

    return df


# ── Step 5: Handle Missing Values ───────────────────────
def handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    print(f"\n── Step 5: Handling Missing Values ────────────────")

    missing_before = df.isnull().sum()

    # Drop rows where critical fields are missing
    critical_cols = ["Customer_Name", "Product", "Order_Date"]
    before = len(df)
    df = df.dropna(subset=critical_cols)
    dropped = before - len(df)
    log.log("MISSING", f"Dropped {dropped} rows with missing critical fields {critical_cols}")

    # Fill missing Price with median price of that category
    missing_price = df["Price"].isnull().sum()
    df["Price"] = df.groupby("Category")["Price"].transform(
        lambda x: x.fillna(x.median())
    )
    log.log("MISSING", f"Price → filled {missing_price} missing values with category median")

    # Fill missing Quantity with 1 (minimum order)
    missing_qty = df["Quantity"].isnull().sum()
    df["Quantity"] = df["Quantity"].fillna(1)
    log.log("MISSING", f"Quantity → filled {missing_qty} missing values with 1")

    # Fill missing Email with placeholder
    missing_email = df["Email"].isnull().sum()
    df["Email"] = df["Email"].fillna("not_provided@unknown.com")
    log.log("MISSING", f"Email → filled {missing_email} missing values with placeholder")

    # Fill missing Country with Unknown
    missing_country = df["Country"].isnull().sum()
    df["Country"] = df["Country"].fillna("Unknown")
    log.log("MISSING", f"Country → filled {missing_country} missing values with 'Unknown'")

    return df


# ── Step 6: Add Calculated Columns ──────────────────────
def add_columns(df: pd.DataFrame) -> pd.DataFrame:
    print(f"\n── Step 6: Adding Calculated Columns ──────────────")

    df["Total_Value"] = (df["Price"] * df["Quantity"]).round(2)
    log.log("COLUMNS", "Added 'Total_Value' = Price × Quantity")

    df["Order_Month"] = pd.to_datetime(df["Order_Date"]).dt.strftime("%B %Y")
    log.log("COLUMNS", "Added 'Order_Month' extracted from Order_Date")

    return df


# ── Step 7: Final Validation ─────────────────────────────
def validate(df: pd.DataFrame) -> pd.DataFrame:
    print(f"\n── Step 7: Final Validation ───────────────────────")

    # Remove rows with negative price or quantity
    before = len(df)
    df = df[(df["Price"] > 0) & (df["Quantity"] > 0)]
    removed = before - len(df)
    log.log("VALIDATE", f"Removed {removed} rows with invalid Price/Quantity values")

    # Reset index cleanly
    df = df.reset_index(drop=True)
    df.index += 1
    df.index.name = "Row"

    log.log("VALIDATE", f"Final dataset: {len(df)} rows × {len(df.columns)} columns")
    log.log("VALIDATE", f"All columns: {list(df.columns)}")
    return df


# ── Summary ──────────────────────────────────────────────
def print_summary(raw_df: pd.DataFrame, clean_df: pd.DataFrame) -> None:
    print(f"\n── Cleaning Summary ───────────────────────────────")
    print(f"  Rows before cleaning : {len(raw_df)}")
    print(f"  Rows after cleaning  : {len(clean_df)}")
    print(f"  Rows removed         : {len(raw_df) - len(clean_df)}")
    print(f"  Columns added        : Total_Value, Order_Month")
    print(f"\n── Dataset Preview (first 5 rows) ─────────────────")
    print(clean_df[["Customer_Name", "Product", "Price",
                     "Quantity", "Total_Value", "Status", "Country"]].head().to_string())

    print(f"\n── Stats ───────────────────────────────────────────")
    print(f"  Total revenue        : ${clean_df['Total_Value'].sum():,.2f}")
    print(f"  Avg order value      : ${clean_df['Total_Value'].mean():.2f}")
    print(f"  Top category         : {clean_df['Category'].value_counts().idxmax()}")
    print(f"  Top country          : {clean_df['Country'].value_counts().idxmax()}")
    print(f"  Completed orders     : {(clean_df['Status'] == 'Completed').sum()}")
    print("─" * 51)

    log.log("SUMMARY", f"Rows before: {len(raw_df)} → after: {len(clean_df)}")
    log.log("SUMMARY", f"Total revenue: ${clean_df['Total_Value'].sum():,.2f}")
    log.log("SUMMARY", f"Top category: {clean_df['Category'].value_counts().idxmax()}")


# ── Entry Point ──────────────────────────────────────────
if __name__ == "__main__":
    # Load
    raw_df = load_data(INPUT_FILE)

    # Clean
    df = raw_df.copy()
    df = remove_duplicates(df)
    df = fix_formatting(df)
    df = fix_data_types(df)
    df = handle_missing(df)
    df = add_columns(df)
    df = validate(df)

    # Save
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"\n  ✅  Clean data saved to '{OUTPUT_CSV}'")

    # Report
    print_summary(raw_df, df)
    log.save(REPORT_FILE)
