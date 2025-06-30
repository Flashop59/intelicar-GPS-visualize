import streamlit as st
import pandas as pd
import pydeck as pdk
import os

# Set Mapbox API key
os.environ["MAPBOX_API_KEY"] = "pk.eyJ1IjoiZmxhc2hvcDAwNyIsImEiOiJjbHo5NzkycmIwN2RxMmtzZHZvNWpjYmQ2In0.A_FZYl5zKjwSZpJuP_MHiA"

# Configure Streamlit page
st.set_page_config(page_title="Intellicar GPS Visualizer", layout="wide")

st.title("📍 GPS Tracker Map (Intellicar Format)")
st.markdown("Upload your **GPS_Report.csv** to view GPS coordinates on a satellite map.")

# File uploader
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 Raw Data Preview")
    st.dataframe(df.head())

    # Check and parse 'Ignition' column
    if 'Ignition' not in df.columns:
        st.error("❌ 'Ignition' column not found.")
    else:
        try:
            # Split into lat/lon
            df[['Latitude', 'Longitude']] = df['Ignition'].str.split(',', expand=True).astype(float)
            df = df.dropna(subset=['Latitude', 'Longitude'])

            st.subheader("🗺️ Mapped GPS Points (Satellite View)")
            st.pydeck_chart(pdk.Deck(
                map_style="mapbox://styles/mapbox/satellite-streets-v12",
                api_keys={"mapbox": os.environ["MAPBOX_API_KEY"]},
                initial_view_state=pdk.ViewState(
                    latitude=df["Latitude"].mean(),
                    longitude=df["Longitude"].mean(),
                    zoom=16,
                    pitch=0,
                ),
                layers=[
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=df,
                        get_position='[Longitude, Latitude]',
                        get_color='[255, 0, 0, 160]',
                        get_radius=5,
                    ),
                ],
                tooltip={"text": "Lat: {Latitude}\nLon: {Longitude}"}
            ))

        except Exception as e:
            st.error(f"⚠️ Error processing GPS coordinates: {e}")
