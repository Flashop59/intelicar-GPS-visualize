import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="Intellicar GPS Visualizer", layout="wide")

st.title("📍 GPS Tracker Map (Intellicar Format)")
st.markdown("Upload your **GPS_Report.csv** to view GPS coordinates on a satellite map.")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Raw Data Preview")
    st.dataframe(df.head())

    if 'Ignition' not in df.columns:
        st.error("❌ 'Ignition' column not found.")
    else:
        try:
            df[['Latitude', 'Longitude']] = df['Ignition'].str.split(',', expand=True).astype(float)
            df = df.dropna(subset=['Latitude', 'Longitude'])

            st.subheader("🗺️ Mapped GPS Points (Satellite View)")
            st.pydeck_chart(pdk.Deck(
                map_style="mapbox://styles/mapbox/satellite-streets-v12",
                initial_view_state=pdk.ViewState(
                    latitude=df["Latitude"].mean(),
                    longitude=df["Longitude"].mean(),
                    zoom=14,
                    pitch=0,
                ),
                layers=[
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=df,
                        get_position='[Longitude, Latitude]',
                        get_color='[255, 0, 0, 160]',
                        get_radius=5,  # 👈 Smaller pin radius
                    ),
                ],
                tooltip={"text": "Lat: {Latitude}\nLon: {Longitude}"}
            ))

        except Exception as e:
            st.error(f"⚠️ Error parsing coordinates: {e}")
