import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Global YouTube Statistics Dashboard", layout="wide")

# Load dataset
df = pd.read_csv("Global YouTube Statistics (1).csv", encoding="latin1")

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

# 🔎 DEBUG: show columns (temporary)
st.write("### Dataset Columns")
st.write(df.columns.tolist())

st.title("📊 Global YouTube Statistics Dashboard")

st.write(
    "This dashboard analyzes global YouTube channel statistics including "
    "subscribers, views, categories, and countries."
)

# Sidebar filters
st.sidebar.header("Filters")

country_filter = st.sidebar.multiselect(
    "Select Country",
    df["country"].dropna().unique(),
    default=df["country"].dropna().unique()
)

category_filter = st.sidebar.multiselect(
    "Select Category",
    df["category"].dropna().unique(),
    default=df["category"].dropna().unique()
)

filtered_df = df[
    (df["country"].isin(country_filter)) &
    (df["category"].isin(category_filter))
]

# KPIs (SAFE ones only)
st.markdown("## 📌 Key Metrics")
