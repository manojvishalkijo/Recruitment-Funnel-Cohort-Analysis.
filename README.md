# 📊 Recruitment Platform Funnel & Cohort Analysis

### 🚀 Project Overview
This project focuses on **Product & HR Analytics** by analyzing user behavior on a recruitment platform. It aims to answer two critical business questions:
1.  **Where are we losing candidates?** (Funnel Analysis)
2.  **Are users coming back after signing up?** (Cohort Retention Analysis)

By simulating a real-world dataset of 1,000+ job seekers and 5,000+ login sessions, this project demonstrates how to identify bottlenecks in the application process and track long-term user engagement using **SQL** and **Python**.

### 🔍 Key Features

#### 1. Funnel Analysis (SQL)
* **Objective:** Track the conversion rate of candidates from "Sign Up" → "Profile Upload" → "Interview" → "Hired".
* **Method:** Utilized **Complex SQL Queries** (aggregations and window functions) to calculate the drop-off percentage at each specific stage of the recruitment pipeline.
* **Business Value:** Identifies friction points (e.g., a complex resume upload form) that cause high candidate abandonment.

#### 2. Cohort Analysis (Python & Pandas)
* **Objective:** Measure user retention over time (Monthly Active Users).
* **Method:** Grouped users by their "Acquisition Month" and tracked their activity over subsequent months (`Month +1`, `Month +2`, etc.).
* **Visualization:** Generated a **Seaborn Heatmap** to visually represent churn and retention trends, making it easy to spot weak cohorts.

#### 3. Automated Data Pipeline
* Built a custom **ETL script** using `Faker` to generate realistic mock data, ensuring the analysis is reproducible and robust without relying on sensitive proprietary data.

### 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Data Analysis:** Pandas, NumPy
* **Database:** SQLite3 (SQL)
* **Visualization:** Seaborn, Matplotlib
* **Concepts:** A/B Testing Metrics, Churn Analysis, Conversion Rate Optimization (CRO)


<img width="1123" height="677" alt="image" src="https://github.com/user-attachments/assets/a809c37f-68a8-4398-9998-856a8dab3a44" />
