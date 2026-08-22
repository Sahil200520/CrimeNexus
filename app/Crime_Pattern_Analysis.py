import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
from sklearn.cluster import DBSCAN
import branca.colormap as cm
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def temporal_analysis(crime_pattern_analysis):
    st.write("##### Filter Controls")
    st.write("Select Districts and Crime Groups to analyze temporal trends.")

    district_options = ["All Districts"] + sorted(crime_pattern_analysis["District_Name"].dropna().unique().tolist())
    selected_districts = st.multiselect("Select Districts", district_options, default=["All Districts"], key="ta_districts")

    crime_group_options = ["All Crime Groups"] + sorted(crime_pattern_analysis["CrimeGroup_Name"].dropna().unique().tolist())
    selected_crime_groups = st.multiselect("Select Crime Groups", crime_group_options, default=["All Crime Groups"], key="ta_groups")

    selected_time_granularity = st.radio("Select Time Granularity", ["Year", "Month", "Day"], horizontal=True, key="ta_granularity")

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

    colormap = cm.LinearColormap(colors=['blue', 'yellow', 'red'], vmin=0, vmax=max(1, df['Count'].max()))

    HeatMap(df[['Latitude', 'Longitude', 'Count']].values.tolist(), 
            gradient={"0.4": 'blue', "0.65": 'yellow', "1.0": 'red'}, 
            radius=15).add_to(m)

    coords = df[['Latitude', 'Longitude']].values
    if len(coords) >= 5:
        coords_rad = np.radians(coords)
        dbscan = DBSCAN(eps=10.0/6371.0, min_samples=5, metric='haversine')
        df['Cluster'] = dbscan.fit_predict(coords_rad)

        for cluster in df['Cluster'].unique():
            if cluster != -1:
                cluster_points = df[df['Cluster'] == cluster]
                center_lat = cluster_points['Latitude'].mean()
                center_lon = cluster_points['Longitude'].mean()
                count = cluster_points['Count'].sum()
                folium.Marker(
                    [center_lat, center_lon],
                    popup=f'Cluster {cluster + 1}<br>Crimes: {count}',
                    icon=folium.Icon(color='red', icon='info-sign')
                ).add_to(m)

    colormap.add_to(m)
    colormap.caption = 'Crime Density'
    return m

def crime_hotspots(crime_pattern_analysis, mean_lat, mean_lon):
    dates = st.radio("Select Date Range Mode", ["All", "Custom Date Range"], horizontal=True, key="hs_date_mode")

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

    crime_types = st.multiselect("Select Crime Groups", crime_pattern_analysis['CrimeGroup_Name'].dropna().unique().tolist(), key="hs_groups")

    if not crime_types:
        st.warning("Please choose at least one Crime Group from the dropdown above.")

    filtered_data = crime_pattern_analysis[
        (crime_pattern_analysis['Date'] >= pd.Timestamp(start_date)) & 
        (crime_pattern_analysis['Date'] <= pd.Timestamp(end_date))
    ]
    if crime_types:
        filtered_data = filtered_data[filtered_data['CrimeGroup_Name'].isin(crime_types)]
    
    if st.button("Render Hotspot Map", type="primary", key="btn_hotspot") and crime_types:
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

def hotspot_evolution_slider(crime_pattern_analysis, mean_lat, mean_lon):
    st.subheader("🗺️ Hotspot Evolution & Time Slider")
    st.write("Slide through time (Months & Years) to observe spatial movement of crime hotspots.")

    df = crime_pattern_analysis.copy()
    if 'Date' not in df.columns:
        df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])

    df['YearMonth'] = df['Date'].dt.to_period('M').astype(str)
    available_months = sorted(df['YearMonth'].unique())

    if not available_months:
        st.error("No valid timeline data available.")
        return

    selected_month = st.select_slider("Select Timeline Period (Year-Month):", options=available_months, value=available_months[0])

    crime_groups = ["All Crime Groups"] + sorted(df['CrimeGroup_Name'].dropna().unique().tolist())
    selected_group = st.selectbox("Filter Crime Category:", crime_groups, key="slider_group")

    period_df = df[df['YearMonth'] == selected_month]
    if selected_group != "All Crime Groups":
        period_df = period_df[period_df['CrimeGroup_Name'] == selected_group]

    st.info(f"Showing Hotspot Evolution for Period: **{selected_month}** | Records: **{len(period_df)}**")

    if period_df.empty:
        st.warning("No crimes recorded for this specific time frame.")
        return

    agg_df = period_df.groupby(['District_Name', 'UnitName', 'Latitude', 'Longitude']).size().reset_index(name='Count')
    m_lat = agg_df['Latitude'].mean() if not agg_df.empty else mean_lat
    m_lon = agg_df['Longitude'].mean() if not agg_df.empty else mean_lon

    m = crime_hotspot_analysis(agg_df, m_lat, m_lon)
    folium_static(m)

def crime_forecasting_engine(crime_pattern_analysis):
    st.subheader("🔮 Crime Forecasting Engine (7 & 30 Days)")
    st.write("Forecast expected future crime trends using time-series modeling.")

    st.warning("⚠️ **Forecast Disclaimer**: Projections represent statistical estimates based on historical patterns and should be treated as guidance rather than absolute certainty.")

    df = crime_pattern_analysis.copy()
    if 'Date' not in df.columns:
        df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])

    col1, col2, col3 = st.columns(3)
    with col1:
        districts = ["All Districts"] + sorted(df['District_Name'].dropna().unique().tolist())
        sel_district = st.selectbox("Select District for Forecast:", districts, key="fc_district")
    with col2:
        categories = ["All Crime Groups"] + sorted(df['CrimeGroup_Name'].dropna().unique().tolist())
        sel_category = st.selectbox("Select Category:", categories, key="fc_category")
    with col3:
        forecast_horizon = st.radio("Forecast Horizon:", ["7 Days", "30 Days"], horizontal=True, key="fc_horizon")

    days_ahead = 7 if forecast_horizon == "7 Days" else 30

    filt_df = df.copy()
    if sel_district != "All Districts":
        filt_df = filt_df[filt_df['District_Name'] == sel_district]
    if sel_category != "All Crime Groups":
        filt_df = filt_df[filt_df['CrimeGroup_Name'] == sel_category]

    if filt_df.empty:
        st.warning("Insufficient data for the selected criteria.")
        return

    daily_ts = filt_df.groupby(filt_df['Date'].dt.date).size().reset_index(name='Count')
    daily_ts['Date'] = pd.to_datetime(daily_ts['Date'])
    daily_ts = daily_ts.sort_values('Date').set_index('Date')

    # Reindex to fill missing dates with 0
    full_idx = pd.date_range(start=daily_ts.index.min(), end=daily_ts.index.max(), freq='D')
    daily_ts = daily_ts.reindex(full_idx, fill_value=0)

    # Fit Time Series Model (Exponential Smoothing with additive trend)
    try:
        model = ExponentialSmoothing(daily_ts['Count'], trend='add', seasonal=None, initialization_method='estimated').fit()
        forecast_vals = model.forecast(days_ahead)
    except Exception:
        # Fallback to rolling average forecast
        last_val = daily_ts['Count'].rolling(7, min_periods=1).mean().iloc[-1]
        forecast_vals = pd.Series([last_val] * days_ahead, index=pd.date_range(start=daily_ts.index.max() + pd.Timedelta(days=1), periods=days_ahead, freq='D'))

    forecast_vals = np.clip(forecast_vals, a_min=0, a_max=None)
    fc_dates = pd.date_range(start=daily_ts.index.max() + pd.Timedelta(days=1), periods=days_ahead, freq='D')
    fc_df = pd.DataFrame({'Date': fc_dates, 'Forecast': forecast_vals.values})

    # Upper and Lower Confidence Bounds (15% margin)
    fc_df['Upper Bound'] = fc_df['Forecast'] * 1.2
    fc_df['Lower Bound'] = fc_df['Forecast'] * 0.8

    m1, m2, m3 = st.columns(3)
    m1.metric("Historical Avg (Daily)", f"{daily_ts['Count'].mean():.1f} crimes")
    m2.metric(f"Forecasted Total ({forecast_horizon})", f"{fc_df['Forecast'].sum():.0f} crimes")
    m3.metric("Projected Daily Trend", f"{fc_df['Forecast'].mean():.1f} crimes/day")

    fig = go.Figure()

    # Historical trend (last 60 days)
    hist_subset = daily_ts.iloc[-60:]
    fig.add_trace(go.Scatter(x=hist_subset.index, y=hist_subset['Count'], mode='lines+markers', name='Historical Crime', line=dict(color='#00b4d8')))

    # Forecast trend
    fig.add_trace(go.Scatter(x=fc_df['Date'], y=fc_df['Forecast'], mode='lines+markers', name='Forecast Estimate', line=dict(color='#ff4d6d', dash='dash')))
    fig.add_trace(go.Scatter(x=fc_df['Date'], y=fc_df['Upper Bound'], mode='lines', name='Upper Bound', line=dict(color='rgba(255, 77, 109, 0.2)'), showlegend=False))
    fig.add_trace(go.Scatter(x=fc_df['Date'], y=fc_df['Lower Bound'], mode='lines', name='Lower Bound', fill='tonexty', fillcolor='rgba(255, 77, 109, 0.1)', line=dict(color='rgba(255, 77, 109, 0.2)'), showlegend=False))

    fig.update_layout(title=f"{forecast_horizon} Statistical Crime Forecast for {sel_district} ({sel_category})", xaxis_title="Date", yaxis_title="Crime Count")
    st.plotly_chart(fig, use_container_width=True)

def crime_anomaly_detection(crime_pattern_analysis):
    st.subheader("🚨 Crime Trend Anomaly & Spike Detection")
    st.write("Detect unusual crime volume spikes using statistical Z-Score thresholding.")

    df = crime_pattern_analysis.copy()
    if 'Date' not in df.columns:
        df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])

    col1, col2 = st.columns(2)
    with col1:
        districts = ["All Districts"] + sorted(df['District_Name'].dropna().unique().tolist())
        sel_district = st.selectbox("Select District:", districts, key="an_district")
    with col2:
        sensitivity = st.slider("Anomaly Sensitivity (Z-Score Threshold):", min_value=1.5, max_value=3.5, value=2.0, step=0.1)

    filt_df = df.copy()
    if sel_district != "All Districts":
        filt_df = filt_df[filt_df['District_Name'] == sel_district]

    if filt_df.empty:
        st.warning("No data available for anomaly detection.")
        return

    # Aggregate by Weekly Count
    weekly_ts = filt_df.groupby(pd.Grouper(key='Date', freq='W-MON')).size().reset_index(name='Weekly_Count')
    
    mean_val = weekly_ts['Weekly_Count'].mean()
    std_val = weekly_ts['Weekly_Count'].std()

    if std_val == 0 or np.isnan(std_val):
        st.info("Insufficient variance to calculate anomalies.")
        return

    weekly_ts['Z_Score'] = (weekly_ts['Weekly_Count'] - mean_val) / std_val
    weekly_ts['Is_Anomaly'] = weekly_ts['Z_Score'] >= sensitivity

    anomalies = weekly_ts[weekly_ts['Is_Anomaly']]

    st.info(f"**Baseline Average**: ~{mean_val:.1f} crimes/week | **Threshold**: +{sensitivity} Standard Deviations")

    if not anomalies.empty:
        st.warning(f"⚠️ **{len(anomalies)} Unusual Crime Spike(s) Detected!**")
        anomaly_table = anomalies[['Date', 'Weekly_Count', 'Z_Score']].copy()
        anomaly_table['Z_Score'] = anomaly_table['Z_Score'].round(2)
        anomaly_table['Status'] = '🚨 Severe Spike'
        st.dataframe(anomaly_table, use_container_width=True, hide_index=True)
    else:
        st.success("✅ No unusual crime spikes detected under the selected sensitivity threshold.")

    fig = go.Figure()

    # Normal line
    fig.add_trace(go.Scatter(x=weekly_ts['Date'], y=weekly_ts['Weekly_Count'], mode='lines+markers', name='Weekly Crime Count', line=dict(color='#3a86ff')))

    # Threshold line
    threshold_val = mean_val + (sensitivity * std_val)
    fig.add_trace(go.Scatter(x=weekly_ts['Date'], y=[threshold_val] * len(weekly_ts), mode='lines', name='Spike Threshold', line=dict(color='#ff006e', dash='dot')))

    # Anomaly points
    if not anomalies.empty:
        fig.add_trace(go.Scatter(x=anomalies['Date'], y=anomalies['Weekly_Count'], mode='markers', name='Detected Anomaly', marker=dict(color='#ff006e', size=12, symbol='x')))

    fig.update_layout(title=f"Weekly Crime Trend & Spike Detection for {sel_district}", xaxis_title="Week", yaxis_title="Crime Count")
    st.plotly_chart(fig, use_container_width=True)

def chloropleth_maps(df, geojson_data, mean_lat, mean_lon):
    district_stats = df.groupby('District_Name').agg({'FIRNo': 'count', 'VICTIM COUNT': 'sum', 'Accused Count': 'sum'}).reset_index()

    selected_stat = st.selectbox('Select Crime Statistic', ['Crime Incidents', 'Total Victim Count', 'Total Accused Count'], key="ch_stat")

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
