import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Global YouTube Statistics Dashboard", layout="wide")

# Load dataset
df = pd.read_csv("Global YouTube Statistics (1).csv", encoding="latin1")


# Title
st.title("📊 Global YouTube Statistics Dashboard")

st.write(
    "This dashboard explores global YouTube channel statistics "
    "to understand patterns in subscribers, views, and content categories."
)

# Sidebar filters
st.sidebar.header("Filters")

country_filter = st.sidebar.multiselect(
    "Select Country",
    df["Country"].dropna().unique(),
    default=df["Country"].dropna().unique()
)

category_filter = st.sidebar.multiselect(
    "Select Category",
    df["Category"].dropna().unique(),
    default=df["Category"].dropna().unique()
)

filtered_df = df[
    (df["Country"].isin(country_filter)) &
    (df["Category"].isin(category_filter))
]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Channels", filtered_df.shape[0])
col2.metric("Average Subscribers", int(filtered_df["Subscribers"].mean()))
col3.metric("Average Views", int(filtered_df["Views"].mean()))

st.divider()

# Top channels
st.subheader("Top 10 Channels by Subscribers")
top_channels = filtered_df.sort_values("Subscribers", ascending=False).head(10)

fig1, ax1 = plt.subplots()
ax1.barh(top_channels["Youtuber"], top_channels["Subscribers"])
ax1.invert_yaxis()
ax1.set_xlabel("Subscribers")
ax1.set_ylabel("Channel")
st.pyplot(fig1)

# Subscribers vs Views
st.subheader("Subscribers vs Views")
fig2, ax2 = plt.subplots()
ax2.scatter(filtered_df["Subscribers"], filtered_df["Views"])
ax2.set_xlabel("Subscribers")
ax2.set_ylabel("Views")
st.pyplot(fig2)

# Category distribution
st.subheader("Channels by Category")
cat_count = filtered_df["Category"].value_counts()

fig3, ax3 = plt.subplots()
cat_count.plot(kind="bar", ax=ax3)
ax3.set_xlabel("Category")
ax3.set_ylabel("Number of Channels")
st.pyplot(fig3)

# Country distribution
st.subheader("Top Countries by Number of Channels")
country_count = filtered_df["Country"].value_counts().head(10)

fig4, ax4 = plt.subplots()
country_count.plot(kind="bar", ax=ax4)
ax4.set_xlabel("Country")
ax4.set_ylabel("Number of Channels")
st.pyplot(fig4)
