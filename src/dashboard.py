import streamlit as st

from src.data_loader import load_data
from src.data_cleaning import clean_data
from src.summary_analysis import (
    analyze_by_hour,
    analyze_by_hour_and_category,
    analyze_crime_trends_over_time,
    analyze_crime_by_division,
    analyze_crime_by_premises_type,
    analyze_crime_by_neighbourhood,
    get_hotspot_data
)
from src.visualizations import (
    create_hourly_chart,
    create_hourly_category_chart,
    create_crime_trend_chart,
    create_division_chart,
    create_premises_chart,
    create_crime_by_neighborhood_trend,
    create_neighborhood_geo_map
)
from src.constants import LATITUDE, LONGITUDE


@st.cache_data
def get_dashboard_data():
    raw_df = load_data("data/Toronto_Crime_Indicators.csv")
    return clean_data(raw_df)


def run_dashboard():
    st.set_page_config(
        page_title="Toronto Crime Analytics",
        layout="wide"
    )

    st.title("Toronto Crime Indicators Dashboard")
    st.write("Visual dashboard rendering historical Toronto crime indicator datasets.")
    st.divider()

    cleaned_df = get_dashboard_data()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Incidents by Hour of Day")
        hourly_df = analyze_by_hour(cleaned_df)
        st.pyplot(create_hourly_chart(hourly_df))

    with col2:
        st.subheader("Incidents by Hour and Category")
        hourly_cat_df = analyze_by_hour_and_category(cleaned_df)
        st.pyplot(create_hourly_category_chart(hourly_cat_df))

    st.divider()

    st.subheader("Crime Trends Over Time")
    trend_df = analyze_crime_trends_over_time(cleaned_df)
    st.pyplot(create_crime_trend_chart(trend_df))

    st.subheader("Police Division Activity")
    division_df = analyze_crime_by_division(cleaned_df)
    st.pyplot(create_division_chart(division_df))

    st.subheader("Crime Incidents by Premises Type")
    premises_df = analyze_crime_by_premises_type(cleaned_df)
    st.pyplot(create_premises_chart(premises_df))

    st.divider()

    st.subheader("Crime Trend by Neighborhood")
    neighbourhood_df = analyze_crime_by_neighbourhood(cleaned_df)
    st.pyplot(create_crime_by_neighborhood_trend(neighbourhood_df))

    st.divider()

    st.subheader("Geographic Crime Density Heatmap")
    st.write("Interactive map showing spatial distribution across Toronto neighborhoods.")

    try:
        geo_map_fig = create_neighborhood_geo_map(
            neighbourhood_df,
            "data/toronto_neighbourhoods_140.geojson"
        )

        st.plotly_chart(geo_map_fig, use_container_width=True)

    except FileNotFoundError:
        st.error(
            "Error: Could not locate 'data/toronto_neighbourhoods_140.geojson'. "
            "Please ensure the file is present in your data directory."
        )

    except Exception as e:
        st.error(f"Failed to generate geographic heatmap: {e}")
        st.info(
            "Hint: Verify that the GeoJSON feature key matches the neighborhood field."
        )

    st.divider()

    st.subheader("📍 Crime Hotspot Map")
    st.write("Geographic distribution of individual crime incidents across Toronto.")

    try:
        hotspot_df = get_hotspot_data(cleaned_df)
        st.map(hotspot_df, latitude=LATITUDE, longitude=LONGITUDE)
    except ValueError as e:
        st.error(f"Could not generate hotspot map: {e}")

if __name__ == "__main__":
    run_dashboard()