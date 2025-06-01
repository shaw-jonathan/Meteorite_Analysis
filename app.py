import streamlit as st
from meteorite_predict import show_predict_page
from explore_page import show_explore_page
from timeline_page import show_timeline_page

# page = st.sidebar.selectbox("Explore or Predict", ("Predict", "Explore"))

st.set_page_config(page_title="Meteorite Landing Predictor", layout="centered")

page = st.sidebar.selectbox("Select a page", ("Predict", "Explore", "Timeline"))


if page == "Predict":
    show_predict_page()
elif page == "Explore":
    show_explore_page()
else:
    show_timeline_page()
    