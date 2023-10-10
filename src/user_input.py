# src/components/user_input.py
import streamlit as st

def get_user_input():
    st.title('Business Competition Assessor')
    st.subheader('Enter the business information:')
    
    business_name = st.text_input('Business Name:')
    latitude = st.number_input('Latitude:', step=0.0001, format='%.4f')
    longitude = st.number_input('Longitude:', step=0.0001, format='%.4f')
    
    return business_name, latitude, longitude
