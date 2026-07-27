import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from src.constants import (
    NEIGHBOURHOOD,
    OCC_YEAR,
    LATITUDE,
    LONGITUDE
)

from src.summary_analysis import (
    get_total_incidents,
    get_category_counts,
    get_division_summary,
    analyze_by_hour,
    identify_peak_hours,
    analyze_crime_trends_over_time,
    analyze_crime_by_division,
    analyze_crime_by_premises_type,
    analyze_commercial_residential_trends,
    analyze_crime_by_neighbourhood,
    filter_valid_coordinates,
    get_hotspot_data
)


def sample_df():

    return pd.DataFrame({
        "CSI_CATEGORY": [
            "Assault",
            "Robbery",
            "Assault",
            "Auto Theft",
            "Robbery",
            "Assault"
        ],
        "DIVISION": [
            "D11",
            "D12",
            "D11",
            "D13",
            "D11",
            "D12"
        ],
        "OCC_HOUR": [1, 2, 3, 1, 23, 3]
    })


def test_get_total_incidents():

    df = sample_df()

    result = get_total_incidents(df)

    assert result == 6


def test_get_category_counts():

    df = sample_df()

    result = get_category_counts(df)

    assert "CSI_CATEGORY" in result.columns
    assert "count" in result.columns
    assert "percentage" in result.columns
    assert result["count"].sum() == 6


def test_get_division_summary():

    df = sample_df()

    result = get_division_summary(df)

    assert "DIVISION" in result.columns
    assert "count" in result.columns
    assert result["count"].sum() == 6


def test_analyze_by_hour():

    df = sample_df()

    result = analyze_by_hour(df)

    assert "OCC_HOUR" in result.columns
    assert "count" in result.columns
    assert result["OCC_HOUR"].is_monotonic_increasing


def test_identify_peak_hours():

    df = sample_df()

    result = identify_peak_hours(df, n=2)

    assert len(result) == 2
    assert result["count"].iloc[0] >= result["count"].iloc[1]


def test_analyze_crime_trends_over_time():

    df = pd.DataFrame({
        "OCC_YEAR": [2023, 2023, 2024, 2024],
        "OCC_MONTH": ["January", "February", "January", "February"]
    })

    result = analyze_crime_trends_over_time(df)

    assert "count" in result.columns
    assert len(result) == 4


def test_analyze_crime_by_division():

    df = pd.DataFrame({
        "DIVISION": ["D11", "D11", "D12", "D13"]
    })

    result = analyze_crime_by_division(df)

    assert "DIVISION" in result.columns
    assert "count" in result.columns
    assert result["count"].sum() == 4


def test_analyze_crime_by_premises_type():

    df = pd.DataFrame({
        "PREMISES_TYPE": [
            "Commercial",
            "Commercial",
            "Apartment",
            "House"
        ]
    })

    result = analyze_crime_by_premises_type(df)

    assert "PREMISES_TYPE" in result.columns
    assert "count" in result.columns
    assert result["count"].sum() == 4


def test_analyze_commercial_residential_trends():

    df = pd.DataFrame({
        "OCC_YEAR": [2023, 2023, 2024, 2024],
        "PREMISES_TYPE": [
            "Commercial",
            "Apartment",
            "Commercial",
            "House"
        ]
    })

    result = analyze_commercial_residential_trends(df)

    assert "count" in result.columns
    assert result["count"].sum() == 4


def crime_neighbourhood_sample_df():

    return pd.DataFrame({
        NEIGHBOURHOOD: [
            "Church-Yonge Corridor",
            "Church-Yonge Corridor",
            "Moss Park",
            "Church-Yonge Corridor",
            "Moss Park",
            "Annex",
        ],
        OCC_YEAR: [2024, 2024, 2024, 2025, 2025, 2025],
    })


def test_analyze_crime_by_neighbourhood():

    df = crime_neighbourhood_sample_df()

    result = analyze_crime_by_neighbourhood(df, print_summary=False)

    assert "Total" in result.columns
    assert len(result) == 3

    assert result["Total"].iloc[0] >= result["Total"].iloc[1]
    assert result["Total"].iloc[1] >= result["Total"].iloc[2]

    expected_data = {
        2024: [2, 1, 0],
        2025: [1, 1, 1],
        "Total": [3, 2, 1]
    }

    expected_df = pd.DataFrame(
        expected_data,
        index=pd.Index(
            ["Church-Yonge Corridor", "Moss Park", "Annex"],
            name=NEIGHBOURHOOD
        )
    )

    expected_df.columns.name = OCC_YEAR

    assert_frame_equal(result, expected_df)


def test_analyze_crime_print_summary():

    df = crime_neighbourhood_sample_df()

    result = analyze_crime_by_neighbourhood(
        df,
        print_summary=True,
        top_neighbourhood=2
    )

    assert result is None


def test_analyze_crime_empty_dataframe():

    empty_df = pd.DataFrame(columns=[NEIGHBOURHOOD, OCC_YEAR])

    result = analyze_crime_by_neighbourhood(
        empty_df,
        print_summary=False
    )

    assert isinstance(result, pd.DataFrame)
    assert result.empty
    assert list(result.columns) == ['Total']

# Test for coordinate validity verification
def coordinate_sample_df():
    """Sample DataFrame with mix of valid and invalid coordinates."""
    return pd.DataFrame({
        "CSI_CATEGORY": ["Assault", "Robbery", "Auto Theft", "Assault"],
        LATITUDE:       [43.70,     0,          43.65,        0],
        LONGITUDE:      [-79.38,    0,          -79.50,       -79.38],
    })


def test_filter_valid_coordinates_removes_zero_rows():
    df = coordinate_sample_df()
    result = filter_valid_coordinates(df)
    assert len(result) == 2


def test_filter_valid_coordinates_keeps_nonzero_rows():
    df = coordinate_sample_df()
    result = filter_valid_coordinates(df)
    assert (result[LATITUDE] != 0).all()
    assert (result[LONGITUDE] != 0).all()


def test_filter_valid_coordinates_does_not_mutate_input():
    df = coordinate_sample_df()
    original_len = len(df)
    filter_valid_coordinates(df)
    assert len(df) == original_len


def test_filter_valid_coordinates_empty_df_returns_empty():
    df = pd.DataFrame(columns=[LATITUDE, LONGITUDE])
    result = filter_valid_coordinates(df)
    assert result.empty


def test_get_hotspot_data_raises_on_all_invalid():
    df = pd.DataFrame({
        LATITUDE:  [0, 0],
        LONGITUDE: [0, 0],
    })
    with pytest.raises(ValueError):
        get_hotspot_data(df)


def test_get_hotspot_data_respects_sample_size():
    df = pd.DataFrame({
        LATITUDE:  [43.70] * 100,
        LONGITUDE: [-79.38] * 100,
    })
    result = get_hotspot_data(df, sample_size=50)
    assert len(result) == 50


def test_get_hotspot_data_returns_valid_coordinates_only():
    df = coordinate_sample_df()
    result = get_hotspot_data(df)
    assert (result[LATITUDE] != 0).all()
    assert (result[LONGITUDE] != 0).all()
