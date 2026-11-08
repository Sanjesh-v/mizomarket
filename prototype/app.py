
import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="MizoMarket",
    page_icon="🌱",
    layout="wide"
)

# Header
st.title("🌱 MizoMarket")
st.subheader(
    "Agricultural Market Intelligence Platform for Mizoram"
)

st.markdown(
    "Understanding agricultural supply chains and "
    "strengthening rural producer-buyer linkages."
)

st.divider()

# Sample dataset - illustrative, not actual market data
data = pd.DataFrame({
    "Crop": ["Ginger", "Turmeric", "Orange"],
    "Village": ["East Lungdar", "Reiek", "Thenzawl"],
    "Available Quantity (MT)": [12, 8, 15],
    "Indicative Price (₹/kg)": [40, 55, 30]
})

# Dashboard metrics
col1, col2, col3 = st.columns(3)

col1.metric("Crops Tracked", "3")
col2.metric("Producer Clusters", "3")
col3.metric("Sample Listings", "3")

st.divider()

# Crop availability
st.header("Agricultural Supply Overview")

fig = px.bar(
    data,
    x="Crop",
    y="Available Quantity (MT)",
    color="Crop",
    title="Illustrative Crop Availability"
)

st.plotly_chart(fig, use_container_width=True)

# Producer directory
st.header("Producer & Crop Directory")

st.dataframe(
    data,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Demonstration data only. These quantities and prices "
    "are synthetic and do not represent verified local market data."
)
