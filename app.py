import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="APeats Analytics Dashboard",
    layout="wide"
)

df = pd.read_csv("orders.csv")
df["Date"] = pd.to_datetime(df["Date"])

st.title("📊 APeats Business Intelligence Dashboard")
st.caption(
    "Prototype built using Python, Pandas, Streamlit and Plotly"
)
from datetime import datetime
st.write(
    f"Last Updated: {datetime.now().strftime('%d %B %Y %I:%M %p')}"
)

st.subheader("Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Orders", len(df))

with col2:
    st.metric("Total Revenue", f"₹{df['Amount'].sum():,.0f}")

with col3:
    st.metric("Active Customers", df["Customer_ID"].nunique())

with col4:
    st.metric("Partner Restaurants", df["Restaurant"].nunique())


st.subheader("Revenue Trend")
revenue_df = (
    df.groupby("Date")["Amount"]
    .sum()
    .reset_index()
)

fig = px.line(
    revenue_df,
    x="Date",
    y="Amount",
    title="Daily Revenue"
)
fig.update_traces(
    line_color="#D17009"
)
fig.update_layout(
    plot_bgcolor="#F0F2F6",
    paper_bgcolor="#F0F2F6"
)

st.subheader("Peak Ordering Hours")
hour_df = (
    df.groupby("Hour")
    .size()
    .reset_index(name="Orders")
)

fig2 = px.bar(
    hour_df,
    x="Hour",
    y="Orders",
    title="Orders by Hour"
)
fig2.update_traces(
    marker_color="#D17009"
)
fig2.update_layout(
    plot_bgcolor="#F0F2F6",
    paper_bgcolor="#F0F2F6"
)

st.subheader("Top Selling Items")
item_df = (
    df.groupby("Item")
    .size()
    .reset_index(name="Orders")
    .sort_values("Orders", ascending=False)
)

fig3 = px.bar(
    item_df.head(10),
    x="Item",
    y="Orders",
    title="Top Selling Items"
)
fig3.update_traces(
    marker_color="#D17009"
)
fig3.update_layout(
    plot_bgcolor="#F0F2F6",
    paper_bgcolor="#F0F2F6"
)

st.subheader("Top Restaurants")
restaurant_df = (
    df.groupby("Restaurant")["Amount"]
    .sum()
    .reset_index()
    .sort_values("Amount", ascending=False)
)

fig4 = px.bar(
    restaurant_df,
    x="Restaurant",
    y="Amount",
    title="Revenue by Restaurant"
)
fig4.update_traces(
    marker_color="#D17009"
)
fig4.update_layout(
    plot_bgcolor="#F0F2F6",
    paper_bgcolor="#F0F2F6"
)

# Row 1
colA, colB = st.columns(2)

with colA:
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

with colB:
    st.plotly_chart(
        fig2,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# Row 2
colC, colD = st.columns(2)

with colC:
    st.plotly_chart(
        fig3,
        use_container_width=True,
        config={"displayModeBar": False}
    )

with colD:
    st.plotly_chart(
        fig4,
        use_container_width=True,
        config={"displayModeBar": False}
    )

st.divider()
st.subheader("📊 Business Insights")
top_item = item_df.iloc[0]["Item"]

top_restaurant = restaurant_df.iloc[0]["Restaurant"]

peak_hour = hour_df.loc[
    hour_df["Orders"].idxmax(),
    "Hour"
]

st.info(
    f"""
🔥 Peak ordering hour: {peak_hour}:00

🍜 Most popular item: {top_item}

🏪 Highest revenue restaurant: {top_restaurant}

💰 Total revenue generated: ₹{df['Amount'].sum():,.0f}
"""
)