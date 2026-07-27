import pandas as pd

from src.data_cleaning import (
    remove_duplicates,
    remove_invalid_coordinates,
    remove_nsa_neighbourhoods,
    handle_missing_values,
    format_dates,
    format_hour_column,
    invalid_coordinate_count,
    nsa_neighbourhood_count
)


# Test duplicate removal
def test_remove_duplicates():

    df = pd.DataFrame({
        "EVENT_UNIQUE_ID": [1, 1, 2]
    })

    cleaned = remove_duplicates(df)

    assert len(cleaned) == 2


# Test invalid coordinate removal
def test_remove_invalid_coordinates():

    df = pd.DataFrame({
        "LAT_WGS84": [43.7, 0],
        "LONG_WGS84": [-79.4, 0]
    })

    cleaned = remove_invalid_coordinates(df)

    assert len(cleaned) == 1


# Test NSA neighbourhood removal
def test_remove_nsa_neighbourhoods():

    df = pd.DataFrame({
        "NEIGHBOURHOOD_140": [
            "Downtown",
            "NSA"
        ]
    })

    cleaned = remove_nsa_neighbourhoods(df)

    assert "NSA" not in cleaned[
        "NEIGHBOURHOOD_140"
    ].values


# Test missing value handling
def test_handle_missing_values():

    df = pd.DataFrame({
        "NEIGHBOURHOOD_140": [
            None,
            "Downtown"
        ]
    })

    cleaned = handle_missing_values(df)

    assert "Unknown" in cleaned[
        "NEIGHBOURHOOD_140"
    ].values


# Test date formatting
def test_format_dates():

    df = pd.DataFrame({
        "REPORT_DATE": ["2024-01-01"],
        "OCC_DATE": ["2024-01-01"]
    })

    cleaned = format_dates(df)

    assert pd.api.types.is_datetime64_any_dtype(
        cleaned["REPORT_DATE"]
    )


# Test hour formatting
def test_format_hour_column():

    df = pd.DataFrame({
        "OCC_HOUR": ["5", "10"]
    })

    cleaned = format_hour_column(df)

    assert cleaned["OCC_HOUR"].dtype != object


# Test invalid coordinate count
def test_invalid_coordinate_count():

    df = pd.DataFrame({
        "LAT_WGS84": [43.7, 0],
        "LONG_WGS84": [-79.4, 0]
    })

    count = invalid_coordinate_count(df)

    assert count == 1


# Test NSA count
def test_nsa_neighbourhood_count():

    df = pd.DataFrame({
        "NEIGHBOURHOOD_140": [
            "NSA",
            "Downtown"
        ]
    })

    count = nsa_neighbourhood_count(df)

    assert count == 1