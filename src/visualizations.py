import json

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import plotly.express as px

from src.constants import (
    OCC_HOUR
)


# Create bar chart of crime incidents by hour of day
def create_hourly_chart(df_hourly):

    fig, ax = plt.subplots(figsize=(14, 6))

    ax.bar(
        df_hourly[OCC_HOUR],
        df_hourly["count"],
        color="steelblue",
        edgecolor="white"
    )

    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Number of Incidents")
    ax.set_title("Crime Incidents by Hour of Day")
    ax.set_xticks(range(0, 24))

    plt.tight_layout()

    return fig


# Create grouped line chart of crimes by hour and category
def create_hourly_category_chart(df_hourly_category):

    fig, ax = plt.subplots(figsize=(14, 6))

    categories = df_hourly_category[
        "CSI_CATEGORY"
    ].unique()

    colors = [
        "steelblue",
        "coral",
        "seagreen",
        "mediumpurple",
        "goldenrod"
    ]

    for i, category in enumerate(categories):

        category_data = df_hourly_category[
            df_hourly_category["CSI_CATEGORY"] == category
        ]

        ax.plot(
            category_data[OCC_HOUR],
            category_data["count"],
            label=category,
            color=colors[i],
            linewidth=2,
            marker="o",
            markersize=4
        )

    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Number of Incidents")
    ax.set_title("Crime Incidents by Hour of Day and Category")
    ax.set_xticks(range(0, 24))
    ax.legend(title="Crime Category")

    plt.tight_layout()

    return fig


# Create line chart for yearly crime trends over time
def create_crime_trend_chart(df_trends):

    yearly_trends = (
        df_trends.groupby("OCC_YEAR")["count"]
        .sum()
        .reset_index()
        .sort_values("OCC_YEAR")
    )

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(
        yearly_trends["OCC_YEAR"],
        yearly_trends["count"],
        marker="o"
    )

    ax.set_title("Crime Trends Over Time")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Incidents")
    ax.set_xticks(yearly_trends["OCC_YEAR"])

    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig


# Create division activity chart
def create_division_chart(df_division):

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(
        df_division["DIVISION"],
        df_division["count"]
    )

    ax.set_title("Crime Activity by Division")
    ax.set_xlabel("Division")
    ax.set_ylabel("Incident Count")

    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig


# Create premises type chart
def create_premises_chart(df_premises):

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(
        df_premises["PREMISES_TYPE"],
        df_premises["count"]
    )

    ax.set_title("Crime Incidents by Premises Type")
    ax.set_xlabel("Premises Type")
    ax.set_ylabel("Incident Count")

    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig


# Create neighborhood crime trend chart
def create_crime_by_neighborhood_trend(neighbourhood_df):

    plot_df = neighbourhood_df.copy()

    if plot_df.index.name is not None:
        plot_df = plot_df.reset_index()

    top_neighbourhoods = plot_df.sort_values(
        "Total",
        ascending=False
    ).head(10)

    fig, ax = plt.subplots(figsize=(14, 6))

    ax.bar(
        top_neighbourhoods["NEIGHBOURHOOD_140"],
        top_neighbourhoods["Total"]
    )

    ax.set_title("Top 10 Neighborhoods by Crime Incidents")
    ax.set_xlabel("Neighborhood")
    ax.set_ylabel("Total Incidents")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    return fig


# Create geographic neighborhood heatmap
def create_neighborhood_geo_map(
    neighbourhood_df,
    geojson_path="data/toronto_neighbourhoods_140.geojson"
):

    with open(geojson_path, "r") as f:
        toronto_geo = json.load(f)

    if neighbourhood_df.index.name is not None:
        df_plot = neighbourhood_df.reset_index()
    else:
        df_plot = neighbourhood_df.copy()

    fig = px.choropleth(
        df_plot,
        geojson=toronto_geo,
        locations="NEIGHBOURHOOD_140",
        featureidkey="properties.AREA_NAME",
        color="Total",
        color_continuous_scale="YlOrRd",
        labels={"Total": "Total Incidents"},
        title="Geographic Density Heatmap of Incidents by Neighborhood"
    )

    fig.update_geos(
        fitbounds="locations",
        visible=False
    )

    fig.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        height=600
    )

    return fig