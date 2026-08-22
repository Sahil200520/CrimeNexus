import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
from sklearn.cluster import DBSCAN
import branca.colormap as cm

def temporal_analysis(crime_pattern_analysis):
    st.write("##### Filter Controls")
    st.write("Select Districts and Crime Groups to analyze temporal trends.")

    district_options = ["All Districts"] + sorted(crime_pattern_analysis["District_Name"].dropna().unique().tolist())
    selected_districts = st.multiselect("Select Districts", district_options, default=["All Districts"])

    crime_group_options = ["All Crime Groups"] + sorted(crime_pattern_analysis["CrimeGroup_Name"].dropna().unique().tolist())
    selected_crime_groups = st.multiselect("Select Crime Groups", crime_group_options, default=["All Crime Groups"])

    selected_time_granularity = st.radio("Select Time Granularity", ["Year", "Month", "Day"], horizontal=True)

    filtered_df = crime_pattern_analysis.copy()
    if "All Districts" not in selected_districts and selected_districts:
        filtered_df = filtered_df[filtered_df["District_Name"].isin(selected_districts)]
    if "All Crime Groups" not in selected_crime_groups and selected_crime_groups:
        filtered_df = filtered_df[filtered_df["CrimeGroup_Name"].isin(selected_crime_groups)]

    if filtered_df.empty:
        st.warning("No data matching the selected filters.")
    else:
        data = filtered_df.groupby([selected_time_granularity, "District_Name", "CrimeGroup_Name"]).size().reset_index(name="Count")
        fig = px.bar(data, x=selected_time_granularity, y="Count", color="District_Name", barmode="group", hover_data=["CrimeGroup_Name"])
        fig.update_layout(xaxis_title=selected_time_granularity, yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)

def crime_hotspot_analysis(df, mean_lat, mean_lon):
    m = folium.Map(location=[mean_lat, mean_lon], zoom_start=7)

    colormap = cm.LinearColormap(colors=['blue', 'yellow', 'red'], vmin=0, vmax=df['Count'].max())

    HeatMap(df[['Latitude', 'Longitude', 'Count']].values.tolist(), 
            gradient={"0.4": 'blue', "0.65": 'yellow', "1.0": 'red'}, 
            radius=15).add_to(m)

    coords = df[['Latitude', 'Longitude']].values
    if len(coords) >= 5:
        dbscan = DBSCAN(eps=0.1, min_samples=5)
        df['Cluster'] = dbscan.fit_predict(coords)

        for cluster in df['Cluster'].unique():
            if cluster != -1:
                cluster_points = df[df['Cluster'] == cluster]
                center_lat = cluster_points['Latitude'].mean()
                center_lon = cluster_points['Longitude'].mean()
                count = cluster_points['Count'].sum()
                folium.Marker(
                    [center_lat, center_lon],
                    popup=f'Cluster {cluster}<br>Crimes: {count}',
                    icon=folium.Icon(color='red', icon='info-sign')
                ).add_to(m)

    colormap.add_to(m)
    colormap.caption = 'Crime Density'
    return m

def crime_hotspots(crime_pattern_analysis, mean_lat, mean_lon):
    dates = st.radio("Select Date Range Mode", ["All", "Custom Date Range"], horizontal=True)

    min_date = crime_pattern_analysis['Date'].min()
    max_date = crime_pattern_analysis['Date'].max()

    if dates == "All":
        date_range = (min_date, max_date)
    else:
        date_range = st.date_input("Select date range", [min_date, max_date], key='date_range')

    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

    crime_types = st.multiselect("Select Crime Groups", crime_pattern_analysis['CrimeGroup_Name'].dropna().unique().tolist())

    if not crime_types:
        st.warning("Please choose at least one Crime Group from the dropdown above.")

    filtered_data = crime_pattern_analysis[
        (crime_pattern_analysis['Date'] >= pd.Timestamp(start_date)) & 
        (crime_pattern_analysis['Date'] <= pd.Timestamp(end_date))
    ]
    if crime_types:
        filtered_data = filtered_data[filtered_data['CrimeGroup_Name'].isin(crime_types)]
    
    if st.button("Render Hotspot Map", type="primary") and crime_types:
        if filtered_data.empty:
            st.info("No crime records found for selected criteria.")
            return

        aggregated_data = filtered_data.groupby(['District_Name', 'UnitName', 'Latitude', 'Longitude', 'CrimeGroup_Name']).size().reset_index(name='Count')
        m_lat = aggregated_data['Latitude'].mean()
        m_lon = aggregated_data['Longitude'].mean()

        m = crime_hotspot_analysis(aggregated_data, m_lat, m_lon)
        folium_static(m)

        st.markdown("""
        **Map Interpretation Guide:**
        - Heatmap gradient indicates crime density (Blue = Low, Yellow = Medium, Red = High).
        - Red markers indicate spatial cluster centers calculated via DBSCAN.
        """)

def chloropleth_maps(df, geojson_data, mean_lat, mean_lon):
    district_stats = df.groupby('District_Name').agg({'FIRNo': 'count', 'VICTIM COUNT': 'sum', 'Accused Count': 'sum'}).reset_index()

    selected_stat = st.selectbox('Select Crime Statistic', ['Crime Incidents', 'Total Victim Count', 'Total Accused Count'])

    if not geojson_data:
        st.warning("GeoJSON boundary data is unavailable. Displaying bar chart fallback.")
        stat_col = 'FIRNo' if selected_stat == 'Crime Incidents' else ('VICTIM COUNT' if selected_stat == 'Total Victim Count' else 'Accused Count')
        fig = px.bar(district_stats, x='District_Name', y=stat_col, title=f'{selected_stat} by District')
        st.plotly_chart(fig, use_container_width=True)
        return

    if selected_stat == 'Crime Incidents':
        color_col = 'FIRNo'
        label_text = 'Crime Incidents'
    elif selected_stat == 'Total Victim Count':
        color_col = 'VICTIM COUNT'
        label_text = 'Total Victim Count'
    else:
        color_col = 'Accused Count'
        label_text = 'Total Accused Count'

    fig = px.choropleth_mapbox(
        district_stats,
        geojson=geojson_data,
        locations='District_Name',
        featureidkey="properties.district",
        color=color_col,
        color_continuous_scale="Viridis",
        mapbox_style="carto-positron",
        zoom=5,
        center={"lat": mean_lat, "lon": mean_lon},
        opacity=0.5,
        labels={color_col: label_text},
        title=f'Choropleth Map: {label_text} by District'
    )
    st.plotly_chart(fig, use_container_width=True)
