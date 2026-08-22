import os
import sys

# Ensure app directory has highest priority in sys.path
app_dir = os.path.dirname(__file__)
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

import requests
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

from Criminal_Profiling import create_criminal_profiling_dashboard
from Crime_Pattern_Analysis import (
    temporal_analysis,
    chloropleth_maps,
    crime_hotspots,
    hotspot_evolution_slider,
    crime_forecasting_engine,
    crime_anomaly_detection
)
from Predictive_modeling import predictive_modeling_recidivism
from Resource_Allocation import resource_allocation
from Continuous_Learning_and_Feedback import continuous_learning_and_feedback

st.set_page_config(page_title="CrimeNexus (CT-DFIR-01)", page_icon="🚔", layout="wide")
st.warning("⚠️ **PROOF-OF-CONCEPT — NOT FOR OPERATIONAL USE** | CT-DFIR-01 Research & Analytics System")

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

with st.sidebar:
    selected = option_menu(
        "CrimeNexus", 
        [
            'Home', 
            'Crime Pattern Analysis', 
            'Criminal Profiling', 
            'Predictive Modeling', 
            'Police Resource Allocation and Management', 
            'Continuous Learning and Feedback', 
            'Documentation and Resources'
        ], 
        icons=['house-fill', 'bar-chart-fill', 'fingerprint', 'cpu-fill', 'diagram-3-fill', 'book-fill', 'file-earmark-text-fill'], 
        menu_icon="shield-shaded", 
        default_index=0, 
        orientation="vertical",
        styles={
            "container": {"padding": "5!important", "background-color": "#1c1e21"},
            "menu-title": {"font-size": "18px", "font-weight": "bold", "color": "#e5e5e5"},
            "menu-icon": {"color": "#62d0ff"},
            "nav": {"background-color": "#1c1e21"},
            "nav-item": {"padding": "0px 10px"},
            "nav-link": {
                "text-decoration": "none",
                "color": "#e5e5e5",
                "font-size": "14px",
                "font-weight": "normal",
                "--hover-color": "#62d0ff",
            },
            "nav-link-selected": {
                "background-color": "#62d0ff",
                "color": "#1c1e21",
                "font-weight": "bold",
            },
            "icon": {"color": "#e5e5e5", "font-size": "16px"},
            "separator": {"margin": "5px 0px", "border-color": "#343a40"},
        }
    )

if selected == "Home":
    st.title("Welcome to CrimeNexus 🚔💻")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            CrimeNexus is an innovative, AI-powered solution that revolutionizes the way law enforcement agencies approach public safety. By utilizing advanced data analysis and machine learning, our platform empowers agencies to make data-driven decisions, enabling them to allocate resources more efficiently and effectively.
            """
        )
        st.markdown(
            """
            CrimeNexus provides law enforcement agencies with actionable intelligence to stay one step ahead of crime. Key analytical capabilities include:
            """
        )
        st.markdown(
            """
            - **Crime Pattern Analysis**: Spatial, temporal, hotspot evolution, forecasting, and anomaly detection.
            - **Criminal Profiling**: Offender demographics and criminal behavior analytics.
            - **Predictive Modeling**: Recidivism risk estimation using AutoML ensembles.
            - **Resource Allocation**: Personnel deployment optimization using mathematical programming (PuLP).
            - **Continuous Learning & Feedback**: Stakeholder feedback, real-time alert monitoring, and email notifications.
            """
        )

    with col2:
        data_file_path = os.path.join(root_dir, 'assets', 'Home_Page_image.jpg')
        if os.path.exists(data_file_path):
            st.image(data_file_path, use_container_width=True)

if selected == "Crime Pattern Analysis":
    @st.cache_data
    def load_data():
        geojson_data = {}
        try:
            url = "https://raw.githubusercontent.com/adarshbiradar/maps-geojson/master/states/karnataka.json"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                geojson_data = response.json()
        except Exception as e:
            st.error(f"Failed to fetch GeoJSON map data: {e}")
        data_file_path = os.path.join(root_dir, 'Component_datasets', 'Crime_Pattern_Analysis_Cleaned.csv')

        crime_pattern_analysis = pd.read_csv(data_file_path)
        crime_pattern_analysis['Date'] = pd.to_datetime(crime_pattern_analysis[['Year', 'Month', 'Day']])
        mean_lat = crime_pattern_analysis['Latitude'].mean()
        mean_lon = crime_pattern_analysis['Longitude'].mean()
        return mean_lat, mean_lon, geojson_data, crime_pattern_analysis

    mean_lat, mean_lon, geojson_data, crime_pattern_analysis = load_data()

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Temporal & Choropleth Maps",
        "🗺️ Hotspot Evolution (Time Slider)",
        "🔮 Crime Forecasting Engine (7/30 Days)",
        "🚨 Anomaly & Spike Detection"
    ])

    with tab1:
        st.subheader("Temporal Analysis of Crime Data")
        temporal_analysis(crime_pattern_analysis)

        st.subheader("Choropleth Maps")
        chloropleth_maps(crime_pattern_analysis, geojson_data, mean_lat, mean_lon)

        st.subheader("Crime Hotspot Map")
        crime_hotspots(crime_pattern_analysis, mean_lat, mean_lon)

    with tab2:
        hotspot_evolution_slider(crime_pattern_analysis, mean_lat, mean_lon)

    with tab3:
        crime_forecasting_engine(crime_pattern_analysis)

    with tab4:
        crime_anomaly_detection(crime_pattern_analysis)

if selected == "Criminal Profiling":
    create_criminal_profiling_dashboard()

if selected == "Predictive Modeling":
    predictive_modeling_recidivism()

if selected == "Police Resource Allocation and Management":
    data_file_path = os.path.join(root_dir, 'Component_datasets', 'Resource_Allocation_Cleaned.csv')
    df = pd.read_csv(data_file_path)
    resource_allocation(df)

if selected == "Continuous Learning and Feedback":
    continuous_learning_and_feedback()

if selected == "Documentation and Resources":
    st.subheader("Documentation & Project Resources 📖")
    st.markdown('Click [here](https://github.com/Sahil200520/CrimeNexus/blob/main/Readme.md) to view the project documentation and resources repository.')
