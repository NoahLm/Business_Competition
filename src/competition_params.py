# src/components/competition_params.py
import streamlit as st

def get_competition_params():
    st.sidebar.subheader("Competition Assessment Parameters")
    business_type = st.sidebar.selectbox(
        "Select Type of Business",
        ["restaurant", "cafe", "clothing_store", "convenience_store", "gym", "school"]  # add other types as needed
    )
    radius = st.sidebar.slider(
        "Search Radius (in meters)",
        min_value=100,
        max_value=5000,
        value=1000,
        step=100
    )
    return business_type, radius