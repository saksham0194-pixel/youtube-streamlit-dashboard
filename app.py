import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Global YouTube Statistics Dashboard", layout="wide")

# Load dataset
df = pd.read_csv("Global YouTube Statistics (1).csv", encoding="latin1")

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

# Title
st.title("📊 Global YouTube Statistics Dashboard")
st.write(
    "This dashboard analyzes global YouTube channel statistics to understand "
    "patterns in subscribers, views, content categories, and countries."
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

filtered_df = df[
    (df["country"].isin(country_filter)) &
    (df["category"].isin(category_filter))
]

# =====================
# KPI SECTION
# =====================
st.markdown("## 📌 Key Metrics")

k1, k2, k3 = st.columns(3)

k1.metric("Total Channels", filtered_df.shape[0])
k2.metric("Average Subscribers", int(filtered_df["subscribers"].mean()))
k3.metric("Average Views", int(filtered_df["video views"].mean()))

st.divider()

# =====================
# GRAPH SECTION
# =====================

# ---- Subscribers vs Views (LOG SAFE) ----
st.subheader("Subscribers vs Views (Log Scale)")

plot_df = filtered_df[
    (filtered_df["subscribers"] > 0) &
    (filtered_df["video views"] > 0)
]

if plot_df.shape[0] > 0:
    fig, ax = plt.subplots()
    ax.scatter(plot_df["subscribers"], plot_df["video views"], alpha=0.6)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Subscribers (log scale)")
    ax.set_ylabel("Views (log scale)")
    st.pyplot(fig)
else:
    st.warning("Not enough positive data points to display log-scale plot.")

# ---- Category Distribution ----
st.subheader("Channels by Category")

if filtered_df.shape[0] > 0:
    cat_count = filtered_df["category"].value_counts()

    fig2, ax2 = plt.subplots()
    cat_count.plot(kind="bar", ax=ax2)
    ax2.set_xlabel("Category")
    ax2.set_ylabel("Number of Channels")
    st.pyplot(fig2)
else:
    st.warning("No data available for selected filters.")

# ---- Country Distribution ----
st.subheader("Top Countries by Number of Channels")

if filtered_df.shape[0] > 0:
    country_count = filtered_df["country"].value_counts().head(10)

    fig3, ax3 = plt.subplots()
    country_count.plot(kind="bar", ax=ax3)
    ax3.set_xlabel("Country")
    ax3.set_ylabel("Number of Channels")
    st.pyplot(fig3)
else:
    st.warning("No data available for selected filters.")
