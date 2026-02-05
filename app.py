import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ======================
# PAGE SETUP
# ======================
st.set_page_config(
    page_title="Global YouTube Analytics Dashboard",
    layout="wide"
)

# ======================
# LOAD DATA
# ======================
df = pd.read_csv("Global YouTube Statistics (1).csv", encoding="latin1")
df.columns = df.columns.str.strip().str.lower()

# ======================
# TITLE & CONTEXT
# ======================
st.title("📊 Global YouTube Analytics Dashboard")

st.markdown(
    """
    **Objective:**  
    This dashboard explores global YouTube channel statistics to understand how
    subscribers, views, content categories, and geographic regions influence
    channel performance.
    """
)

# ======================
# FILTERS
# ======================
st.sidebar.header("🔎 Filters")

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
# KPI SECTION
# ======================
st.markdown("## 📌 Dataset Overview")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Channels", filtered_df.shape[0])
k2.metric("Avg Subscribers", f"{int(filtered_df['subscribers'].mean()):,}")
k3.metric("Avg Views", f"{int(filtered_df['video views'].mean()):,}")
k4.metric("No. of Categories", filtered_df["category"].nunique())

st.markdown(
    "📌 **Insight:** The KPIs summarize the overall scale and diversity of YouTube channels in the selected data."
)

st.divider()

# ======================
# UNIVARIATE ANALYSIS
# ======================
st.markdown("## 📈 Univariate Analysis")

st.subheader("Distribution of Subscribers")

fig1, ax1 = plt.subplots()
ax1.hist(filtered_df["subscribers"], bins=30)
ax1.set_xlabel("Subscribers")
ax1.set_ylabel("Number of Channels")
st.pyplot(fig1)

st.markdown(
    "📌 **Insight:** Subscriber distribution is highly right-skewed, indicating that a small number of channels dominate the platform."
)

# ======================
# BIVARIATE ANALYSIS
# ======================
st.divider()
st.markdown("## 🔗 Bivariate Analysis")

st.subheader("Subscribers vs Views (Log Scale)")

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
    "📌 **Insight:** There is a strong positive relationship between subscribers and views, "
    "suggesting that subscriber base is a key driver of viewership."
)

# ======================
# MULTIVARIATE ANALYSIS
# ======================
st.divider()
st.markdown("## 🧩 Multivariate Analysis")

st.subheader("Average Subscribers by Category")

cat_stats = (
    filtered_df
    .groupby("category")["subscribers"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

fig3, ax3 = plt.subplots()
cat_stats.plot(kind="bar", ax=ax3)
ax3.set_xlabel("Category")
ax3.set_ylabel("Average Subscribers")
st.pyplot(fig3)

st.markdown(
    "📌 **Insight:** Entertainment-related categories attract significantly higher average subscribers than informational categories."
)

# ======================
# COUNTRY ANALYSIS
# ======================
st.divider()
st.markdown("## 🌍 Geographic Analysis")

st.subheader("Top Countries by Number of Channels")

country_count = filtered_df["country"].value_counts().head(10)

fig4, ax4 = plt.subplots()
country_count.plot(kind="bar", ax=ax4)
ax4.set_xlabel("Country")
ax4.set_ylabel("Number of Channels")
st.pyplot(fig4)

st.markdown(
    "📌 **Insight:** A small number of countries dominate YouTube content creation, "
    "indicating geographic concentration of top channels."
)

# ======================
# CONCLUSION
# ======================
st.divider()
st.markdown("## ✅ Key Takeaways")

st.markdown(
    """
    - YouTube channel performance is **highly skewed**, with a few channels dominating subscribers and views.  
    - Subscriber count is a strong predictor of total views.  
    - Content category and geographic location play a significant role in channel success.  
    """
)

st.caption("Dashboard built using Streamlit | Data Source: Global YouTube Statistics")
