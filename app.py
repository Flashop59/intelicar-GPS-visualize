import streamlit as st
import pandas as pd
import pydeck as pdk

# Streamlit page config
st.set_page_config(page_title="GPS Tracker Visualization", layout="wide")

st.title("📍 GPS Location Visualizer (Intellicar Data)")
st.markdown("Upload your `GPS_Report.csv` to visualize the GPS data on a Mapbox map.")

# Upload file
uploaded_file = st.file_uploader("Upload GPS_Report.csv", type=["csv"])

if uploaded_file:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)

    # Display first few rows
    st.subheader("Raw Data Preview")
    st.dataframe(df.head())

    # Detect latitude and longitude columns
    lat_col = next((col for col in df.columns if 'lat' in col.lower()), None)
    lon_col = next((col for col in df.columns if 'lon' in col.lower() or 'lng' in col.lower()), None)

    if not lat_col or not lon_col:
        st.error("Could not find latitude/longitude columns in the uploaded file.")
    else:
        # Remove invalid or missing coordinates
        df_clean = df.dropna(subset=[lat_col, lon_col])
        df_clean = df_clean[(df_clean[lat_col] != 0) & (df_clean[lon_col] != 0)]

        # Create map
        st.subheader("Map View of GPS Points")
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/streets-v12',
            initial_view_state=pdk.ViewState(
                latitude=df_clean[lat_col].mean(),
                longitude=df_clean[lon_col].mean(),
                zoom=12,
                pitch=0,
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=df_clean,
                    get_position=f"[{lon_col}, {lat_col}]",
                    get_radius=30,
                    get_color=[255, 0, 0, 160],
                    pickable=True,
                ),
            ],
            tooltip={"text": f"{lat_col}: {{{lat_col}}}\n{lon_col}: {{{lon_col}}}"}
        ))
