# 🧹 Automated Data Cleaning & Formatting Script

A Python script that automatically cleans and organizes raw, messy datasets by removing duplicates, fixing formatting issues, handling missing values, and structuring data for reporting — all in one run.

---

## 📌 Project Overview

Real-world datasets are messy. This script takes a raw e-commerce orders CSV with common issues like inconsistent formatting, duplicate records, missing values, and mixed date formats — and transforms it into a clean, analysis-ready dataset.

---

## ✨ What It Fixes

| Problem | Solution |
|---------|---------|
| Duplicate rows | Removed exact & fuzzy duplicates |
| Inconsistent casing (JOHN, john) | Standardized to Title Case |
| Mixed date formats (DD/MM/YYYY & YYYY-MM-DD) | Unified to YYYY-MM-DD |
| Country abbreviations (USA, UK) | Expanded to full names |
| Missing prices | Filled with category median |
| Missing quantities | Filled with default value of 1 |
| Extra whitespace in columns | Stripped from all fields |
| Invalid/empty critical rows | Dropped cleanly |

---

## ✨ Features

- ✅ **7-step automated cleaning pipeline**
- ✅ Removes exact and fuzzy duplicate records
- ✅ Fixes inconsistent text casing and whitespace
- ✅ Standardizes mixed date formats
- ✅ Handles missing values intelligently
- ✅ Adds calculated columns (Total Value, Order Month)
- ✅ Validates final data integrity
- ✅ Auto-generates a **cleaning report** (.txt)
- ✅ Exports clean structured CSV ready for analysis

---

## 🛠️ Tools & Technologies

| Tool | Purpose |
|------|---------|
| Python | Core programming language |
| Pandas | Data cleaning & transformation |
| NumPy | Numerical operations |

---

## 📁 Project Structure

```
data-cleaning-script/
│
├── data_cleaner.py           # Main cleaning script
├── raw_ecommerce_data.csv    # Input — messy raw dataset
├── cleaned_ecommerce_data.csv# Output — clean structured data
├── cleaning_report.txt       # Auto-generated cleaning report
├── screenshots/              # Before & after screenshots
└── README.md                 # Project documentation
```

---

## ⚙️ How to Run

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/data-cleaning-script.git
cd data-cleaning-script
```

**2. Install dependencies**
```bash
pip install pandas numpy
```

**3. Run the script**
```bash
python data_cleaner.py
```

**4. Check your outputs:**
- `cleaned_ecommerce_data.csv` — clean dataset
- `cleaning_report.txt` — full log of all changes made

---

## 📊 Before vs After

| | Before | After |
|--|--------|-------|
| Rows | 25 | 17 |
| Duplicates | 8 | 0 |
| Missing values | 6 | 0 |
| Date formats | Mixed | Unified |
| Country names | Inconsistent | Standardized |
| Extra columns | None | Total_Value, Order_Month |

---

## 📈 Auto-Generated Summary

```
Total revenue        : $1,230.12
Avg order value      : $72.36
Top category         : Electronics
Top country          : United States
Completed orders     : 13
```

---

## 🚀 Skills Demonstrated

- Data cleaning & transformation with Pandas
- Handling missing values intelligently
- Deduplication (exact & fuzzy)
- Date format standardization
- Automated reporting
- Clean, modular Python code

---

## 📬 Contact

Available for freelance data cleaning & automation projects on [Upwork](https://www.upwork.com)!
