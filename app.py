import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------
# Dashboard Title
# ---------------------------------------------------

st.title("📊 Sales & Revenue Analysis Dashboard")
st.markdown("Analyze sales, revenue, and profit data interactively")

# ---------------------------------------------------
# Load Dataset
# ---------------------------------------------------

df = pd.read_csv("sales_data.csv")

# Convert Date Column to Datetime
df['Date'] = pd.to_datetime(df['Date'])

# ---------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------

st.sidebar.header("Filter Data")

region_filter = st.sidebar.multiselect(
    "Select Region",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

category_filter = st.sidebar.multiselect(
    "Select Category",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

# ---------------------------------------------------
# Apply Filters
# ---------------------------------------------------

filtered_df = df[
    (df['Region'].isin(region_filter)) &
    (df['Category'].isin(category_filter))
]

# ---------------------------------------------------
# KPI Calculations
# ---------------------------------------------------

total_revenue = filtered_df['Revenue'].sum()
total_profit = filtered_df['Profit'].sum()
total_units = filtered_df['Units Sold'].sum()

# ---------------------------------------------------
# KPI Cards
# ---------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Revenue", f"₹{total_revenue:,.0f}")

with col2:
    st.metric("Total Profit", f"₹{total_profit:,.0f}")

with col3:
    st.metric("Units Sold", f"{total_units}")

st.markdown("---")

# ---------------------------------------------------
# Revenue by Region Chart
# ---------------------------------------------------

region_data = filtered_df.groupby('Region')['Revenue'].sum().reset_index()

region_chart = px.bar(
    region_data,
    x='Region',
    y='Revenue',
    color='Region',
    title='Revenue by Region'
)

# ---------------------------------------------------
# Revenue Trend Chart
# ---------------------------------------------------

trend_data = filtered_df.groupby('Date')['Revenue'].sum().reset_index()

trend_chart = px.line(
    trend_data,
    x='Date',
    y='Revenue',
    markers=True,
    title='Revenue Trend Over Time'
)

# ---------------------------------------------------
# Product Revenue Pie Chart
# ---------------------------------------------------

product_data = filtered_df.groupby('Product')['Revenue'].sum().reset_index()

product_chart = px.pie(
    product_data,
    names='Product',
    values='Revenue',
    title='Revenue Share by Product'
)

# ---------------------------------------------------
# Charts Layout
# ---------------------------------------------------

col4, col5 = st.columns(2)

with col4:
    st.plotly_chart(region_chart, use_container_width=True)

with col5:
    st.plotly_chart(trend_chart, use_container_width=True)

st.plotly_chart(product_chart, use_container_width=True)

# ---------------------------------------------------
# Sales Data Table
# ---------------------------------------------------

st.subheader("Sales Data Table")

st.dataframe(filtered_df)

# ---------------------------------------------------
# Download Filtered Data
# ---------------------------------------------------

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name='filtered_sales_data.csv',
    mime='text/csv'
)