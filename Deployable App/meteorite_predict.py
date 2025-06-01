import streamlit as st
import numpy as np
import pickle
import pandas as pd
import pydeck as pdk


def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

def show_predict_page():
    st.title("Predict Meteorite Landing Location")

    data = load_model()
    clf = data["model"]
    reg_model = data["reg_model"]
    le_Status = data["le_Status"]
    le_Fall = data["le_Fall"]
    le_type = data["le_type"]
    features = data["features"]
    kmeans = data["kmeans"]
    
    cluster_df = data["cluster_df"]
    
    

    label_encoders = {
        'Status_simplified': le_Status,
        'Fall_simplified': le_Fall,
        'simplified_type': le_type
    }


    st.write("### Input Meteorite Properties Here")


    status = st.selectbox("Official Status", le_Status.classes_)
    fall = st.selectbox("Fall or Found?", le_Fall.classes_)
    year = st.slider("Year Discovered", 860, 2025, 2000)
    m_type = st.selectbox("Meteorite Type (See https://www.lpi.usra.edu/ for full descriptions)", le_type.classes_)
    mass = st.number_input("Mass (g)", min_value=0.0, value=100.0)


    # Convert to DataFrame
    input_df = pd.DataFrame([{
        'Status_simplified': status,
        'Fall_simplified': fall,
        'Year_clean': year,
        'simplified_type': m_type,
        'Mass_g': mass
    }])

    # Encode
    for col, le in label_encoders.items():
        input_df[col] = input_df[col].astype(str)
        input_df[col] = input_df[col].apply(lambda x: le.transform([x])[0] if x in le.classes_ else -1)

    X_input = input_df[features]

    if st.button("Predict Location!"):
        region = clf.predict(X_input)[0]
        latlon = reg_model[region].predict(X_input)[0]

        st.success(f"**Predicted Region:** {region}")
        st.success(f"**Predicted Latitude:** {latlon[0]:.5f}")
        st.success(f"**Predicted Longitude:** {latlon[1]:.5f}")

        # Show point on map
        st.write("### Predicted Location on Map")
        map_df = pd.DataFrame([{
            'Latitude': latlon[0],
            'Longitude': latlon[1]
        }])

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_df,
            get_position='[Longitude, Latitude]',
            get_color='[200, 30, 0, 160]',
            get_radius=50000,
        )

        view_state = pdk.ViewState(
            latitude=latlon[0],
            longitude=latlon[1],
            zoom=3,
            pitch=0,
        )

        st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

