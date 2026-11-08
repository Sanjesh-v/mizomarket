import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==========================================
# MIZOMARKET - VERSION 1.0 MVP
# ==========================================

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

st.set_page_config(
    page_title="MizoMarket",
    page_icon="🌱",
    layout="wide"
)

# ------------------------------------------
# DATA LOADING
# ------------------------------------------

@st.cache_data
def load_csv(filename):
    path = DATA / filename
    if not path.exists():
        raise FileNotFoundError(f"Missing dataset: {path}")
    return pd.read_csv(path)

supply = load_csv("crop_supply.csv")
prices = load_csv("market_prices.csv")
buyers = load_csv("buyers.csv")

# ------------------------------------------
# BASIC VALIDATION
# ------------------------------------------

required_supply = {
    "crop", "village", "quantity_mt", "harvest_season"
}
required_prices = {
    "crop", "market", "price_per_kg", "date", "source"
}
required_buyers = {
    "buyer_name", "buyer_type", "interested_crop", "location"
}

if not required_supply.issubset(supply.columns):
    st.error("Crop supply dataset has missing columns.")
    st.stop()

if not required_prices.issubset(prices.columns):
    st.error("Market price dataset has missing columns.")
    st.stop()

if not required_buyers.issubset(buyers.columns):
    st.error("Buyer dataset has missing columns.")
    st.stop()

# ------------------------------------------
# STYLING
# ------------------------------------------

st.markdown("""
<style>
h1, h2, h3 {
    color: #214d36;
}
[data-testid="stSidebar"] {
    background-color: #edf3ec;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------
# HEADER
# ------------------------------------------

st.title("🌱 MizoMarket")
st.subheader(
    "Agricultural Market Intelligence Platform for Mizoram"
)

st.write(
    "A research-led initiative exploring agricultural supply, "
    "market information and producer-buyer linkages."
)

st.warning(
    "DEMONSTRATION MODE: All included records are synthetic. "
    "They are not verified farmer listings, market prices or "
    "buyer commitments."
)

# ------------------------------------------
# NAVIGATION
# ------------------------------------------

st.sidebar.title("🌱 MizoMarket")
st.sidebar.caption("Rural Market Intelligence")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Crop Supply",
        "Price Intelligence",
        "Buyer Discovery",
        "Market Insights",
        "About & Methodology"
    ]
)

# ------------------------------------------
# DASHBOARD
# ------------------------------------------

if page == "Dashboard":

    st.header("Agricultural Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Crops Tracked", supply["crop"].nunique())
    col2.metric("Villages Represented", supply["village"].nunique())
    col3.metric(
        "Sample Supply",
        f'{supply["quantity_mt"].sum():.1f} MT'
    )
    col4.metric("Sample Buyer Profiles", len(buyers))

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Crop Supply")

        crop_supply = (
            supply.groupby("crop", as_index=False)
            ["quantity_mt"].sum()
        )

        fig = px.bar(
            crop_supply,
            x="crop",
            y="quantity_mt",
            color="crop",
            title="Illustrative Crop Availability",
            labels={
                "crop": "Crop",
                "quantity_mt": "Quantity (MT)"
            }
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Village Contribution")

        village_supply = (
            supply.groupby("village", as_index=False)
            ["quantity_mt"].sum()
        )

        fig = px.pie(
            village_supply,
            names="village",
            values="quantity_mt",
            title="Illustrative Supply Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Sample Supply Records")
    st.dataframe(supply, use_container_width=True, hide_index=True)

# ------------------------------------------
# CROP SUPPLY
# ------------------------------------------

elif page == "Crop Supply":

    st.header("Crop Supply Directory")

    crop_filter = st.multiselect(
        "Filter by crop",
        sorted(supply["crop"].unique()),
        default=sorted(supply["crop"].unique())
    )

    village_filter = st.multiselect(
        "Filter by village",
        sorted(supply["village"].unique()),
        default=sorted(supply["village"].unique())
    )

    filtered = supply[
        supply["crop"].isin(crop_filter)
        & supply["village"].isin(village_filter)
    ]

    st.metric(
        "Filtered Sample Supply",
        f'{filtered["quantity_mt"].sum():.1f} MT'
    )

    st.dataframe(filtered, use_container_width=True, hide_index=True)

# ------------------------------------------
# PRICE INTELLIGENCE
# ------------------------------------------

elif page == "Price Intelligence":

    st.header("Agricultural Price Intelligence")

    crop = st.selectbox(
        "Select crop",
        sorted(prices["crop"].unique())
    )

    selected = prices[prices["crop"] == crop]

    fig = px.bar(
        selected,
        x="market",
        y="price_per_kg",
        color="market",
        title=f"Illustrative {crop} Price Comparison",
        labels={
            "market": "Market",
            "price_per_kg": "Price (₹/kg)"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(selected, use_container_width=True, hide_index=True)

    st.caption(
        "Always check the source and observation date. "
        "These sample prices are not live market quotations."
    )

# ------------------------------------------
# BUYER DISCOVERY
# ------------------------------------------

elif page == "Buyer Discovery":

    st.header("Buyer Discovery")

    crop_filter = st.selectbox(
        "Select crop",
        ["All"] + sorted(buyers["interested_crop"].unique())
    )

    if crop_filter == "All":
        filtered = buyers.copy()
    else:
        filtered = buyers[
            buyers["interested_crop"] == crop_filter
        ]

    st.dataframe(filtered, use_container_width=True, hide_index=True)

    st.info(
        "Real buyer profiles will be added only after verification "
        "and appropriate permission."
    )

# ------------------------------------------
# MARKET INSIGHTS
# ------------------------------------------

elif page == "Market Insights":

    st.header("Market Insights")

    fig = px.bar(
        supply,
        x="village",
        y="quantity_mt",
        color="crop",
        barmode="group",
        title="Illustrative Crop Supply by Village"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Questions for Field Research")

    st.markdown("""
    - Where are agricultural producers concentrated?
    - How does crop availability vary by season?
    - What price differences exist between markets?
    - What are the requirements of potential buyers?
    - Where are aggregation and transport bottlenecks?
    """)

    st.warning(
        "These are research questions, not conclusions "
        "established by the demonstration dataset."
    )

# ------------------------------------------
# ABOUT AND METHODOLOGY
# ------------------------------------------

elif page == "About & Methodology":

    st.header("About MizoMarket")

    st.write("""
    MizoMarket is a proposed rural agricultural market intelligence
    initiative focused on Mizoram.

    It aims to investigate agricultural market-access challenges
    and explore practical ways to improve producer-buyer visibility.
    """)

    st.subheader("Research Methodology")

    st.markdown("""
    1. Secondary research using reports and government data.
    2. Farmer and producer-group consultations.
    3. Trader and processor interviews.
    4. Agricultural value-chain mapping.
    5. Prototype testing and stakeholder feedback.
    """)

    st.subheader("Proposed Research Clusters")

    st.markdown("""
    - East Lungdar - Ginger
    - Reiek - Turmeric
    - Thenzawl - Orange
    """)

    st.info(
        "Current status: Concept development and demonstration MVP. "
        "Field validation and verified market data are pending."
    )

    st.caption(
        "MizoMarket | Version 1.0 MVP | IIT Madras | "
        "New India Internship proposal"
    )
