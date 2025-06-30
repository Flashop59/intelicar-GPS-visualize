import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="Intellicar GPS Visualizer", layout="wide")

st.title("📍 GPS Tracker Map (Intellicar Format)")
st.markdown("Upload your **GPS_Report.csv** to view GPS coordinates on a map.")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Raw Data Preview")
    st.dataframe(df.head())

    # Check if 'Ignition' column exists
    if 'Ignition' not in df.columns:
        st.error("❌ 'Ignition' column not found in the uploaded file.")
    else:
        # Split Ignition column into lat/lon
        try:
            df[['Latitude', 'Longitude']] = df['Ignition'].str.split(',', expand=True).astype(float)

            # Clean out any invalid points
            df = df.dropna(subset=['Latitude', 'Longitude'])

            st.subheader("📌 Mapped GPS Points")
            st.pydeck_chart(pdk.Deck(
                map_style="mapbox://styles/mapbox/streets-v12",
                initial_view_state=pdk.ViewState(
                    latitude=df["Latitude"].mean(),
                    longitude=df["Longitude"].mean(),
                    zoom=12,
                    pitch=0,
                ),
                layers=[
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=df,
                        get_position='[Longitude, Latitude]',
                        get_color='[255, 0, 0, 160]',
                        get_radius=30,
                    ),
                ],
                tooltip={"text": "Lat: {Latitude}\nLon: {Longitude}"}
            ))

        except Exception as e:
            st.error(f"⚠️ Error parsing coordinates: {e}")
