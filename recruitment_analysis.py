import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from faker import Faker
import random
from datetime import datetime, timedelta

def generate_recruitment_data():
    """
    Generates mock data for recruitment funnel and user activity.
    Returns:
        df_applications (pd.DataFrame): 1000 applicants with statuses.
        df_activity (pd.DataFrame): 5000 login events Jan-Apr.
    """
    fake = Faker()
    Faker.seed(42)
    np.random.seed(42)
    random.seed(42)

    num_applicants = 1000
    user_ids = list(range(1, num_applicants + 1))
    
    stages = ['Sign Up', 'Profile Uploaded', 'Applied', 'Interview', 'Offer', 'Hired']
    stage_probs = [0.35, 0.25, 0.20, 0.10, 0.07, 0.03] 
    
    statuses = np.random.choice(stages, size=num_applicants, p=stage_probs)
    
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=random.randint(0, 90)) for _ in range(num_applicants)]
    
    df_applications = pd.DataFrame({
        'user_id': user_ids,
        'application_date': dates,
        'current_status': statuses
    })

    num_logins = 5000
    activity_data = []
    
    for _ in range(num_logins):
        uid = random.choice(user_ids)
        days_offset = random.randint(0, 120) 
        login_date = datetime(2024, 1, 1) + timedelta(days=days_offset)
        activity_data.append({'user_id': uid, 'login_date': login_date})
        
    df_activity = pd.DataFrame(activity_data)
    
    return df_applications, df_activity

def perform_sql_funnel_analysis(df_applications):
    """
    Uses SQLite to calculate funnel conversion rates.
    """
    conn = sqlite3.connect(':memory:')
    
    df_applications.to_sql('applicant_funnel', conn, index=False)
    
    query = """
    WITH StageMapping AS (
        SELECT 1 as stage_rank, 'Sign Up' as stage_name UNION ALL
        SELECT 2, 'Profile Uploaded' UNION ALL
        SELECT 3, 'Applied' UNION ALL
        SELECT 4, 'Interview' UNION ALL
        SELECT 5, 'Offer' UNION ALL
        SELECT 6, 'Hired'
    ),
    UserRanks AS (
        SELECT 
            u.user_id,
            m.stage_rank as current_rank
        FROM applicant_funnel u
        JOIN StageMapping m ON u.current_status = m.stage_name
    ),
    FunnelCounts AS (
        SELECT 
            m.stage_name,
            m.stage_rank,
            COUNT(u.user_id) as user_count
        FROM StageMapping m
        LEFT JOIN UserRanks u ON u.current_rank >= m.stage_rank
        GROUP BY m.stage_name, m.stage_rank
    )
    SELECT 
        stage_name,
        user_count,
        100.0 * (user_count - LAG(user_count, 1, user_count) OVER (ORDER BY stage_rank)) / 
        LAG(user_count, 1, user_count) OVER (ORDER BY stage_rank) as drop_off_pct
    FROM FunnelCounts
    ORDER BY stage_rank;
    """
    
    funnel_results = pd.read_sql(query, conn)
    conn.close()
    
    return funnel_results

def perform_cohort_analysis(df_activity):
    """
    Creates a retention heatmap based on acquisition month.
    """
    df_activity['login_date'] = pd.to_datetime(df_activity['login_date'])
    
    df_activity['order_month'] = df_activity['login_date'].dt.to_period('M')
    
    cohort_group = df_activity.groupby('user_id')['order_month']
    df_activity['cohort'] = cohort_group.transform('min')
    
    df_cohort = df_activity.groupby(['cohort', 'order_month']).agg(n_customers=('user_id', 'nunique')).reset_index()
    
    df_cohort['period_number'] = (df_cohort.order_month - df_cohort.cohort).apply(lambda x: x.n)
    
    cohort_pivot = df_cohort.pivot_table(index='cohort', columns='period_number', values='n_customers')
    
    cohort_size = cohort_pivot.iloc[:, 0]
    retention_matrix = cohort_pivot.divide(cohort_size, axis=0) * 100
    
    plt.figure(figsize=(10, 6))
    plt.title('User Retention by Cohort (Jan-Apr 2024)', fontsize=16)
    sns.heatmap(retention_matrix, annot=True, fmt='.1f', cmap='YlGnBu', vmin=0, vmax=50)
    plt.ylabel('Cohort Month')
    plt.xlabel('Months Since Acquisition')
    plt.yticks(rotation=0)
    
    return retention_matrix

def print_executive_report(funnel_df, retention_matrix):
    print("\n" + "="*50)
    print("EXECUTIVE SUMMARY REPORT")
    print("="*50)
    
    max_drop = funnel_df['drop_off_pct'].min()
    worst_stage_row = funnel_df.loc[funnel_df['drop_off_pct'] == max_drop].iloc[0]
    
    print("\n1. FUNNEL ANALYSIS")
    print("-" * 30)
    print(funnel_df.to_string(index=False))
    print(f"\n[Key Insight]: The largest drop-off ({worst_stage_row['drop_off_pct']:.1f}%) occurs at the '{worst_stage_row['stage_name']}' stage.")
    print("[Recommendation]: Investigate technical friction in this step or review qualification criteria.")
    
    if 1 in retention_matrix.columns:
        avg_retention_m1 = retention_matrix[1].mean()
        print("\n2. COHORT RETENTION")
        print("-" * 30)
        print(f"Average Month 1 Retention: {avg_retention_m1:.1f}%")
        if avg_retention_m1 < 20:
            print("[Insight]: Retention is critically low. Users are not finding immediate value.")
        else:
            print("[Insight]: Healthy initial retention, indicating strong product-market fit.")
    else:
        print("\n[Insight]: Not enough data for Month 1 retention yet.")

if __name__ == "__main__":
    print("Generating Mock Data...")
    df_app, df_act = generate_recruitment_data()
    
    print("Running SQL Funnel Analysis...")
    funnel_results = perform_sql_funnel_analysis(df_app)
    
    print("Running Cohort Analysis & Plotting...")
    retention_mat = perform_cohort_analysis(df_act)
    
    print_executive_report(funnel_results, retention_mat)
    
    print("\nSaving Cohort Heatmap to cohort_analysis.png...")
    plt.savefig('cohort_analysis.png')
    print("Plot saved.")
