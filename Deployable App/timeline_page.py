import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import pydeck as pdk


def show_timeline_page():
  
        # Title
    st.title("Explore Meteorite Timeline")

    
    # Load data
    @st.cache_data
    def load_data():
        df = pd.read_csv("final_meteorite_data.csv")
        
        # Extract coordinates
        if 'LatLong' in df.columns and ('Latitude' not in df or 'Longitude' not in df):
            df[['Latitude', 'Longitude']] = df['LatLong'].str.strip("()").str.split(",", expand=True).astype(float)

        df = df.dropna(subset=['Latitude', 'Longitude', 'Year_clean'])
        df['Year_clean'] = df['Year_clean'].astype(int)  
        return df

    df = load_data()

    # Filter setup
    min_year, max_year = int(df['Year_clean'].min()), int(df['Year_clean'].max())

    # Initial filtered data (entire range)
    year_range = (min_year, max_year)
    fall_type = df['Fall_simplified'].dropna().unique()
    status = df['Status_simplified'].dropna().unique()

    # Show the map first (full dataset temporarily) - this is required to work
    filtered_df = df.copy()

    # controls below map
    st.markdown("---")
    st.subheader("Filter by Year, Fall/found, and Status")

    year_range = st.slider("Select Year Range", min_year, max_year, (min_year, max_year))
    selected_fall = st.multiselect("Fall/found", fall_type, default=fall_type)
    selected_status = st.multiselect("Status", status, default=status)

    # Apply filters to the data to remove any erorrs
    filtered_df = df[
        (df['Year_clean'] >= year_range[0]) & (df['Year_clean'] <= year_range[1]) &
        (df['Fall_simplified'].isin(selected_fall)) &
        (df['Status_simplified'].isin(selected_status))
    ]

    st.write(f"Displaying {len(filtered_df)} meteorites from {year_range[0]} to {year_range[1]}.")

    # Re-render updated map with filters
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=20,
            longitude=0,
            zoom=1.5,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=filtered_df,
                get_position='[Longitude, Latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius=20000,
                pickable=True,
            )
        ],
        tooltip={"text": "Name: {Name}\nMass: {Mass_g}\nYear: {Year_clean}"} # what shows on the daat points on the map
    ))