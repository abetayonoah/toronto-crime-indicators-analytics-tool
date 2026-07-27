import pandas as pd

from src.constants import (
    CSI_CATEGORY,
    DIVISION,
    OCC_HOUR,
    OCC_YEAR,
    OCC_MONTH,
    NEIGHBOURHOOD,
    PREMISES_TYPE,
    LATITUDE,
    LONGITUDE
)

# Get total number of crime incidents
def get_total_incidents(df):

    return len(df)

# Get incident counts grouped by crime category
def get_category_counts(df):

    counts = (
        df[CSI_CATEGORY]
        .value_counts()
        .reset_index()
    )

    counts.columns = [CSI_CATEGORY, "count"]

    counts["percentage"] = (
        counts["count"] / counts["count"].sum() * 100
    ).round(2)

    return counts

# Get incident counts grouped by police division
def get_division_summary(df):

    summary = (
        df[DIVISION]
        .value_counts()
        .reset_index()
    )

    summary.columns = [DIVISION, "count"]

    return summary

# Group incidents by hour of day sorted chronologically
def analyze_by_hour(df):

    hourly = (
        df.groupby(OCC_HOUR)
        .size()
        .reset_index(name="count")
    )

    hourly = hourly.sort_values(
        OCC_HOUR
    ).reset_index(drop=True)

    return hourly


# Identify top N peak crime hours
def identify_peak_hours(df, n=3):

    hourly = analyze_by_hour(df)

    peak = hourly.nlargest(
        n, "count"
    ).reset_index(drop=True)

    return peak

# Group incidents by hour and crime category
def analyze_by_hour_and_category(df):

    hourly_category = (
        df.groupby([OCC_HOUR, CSI_CATEGORY])
        .size()
        .reset_index(name="count")
    )

    hourly_category = hourly_category.sort_values(
        OCC_HOUR
    ).reset_index(drop=True)

    return hourly_category

# Placeholder code
def analyze_crime_by_neighbourhood(df, print_summary=False, top_neighbourhood=5):
    # 1. Group by neighborhood and occurrence year, counting EVENT_UNIQUE_IDs
    grouped_df = df.groupby([NEIGHBOURHOOD, OCC_YEAR]).size().reset_index(name="Incident_Count")

    # 2. Pivot the table so years become the columns
    pivot_df = grouped_df.pivot(
        index=NEIGHBOURHOOD,
        columns=OCC_YEAR,
        values="Incident_Count"
    )

    # 3. Fill any missing values (years where a neighborhood had 0 crimes) with 0
    pivot_df = pivot_df.fillna(0).astype(int)

    # 4. Add a Total column summarizing all years combined
    pivot_df["Total"] = pivot_df.sum(axis=1)

    # 5. Sort the table so the highest-crime neighborhoods appear first
    pivot_df = pivot_df.sort_values(by="Total", ascending=False)
    # Reset index so 'NEIGHBOURHOOD' becomes a standard display column
    pivot_df.reset_index()

    # 6. Format the dataframe for printing
    print_df = pivot_df.copy()
    print_df.columns.name = None
    print_df.reset_index(inplace=True)

    # Print Result
    if print_summary:
        print(f"\nTop {top_neighbourhood} Neighborhoods with Highest Incident Count")
        print(print_df[[NEIGHBOURHOOD, 'Total']].head(top_neighbourhood))
        return None
    else:
        return pivot_df
    
# Group crime incidents by year and month
def analyze_crime_trends_over_time(df):
    trends = (
        df.groupby([OCC_YEAR, OCC_MONTH])
        .size()
        .reset_index(name="count")
    )

    month_order = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }

    trends["month_number"] = trends[OCC_MONTH].map(month_order)

    trends = trends.sort_values(
        [OCC_YEAR, "month_number"]
    ).reset_index(drop=True)

    return trends


# Group crime incidents by police division
def analyze_crime_by_division(df):
    division_summary = (
        df[DIVISION]
        .value_counts()
        .reset_index()
    )

    division_summary.columns = [DIVISION, "count"]

    return division_summary


# Group crime incidents by premises type
def analyze_crime_by_premises_type(df):
    premises_summary = (
        df[PREMISES_TYPE]
        .value_counts()
        .reset_index()
    )

    premises_summary.columns = [PREMISES_TYPE, "count"]

    return premises_summary


# Compare commercial and residential crime trends by year
def analyze_commercial_residential_trends(df):
    filtered_df = df[
        df[PREMISES_TYPE].isin(["Commercial", "Apartment", "House"])
    ]

    trends = (
        filtered_df.groupby([OCC_YEAR, PREMISES_TYPE])
        .size()
        .reset_index(name="count")
    )

    trends = trends.sort_values(
        [OCC_YEAR, PREMISES_TYPE]
    ).reset_index(drop=True)

    return trends

def filter_valid_coordinates(df):
    """Remove rows where latitude or longitude is zero."""
    return df[(df[LATITUDE] != 0) & (df[LONGITUDE] != 0)].copy()

def get_hotspot_data(df, sample_size=50_000):
    """Return a filtered and sampled DataFrame ready for map rendering."""
    valid_df = filter_valid_coordinates(df)

    if valid_df.empty:
        raise ValueError("No valid coordinates found in the dataset.")

    if sample_size and len(valid_df) > sample_size:
        valid_df = valid_df.sample(n=sample_size, random_state=42)

    return valid_df

