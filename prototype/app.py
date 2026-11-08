
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------

st.set_page_config(
    page_title="MizoMarket",
    page_icon="🌱",
    layout="wide"
)

# ---------------------------------
# 2. SAMPLE DATA
# ---------------------------------

# Synthetic demonstration data.
# Replace with verified field data later.

data = pd.DataFrame({
    "Crop": ["Ginger", "Turmeric", "Orange"],
    "Village": ["East Lungdar", "Reiek", "Thenzawl"],
    "Available Quantity (MT)": [12, 8, 15],
    "Indicative Price (₹/kg)": [40, 55, 30]
})

# ---------------------------------
# 3. HEADER
# ---------------------------------

st.title("🌱 MizoMarket")

st.subheader(
    "Agricultural Market Intelligence Platform for Mizoram"
)

st.markdown(
    """
    Connecting rural producers with market intelligence,
    potential buyers and better market opportunities.
    """
)

st.divider()

# ---------------------------------
# 4. SIDEBAR
# ---------------------------------

st.sidebar.title("MizoMarket")
st.sidebar.caption("Rural Market Intelligence")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Producer Directory",
        "Price Intelligence",
        "Buyer Discovery",
        "About the Project"
    ]
)

# ---------------------------------
# 5. DASHBOARD
# ---------------------------------

if page == "Dashboard":

    st.header("Agricultural Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Crops Tracked", "3")
    col2.metric("Villages Represented", "3")
    col3.metric("Sample Listings", "3")

    st.divider()

    st.subheader("Illustrative Crop Availability")

    fig = px.bar(
        data,
        x="Crop",
        y="Available Quantity (MT)",
        color="Crop",
        title="Sample Agricultural Supply"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info(
        "Demonstration data only. Quantities and prices "
        "are synthetic and are not verified market observations."
    )

# ---------------------------------
# 6. PRODUCER DIRECTORY
# ---------------------------------

elif page == "Producer Directory":

    st.header("Producer Directory")

    village = st.selectbox(
        "Select Village",
        ["All"] + sorted(data["Village"].unique())
    )

    filtered = data.copy()

    if village != "All":
        filtered = filtered[
            filtered["Village"] == village
        ]

    st.dataframe(
        filtered[["Village", "Crop", "Available Quantity (MT)"]],
        use_container_width=True,
        hide_index=True
    )

# ---------------------------------
# 7. PRICE INTELLIGENCE
# ---------------------------------

elif page == "Price Intelligence":

    st.header("Price Intelligence")

    st.dataframe(
        data[["Crop", "Village", "Indicative Price (₹/kg)"]],
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Sample prices are illustrative, not live or verified prices."
    )

# ---------------------------------
# 8. BUYER DISCOVERY
# ---------------------------------

elif page == "Buyer Discovery":

    st.header("Buyer Discovery")

    st.write(
        "This module will eventually help producers "
        "identify potential wholesalers, processors "
        "and institutional buyers."
    )

    st.warning(
        "Buyer information will be added after stakeholder research."
    )

# ---------------------------------
# 9. ABOUT
# ---------------------------------

elif page == "About the Project":

    st.header("About MizoMarket")

    st.write(
        """
        MizoMarket is a proposed agricultural market
        intelligence initiative focused on Mizoram.

        The project aims to investigate market-access
        challenges and explore practical ways to improve
        producer-buyer linkages.
        """
    )

    st.markdown(
        "**Current stage:** Concept development and prototype."
    )
