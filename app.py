import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Page setup
st.set_page_config(
    page_title="Global YouTube Statistics Dashboard",
    layout="wide"
)

# Load dataset
df = pd.read_csv("Global YouTube Statistics (1).csv", encoding="latin1")

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

# Title & intro
st.title("📊 Global YouTube Statistics Dashboard")
st.markdown(
    """
    This interactive dashboard analyzes global YouTube channel data to uncover
    patterns in subscriber growth, viewership, content categories, and geographic distribution.
    """
)

# Sidebar filters
st.sidebar.header("🔎 Filters")

country_filter = st.sidebar.multiselect(
    "Select Country",
    sorted(df["country"].dropna().unique()),
    default=sorted(df["country"].dropna().unique())
)

category_filter = st.sidebar.multiselect(
    "Select Category",
    sorted(df["category"].dropna().unique()),
    default=sorted(df["category"].dropna().unique())
)
