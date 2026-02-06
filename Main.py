import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("hospital_patients.csv")

# Date processing
df['Admission_Date'] = pd.to_datetime(df['Admission_Date'])
df['Month'] = df['Admission_Date'].dt.to_period('M')
df['Day_Type'] = df['Admission_Date'].dt.dayofweek.apply(
    lambda x: 'Weekend' if x >= 5 else 'Weekday'
)

# ------------------ ANALYSIS ------------------

# Total hospital revenue
total_sum = df['Treatment_Cost'].sum()
print("Total Revenue:", total_sum)

# Revenue by Department
dept_revenue = df.groupby('Department')['Treatment_Cost'].agg(['sum', 'mean'])
print("\nRevenue by Department:\n", dept_revenue)

# Monthly Revenue
monthly_sum = df.groupby('Month')['Treatment_Cost'].sum()
print("\nMonthly Revenue:\n", monthly_sum)

# Age Grouping
bins = [0, 10, 19, 49, 69, 100]
labels = ['0-10', '11-19', '20-49', '50-69', '70+']

df['Age_Group'] = pd.cut(
    df['Age'],
    bins=bins,
    labels=labels,
    include_lowest=True
)

age_spending_group = df.groupby('Age_Group')['Treatment_Cost'].sum()
print("\nSpending by Age Group:\n", age_spending_group)

# Gender Spending
gender_spending = df.groupby('Gender')['Treatment_Cost'].sum()
print("\nSpending by Gender:\n", gender_spending)

# Top 10 High-Cost Patients
top_10 = df.sort_values(by='Treatment_Cost', ascending=False).head(10)
print("\nTop 10 High-Cost Patients:\n",
      top_10[['Patient_ID', 'Department', 'Age', 'Treatment_Cost']])

# Best Month
best_month = monthly_sum.idxmax()
print("\nBest Month:", best_month)

# Weekday vs Weekend Revenue
weekday_weekend_revenue = df.groupby('Day_Type')['Treatment_Cost'].sum()
print("\nRevenue by Day Type:\n", weekday_weekend_revenue)

# ------------------ VISUALIZATION (MATPLOTLIB ONLY) ------------------

plt.style.use('ggplot')

# Total Revenue
plt.figure(figsize=(6,4))
plt.bar(['Total Revenue'], [total_sum])
plt.title("Total Revenue")
plt.ylabel("Revenue")
plt.show()

# Revenue by Department
plt.figure(figsize=(10,5))
plt.bar(dept_revenue.index, dept_revenue['sum'])
plt.title("Revenue by Department")
plt.xlabel("Department")
plt.ylabel("Total Revenue")
plt.xticks(rotation=45)
plt.show()

# Monthly Revenue Trend
plt.figure(figsize=(10,5))
plt.plot(monthly_sum.index.astype(str), monthly_sum.values, marker='o')
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.show()

# Age Group Spending
plt.figure(figsize=(8,5))
plt.bar(age_spending_group.index.astype(str), age_spending_group.values)
plt.title("Spending by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Revenue")
plt.show()

# Gender Spending
plt.figure(figsize=(6,4))
plt.bar(gender_spending.index, gender_spending.values)
plt.title("Spending by Gender")
plt.ylabel("Revenue")
plt.show()

# Top 10 Patients
plt.figure(figsize=(10,5))
plt.bar(top_10['Patient_ID'], top_10['Treatment_Cost'])
plt.title("Top 10 High-Cost Patients")
plt.xlabel("Patient ID")
plt.ylabel("Treatment Cost")
plt.xticks(rotation=45)
plt.show()

# Weekday vs Weekend Revenue
plt.figure(figsize=(6,4))
plt.bar(weekday_weekend_revenue.index, weekday_weekend_revenue.values)
plt.title("Weekday vs Weekend Revenue")
plt.ylabel("Revenue")
plt.show()
