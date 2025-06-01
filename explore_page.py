import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import folium
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from streamlit_folium import st_folium
import plotly.express as px




def show_mass_year_scatter(df):
    st.subheader("Mass vs. Year") 
    fig = px.scatter(   # using plotly for interaction
        df,
        x='Year_clean',
        y='Mass_g',
        color='Fall_simplified', 
        hover_data=['simplified_type'],
        title="Meteorite Mass Over Time",
        labels={'Mass_g': 'Mass (g)', 'Year_clean': 'Year'},
        log_y=True  
    )
    st.plotly_chart(fig)


def show_mass_type_boxplot(df):
    st.subheader("Mass by Meteorite Type")
    fig, ax = plt.subplots(figsize=(20, 8))
    sns.boxplot(x='simplified_type', y='Mass_g', data=df, ax=ax)
    plt.xlabel('Meteorite Type')
    plt.ylabel('Mass (g)')
    ax.set_yscale("log")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_title("Mass Distribution Across Meteorite Types")
    st.pyplot(fig)


def show_landing_heatmap(df):

    st.title("Meteorite Landing Heatmap")
    # Drop missing coordinates
    df = df[['Latitude', 'Longitude']].dropna()
    # Create base map using folium
    m = folium.Map(location=[0, 0], zoom_start=2, tiles="CartoDB positron")
    # Generate heatmap data
    heat_data = df[['Latitude', 'Longitude']].values.tolist()
    HeatMap(heat_data, radius=10, blur=15, min_opacity=0.3).add_to(m)
    folium_static(m)


def show_pieces_vs_mass(df):
    st.subheader("Pieces vs. Mass of Meteorites")

    # Drop rows with missing or zero values
    df_filtered = df.dropna(subset=['pieces_numeric', 'Mass_g'])
    df_filtered = df_filtered[df_filtered['pieces_numeric'] > 0]
    df_filtered = df_filtered[df_filtered['Mass_g'] > 0]

    # interactable plot sorting mass by pieces found with  hue of type
    fig = px.scatter(
        df_filtered,
        x='pieces_numeric',
        y='Mass_g',
        hover_name='Name',
        color='simplified_type', 
        labels={'pieces_numeric': 'Number of Pieces', 'Mass_g': 'Mass (g)'},
        log_y=True,
        log_x=True,
    )
    st.plotly_chart(fig)


def show_discoveries_per_year(df):
    st.subheader("Discoveries Per Year")

    # drop missing years
    df_filtered = df.dropna(subset=["Year_clean"])
    df_filtered = df_filtered[df_filtered["Year_clean"].between(860, 2025)]

    # Plot
    plt.figure(figsize=(12, 6))
    sns.histplot(df_filtered["Year_clean"], bins=100, color='royalblue')
    plt.xlabel("Year")
    plt.ylabel("Number of Discoveries")
    plt.title("Histogram of Meteorite Discoveries Per Year")
    plt.grid(True)

    st.pyplot(plt)


def show_type_analysis_and_map(df):
    st.subheader("Meteorite Type Distribution and Map")

        
    type_counts = df['simplified_type'].value_counts().reset_index()
    type_counts.columns = ['Type', 'Count']

    plt.figure(figsize=(14, 8))
    sns.barplot(data=type_counts, x='Type', y='Count', palette='coolwarm')
    plt.xticks(rotation=90, ha='right')
    plt.title("Count of Meteorites by Type")
    plt.ylabel("Count")
    plt.xlabel("Meteorite Type")
    plt.tight_layout()
    st.pyplot(plt)

    # interactive map that can filter type
    st.markdown("### Map of Meteorite Locations by Type")
    available_types = df['simplified_type'].dropna().unique()
    selected_type = st.selectbox("Select Meteorite Type", sorted(available_types))

    
    filtered_df = df[
        (df['simplified_type'] == selected_type) & 
        df['Latitude'].notnull() & 
        df['Longitude'].notnull()
    ]
    # default clusters
    m = folium.Map(location=[20, 0], zoom_start=2)
    marker_cluster = MarkerCluster().add_to(m)

    #show name and year of the location point
    for _, row in filtered_df.iterrows():
        popup = f"{row['Name']} ({int(row['Year_clean']) if not pd.isna(row['Year_clean']) else 'Unknown'})"
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=popup,
            tooltip=row['simplified_type']
        ).add_to(marker_cluster)

    st_data = st_folium(m, width=800, height=500)


def show_explore_page():
    
    st.title("Explore Meteorite Dataset")
    df = pd.read_csv("final_meteorite_data.csv")  

    chart_type = st.selectbox("Select a Visualization", [
        "Mass vs. Year",
        "Mass by Meteorite Type",
        "Meteorite Landing Heatmap", 
        "Pieces vs. Mass of Meteorites",
        "Type Analysis and Map"
    ])





    if chart_type == "Mass vs. Year":
        show_mass_year_scatter(df)
    elif chart_type == "Mass by Meteorite Type":
        show_mass_type_boxplot(df)
    elif chart_type == "Meteorite Landing Heatmap":
        show_landing_heatmap(df) 
    elif chart_type == "Pieces vs. Mass of Meteorites":
        show_pieces_vs_mass(df)    
    elif chart_type == "Discoveries Per Year":
        show_discoveries_per_year(df)
    elif chart_type == "Type Analysis and Map":
        show_type_analysis_and_map(df)





   




