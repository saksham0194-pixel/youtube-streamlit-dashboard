import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ======================
# PAGE SETUP
# ======================
st.set_page_config(
    page_title="Global YouTube Analytics: A Data Story",
    layout="wide"
)

# ======================
# LOAD & PREP DATA
# ======================
df = pd.read_csv("Global YouTube Statistics (1).csv", encoding="latin1")
df.columns = df.columns.str.strip().str.lower()

# ======================
# TITLE & STORY INTRO
# ======================
st.title("📊 Global YouTube Analytics: A Data Story")

st.markdown(
    """
    **Purpose of this dashboard:**  
    To understand how YouTube channel success is distributed globally and what factors
    drive subscriber growth and viewership.
    
    This dashboard tells a **data-driven story** using real-world YouTube statistics.
    """
)

# ======================
# FILTERS
# ======================
st.sidebar.header("🔎 Explore the Data")

country_filter = st.sidebar.multiselect(
    "Country",
    sorted(df["country"].dropna().unique()),
    default=sorted(df["country"].dropna().unique())
)

category_filter = st.sidebar.multiselect(
    "Category",
    sorted(df["category"].dropna().unique()),
    default=sorted(df["category"].dropna().unique())
)

filtered_df = df[
    (df["country"].isin(country_filter)) &
    (df["category"].isin(category_filter))
]

# ======================
# CHAPTER 1: SCALE & INEQUALITY
# ======================
st.markdown("## 📌 Chapter 1: How Unequal Is YouTube?")

k1, k2, k3 = st.columns(3)
k1.metric("Total Channels", filtered_df.shape[0])
k2.metric("Mean Subscribers", f"{int(filtered_df['subscribers'].mean()):,}")
k3.metric("Median Subscribers", f"{int(filtered_df['subscribers'].median()):,}")

st.markdown(
    """
    📖 **Story:**  
    The large gap between mean and median subscribers indicates **extreme inequality**.
    A small number of channels dominate the platform.
    """
)

fig1, ax1 = plt.subplots()
ax1.hist(filtered_df["subscribers"], bins=40)
ax1.set_xlabel("Subscribers")
ax1.set_ylabel("Number of Channels")
st.pyplot(fig1)

st.markdown(
    "📌 **Insight:** Most channels have relatively few subscribers, while a tiny fraction captures massive audiences."
)

# ======================
# CHAPTER 2: DOMINANCE ANALYSIS
# ======================
st.divider()
st.markdown("## 📈 Chapter 2: Who Dominates the Platform?")

top_1 = np.percentile(filtered_df["subscribers"], 99)
top_10 = np.percentile(filtered_df["subscribers"], 90)

st.markdown(
    f"""
    - Top **1%** of channels have more than **{int(top_1):,} subscribers**  
    - Top **10%** of channels have more than **{int(top_10):,} subscribers**
    """
)

st.markdown(
    "📌 **Insight:** YouTube follows a **power-law distribution**, common in digital platforms."
)

# ======================
# CHAPTER 3: SUBSCRIBERS VS VIEWS
# ======================
st.divider()
st.markdown("## 🔗 Chapter 3: Do Subscribers Really Matter?")

plot_df = filtered_df[
    (filtered_df["subscribers"] > 0) &
    (filtered_df["video views"] > 0)
]

fig2, ax2 = plt.subplots()
ax2.scatter(plot_df["subscribers"], plot_df["video views"], alpha=0.6)
ax2.set_xscale("log")
ax2.set_yscale("log")
ax2.set_xlabel("Subscribers (log scale)")
ax2.set_ylabel("Views (log scale)")
st.pyplot(fig2)

st.markdown(
    """
    📌 **Insight:**  
    The near-linear pattern on a log–log scale confirms that **subscriber growth strongly drives total views**.
    """
)

# ======================
# CHAPTER 4: CATEGORY EFFICIENCY
# ======================
st.divider()
st.markdown("## 🎬 Chapter 4: Which Categories Perform Better?")

filtered_df["views_per_sub"] = filtered_df["video views"] / filtered_df["subscribers"]

cat_eff = (
    filtered_df
    .groupby("category")["views_per_sub"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

fig3, ax3 = plt.subplots()
cat_eff.plot(kind="bar", ax=ax3)
ax3.set_xlabel("Category")
ax3.set_ylabel("Views per Subscriber")
st.pyplot(fig3)

st.markdown(
    """
    📌 **Insight:**  
    Some categories generate disproportionately high views relative to their subscriber base,
    indicating **higher engagement efficiency**.
    """
)

# ======================
# CHAPTER 5: GEOGRAPHIC CONCENTRATION
# ======================
st.divider()
st.markdown("## 🌍 Chapter 5: Where Does Content Come From?")

country_count = filtered_df["country"].value_counts().head(10)

fig4, ax4 = plt.subplots()
country_count.plot(kind="bar", ax=ax4)
ax4.set_xlabel("Country")
ax4.set_ylabel("Number of Channels")
st.pyplot(fig4)

st.markdown(
    """
    📌 **Insight:**  
    YouTube content creation is geographically concentrated, with a few countries
    dominating the global creator ecosystem.
    """
)

# ======================
# FINAL: RECOMMENDATIONS
# ======================
st.divider()
st.markdown("## ✅ Recommendations & Takeaways")

st.markdown(
    """
    **For new creators:**  
    - Focus on high-engagement categories rather than chasing subscriber count alone.  
    - Early subscriber growth is crucial due to compounding visibility effects.

    **For platforms & marketers:**  
    - Algorithmic exposure reinforces inequality — discovery tools for small creators matter.  
    - Category-level engagement metrics can guide better content promotion strategies.

    **Overall conclusion:**  
    YouTube is a winner-takes-most platform where strategic positioning matters as much as content quality.
    """
)

st.caption("Story-driven dashboard built using Streamlit | Data Source: Global YouTube Statistics")
