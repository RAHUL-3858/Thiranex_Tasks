import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    page_icon="🧑‍🤝‍🧑",
    layout="wide"
)

# ---------------------------------------------------
# Title
# ---------------------------------------------------

st.title("🧑‍🤝‍🧑 Customer Segmentation Dashboard")
st.markdown("Analyze customer behavior using clustering techniques")

# ---------------------------------------------------
# Load Dataset
# ---------------------------------------------------

df = pd.read_csv("customer_data.csv")

# ---------------------------------------------------
# Select Features for Clustering
# ---------------------------------------------------

X = df[['Annual Income', 'Spending Score']]

# ---------------------------------------------------
# Apply KMeans Clustering
# ---------------------------------------------------

kmeans = KMeans(n_clusters=5, random_state=42)

df['Cluster'] = kmeans.fit_predict(X)

# ---------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------

st.sidebar.header("Filter Customers")

gender_filter = st.sidebar.multiselect(
    "Select Gender",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

filtered_df = df[
    df['Gender'].isin(gender_filter)
]

# ---------------------------------------------------
# KPI Metrics
# ---------------------------------------------------

total_customers = filtered_df.shape[0]
average_income = filtered_df['Annual Income'].mean()
average_score = filtered_df['Spending Score'].mean()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Customers", total_customers)

with col2:
    st.metric("Average Income", f"${average_income:.2f}k")

with col3:
    st.metric("Average Spending Score", f"{average_score:.2f}")

st.markdown("---")

# ---------------------------------------------------
# Scatter Plot for Clusters
# ---------------------------------------------------

cluster_chart = px.scatter(
    filtered_df,
    x='Annual Income',
    y='Spending Score',
    color='Cluster',
    hover_data=['CustomerID', 'Age', 'Gender'],
    title='Customer Segments'
)

st.plotly_chart(cluster_chart, use_container_width=True)

# ---------------------------------------------------
# Age Distribution
# ---------------------------------------------------

age_chart = px.histogram(
    filtered_df,
    x='Age',
    color='Gender',
    title='Age Distribution'
)

st.plotly_chart(age_chart, use_container_width=True)

# ---------------------------------------------------
# Cluster Count
# ---------------------------------------------------

cluster_count = filtered_df['Cluster'].value_counts().reset_index()

cluster_count.columns = ['Cluster', 'Customers']

bar_chart = px.bar(
    cluster_count,
    x='Cluster',
    y='Customers',
    color='Cluster',
    title='Customers per Segment'
)

st.plotly_chart(bar_chart, use_container_width=True)

# ---------------------------------------------------
# Data Table
# ---------------------------------------------------

st.subheader("Customer Data")

st.dataframe(filtered_df)

# ---------------------------------------------------
# Download Button
# ---------------------------------------------------

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Segmented Data",
    data=csv,
    file_name='customer_segments.csv',
    mime='text/csv'
)

# ---------------------------------------------------
# Footer
# ---------------------------------------------------

st.markdown("---")
st.markdown("Developed by Rahul | Customer Segmentation Project")