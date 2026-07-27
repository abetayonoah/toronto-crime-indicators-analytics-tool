import pandas as pd

from src.constants import (
    EVENT_ID,
    NEIGHBOURHOOD,
    LATITUDE,
    LONGITUDE,
    REPORT_DATE,
    OCC_DATE,
    OCC_HOUR
)


# Remove duplicate crime records
def remove_duplicates(df):

    cleaned_df = df.drop_duplicates(
        subset=EVENT_ID
    ).reset_index(drop=True) # VinhT: reset index

    return cleaned_df


# Remove rows with invalid coordinates
def remove_invalid_coordinates(df):

    cleaned_df = df[
        (df[LATITUDE] != 0) &
        (df[LONGITUDE] != 0)
    ]

    return cleaned_df


# Remove NSA neighbourhood records
def remove_nsa_neighbourhoods(df):

    cleaned_df = df[
        df[NEIGHBOURHOOD] != "NSA"
    ]

    return cleaned_df


# Handle missing values
def handle_missing_values(df):

    df[NEIGHBOURHOOD] = df[
        NEIGHBOURHOOD
    ].fillna("Unknown")

    return df


# Convert date columns to datetime
def format_dates(df):

    df[REPORT_DATE] = pd.to_datetime(
        df[REPORT_DATE],
        errors="coerce"
    )

    df[OCC_DATE] = pd.to_datetime(
        df[OCC_DATE],
        errors="coerce"
    )

    return df


# Convert hour column to numeric
def format_hour_column(df):

    df[OCC_HOUR] = pd.to_numeric(
        df[OCC_HOUR],
        errors="coerce"
    )

    return df


# Count invalid coordinates
def invalid_coordinate_count(df):

    invalid_rows = df[
        (df[LATITUDE] == 0) |
        (df[LONGITUDE] == 0)
    ]

    return len(invalid_rows)


# Count NSA neighbourhood records
def nsa_neighbourhood_count(df):

    nsa_rows = df[
        df[NEIGHBOURHOOD] == "NSA"
    ]

    return len(nsa_rows)


# Missing value summary
def missing_value_summary(df):

    return df.isnull().sum()


# Summary statistics
def numeric_summary(df):

    return df.describe()

def dataset_shape(df):

    return df.shape


# Main cleaning pipeline
def clean_data(df):

    df = remove_duplicates(df)

    df = remove_invalid_coordinates(df)

    df = remove_nsa_neighbourhoods(df)

    df = handle_missing_values(df)

    df = format_dates(df)

    df = format_hour_column(df)

    return df