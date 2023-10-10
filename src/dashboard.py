import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def display_dashboard(business_info, latitude, longitude, competing_businesses):
    st.title("Competition Assessment Dashboard")
    
    st.header("Business Metrics")
    st.write(f'Business Name: {business_info["name"]}')
    st.write(f'Type of Place: {business_info["type"]}')
    st.write(f'Score: {business_info["score"]}')
    st.write(f'Number of Reviews: {business_info["number_of_reviews"]}')
    st.write(f'Latitude: {latitude}')
    st.write(f'Longitude: {longitude}')
    
    st.header("Competition Metrics")
    # Convert competing businesses to DataFrame for easier analysis
    comp_df = pd.DataFrame(competing_businesses)
    
    #Para ver lo que contiene comp_df (Eliminar despues)
    #st.write("Esto es solo para ver lo que contiene el df (BORRAR)")
    #st.write(comp_df)
    
    # Combine business_info with competing businesses
    business_df = pd.DataFrame([business_info])
    
    st.write(f'Number of Competing Businesses: {len(comp_df)}')
    
    # Score vs Number of Reviews visualization
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Set a beautiful Seaborn style
    sns.set_style("whitegrid")
    
    # Create a figure and axes
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Plot the business_info data with a different color and style
    ax.scatter(
        business_df['number_of_reviews'],
        business_df['score'],
        label='Your Business',
        color='red',
        marker='o',
        s=100,
        edgecolors='black',  # Add black edge colors for better visibility
        linewidths=1.5,     # Increase marker edge linewidth
        zorder=2             # Place the points above other points
    )
    
    # Plot the competing businesses with a different color and style
    ax.scatter(
        comp_df['Number of Reviews'],
        comp_df['Score'],
        label='Competing Businesses',
        color='blue',
        alpha=0.7,            # Reduce opacity for a subtle effect
        edgecolors='gray',    # Add gray edge colors
        linewidths=0.8,       # Adjust marker edge linewidth
        zorder=1              # Place the points below your business points
    )
    
    ax.set_title('Score vs Number of Reviews', fontsize=16)
    ax.set_xlabel('Number of Reviews', fontsize=14)
    ax.set_ylabel('Score', fontsize=14)
    
    # Customize tick labels' font size
    ax.tick_params(labelsize=12)
    
    # Add grid lines
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # Add legend with a shadow effect
    ax.legend(loc='best', fontsize=12, shadow=True)
    
    # Add a background color to the legend
    legend = ax.legend(loc='best', fontsize=12, shadow=True)
    legend.get_frame().set_facecolor('lightgray')
    
    # Remove spines (top and right axes lines)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    st.pyplot(fig)
    
     # Create a DataFrame for the map
    map_data = pd.DataFrame({'latitude': [latitude], 'longitude': [longitude]})
    
    # Add your business to the map_data DataFrame
    map_data.loc[0] = [latitude, longitude]
    
    # Add competing businesses to the map_data DataFrame
    map_data = pd.concat([map_data, comp_df[['latitude', 'longitude']].reset_index(drop=True)])

    # Print the DataFrame before creating the map
    #st.subheader("Map Data")
    #st.write(map_data)

    # Display the map
    st.subheader("Map")
    st.map(map_data,
    latitude='latitude',
    longitude='longitude')