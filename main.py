import streamlit as st
import pandas as pd
from src.user_input import get_user_input
from queries.place_id_query import get_place_id
from queries.business_info_query import get_business_info
from src.competition_params import get_competition_params
from queries.competing_businesses_query import search_competing_businesses
from src.dashboard import display_dashboard
from queries.aggregator_query import aggregate_business_info
from src.export_report import create_pdf_report

api_key = st.secrets["api_key"]

@st.cache_data
def cached_get_place_id(business_name, latitude, longitude, api_key):
    return get_place_id(business_name, latitude, longitude, api_key)

@st.cache_data
def cached_get_business_info(place_id, api_key):
    return get_business_info(place_id, api_key)

@st.cache_data
def cached_search_competing_businesses(api_key, business_type, latitude, longitude, radius):
    return search_competing_businesses(api_key, business_type, latitude, longitude, radius)

@st.cache_data
def cached_display_dashboard(business_info, latitude, longitude, competing_businesses):
    return display_dashboard(business_info, latitude, longitude, competing_businesses)


def main():
    st.sidebar.title("Navigation")
    selected_box = st.sidebar.radio(
        "Choose an option",
        ("Business Information", "Competition Assessment")
    )
    
    if selected_box == "Business Information":
        st.header("Business Information")
        business_name, latitude, longitude = get_user_input()
        
        # Assuming you have your Google API Key as an environment variable
        #api_key = st.secrets["google_api_key"]
        try:
            place_id = cached_get_place_id(business_name, latitude, longitude, api_key)
            st.write(f'Place ID: {place_id}')
        except Exception as e:
            st.error(f'Error: {e}')
        
        try:
            business_info = cached_get_business_info(place_id, api_key)
            # General information
            st.subheader("General Information")
            st.write(f'Business Name: {business_info["name"]}')
            st.write(f'Type of Place: {business_info["type"]}')

            # Rating and reviews
            st.subheader("Rating and Reviews")
            st.write(f'Score: {business_info["score"]}')
            st.write(f'Number of Reviews: {business_info["number_of_reviews"]}')
            
            # Display the map
            st.subheader("Map")
            df_map = pd.DataFrame({'latitude': [latitude], 'longitude': [longitude]})
            st.map(df_map[['latitude', 'longitude']])
            
            # Comments
            st.subheader("Comments")
            with st.expander("Show Comments"):
                comment_number = 1
                for comment in business_info["comments"]:
                    st.write(f"Comment {comment_number}: {comment}")
                    comment_number += 1

        except Exception as e:
            st.error(f'Error: {e}')

    elif selected_box == "Competition Assessment":
        st.header("Competition Assessment")
        business_name, latitude, longitude = get_user_input()
        business_type, radius = get_competition_params()
        st.write(f'Type of Business: {business_type}')
        st.write(f'Search Radius: {radius} meters')
        
        try:
            place_id = cached_get_place_id(business_name, latitude, longitude, api_key)
            business_info = cached_get_business_info(place_id, api_key)

            competing_businesses = cached_search_competing_businesses(api_key, business_type, latitude, longitude, radius)
            
            business_data = aggregate_business_info(api_key, competing_businesses)
            display_dashboard(business_info, latitude, longitude, business_data)

            #Camino Real Mérida
            #21.0374
            #-89.6016
           
        except Exception as e:
            st.error(f'Error Main: {e}')
            
        if st.button("Export Report"):
            competing_businesses = cached_search_competing_businesses(api_key, business_type, latitude, longitude, radius)
            report_file_path = create_pdf_report(business_info, competing_businesses)
            st.download_button(
                label="Download Report",
                data=open(report_file_path, "rb"),
                file_name="competition_assessment_report.pdf"
            )


if __name__ == "__main__":
    main()
