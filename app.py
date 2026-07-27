from src.data_loader import (load_data, data_preview)
from src.data_cleaning import (clean_data, missing_value_summary, invalid_coordinate_count, nsa_neighbourhood_count, numeric_summary)
from src.summary_analysis import (
    get_total_incidents,
    get_category_counts,
    get_division_summary,
    analyze_by_hour,
    identify_peak_hours,
    analyze_by_hour_and_category,
    analyze_crime_by_neighbourhood,
    analyze_crime_trends_over_time,
    analyze_crime_by_division,
    analyze_crime_by_premises_type,
    analyze_commercial_residential_trends
)

def main():

    # Load dataset
    df = load_data(
        "data/Toronto_Crime_Indicators.csv"
    )

    print("Dataset Loaded Successfully")

    print("\nDataset Shape")
    print(df.shape)

    print("\nDataset Preview")
    print(data_preview(df))

    # BEFORE CLEANING
    print("\nBEFORE CLEANING")
    print("------------------------")

    print("\nMissing Values")
    print(missing_value_summary(df))

    print("\nInvalid Coordinates")
    print(invalid_coordinate_count(df))

    print("\nNSA Records")
    print(nsa_neighbourhood_count(df))


    # Clean dataset
    cleaned_df = clean_data(df)

    # AFTER CLEANING
    print("\nAFTER CLEANING")
    print("------------------------")

    print("\nDataset Shape")
    print(cleaned_df.shape)

    print("\nMissing Values")
    print(missing_value_summary(cleaned_df))

    print("\nInvalid Coordinates")
    print(invalid_coordinate_count(cleaned_df))

    print("\nNSA Records")
    print(nsa_neighbourhood_count(cleaned_df))

    print("\nSummary Statistics")
    print(numeric_summary(cleaned_df))
    
    # US#3 - Crime Summary Statistics
    print("\nCRIME SUMMARY STATISTICS")
    print("------------------------")

    print("\nTotal Incidents")
    print(get_total_incidents(cleaned_df))

    print("\nIncidents by Crime Category")
    print(get_category_counts(cleaned_df))

    print("\nIncidents by Police Division")
    print(get_division_summary(cleaned_df))
    
    # US#4 - Crimes by Hour of Day
    print("\nCRIMES BY HOUR OF DAY")
    print("------------------------")

    print("\nHourly Incident Counts")
    print(analyze_by_hour(cleaned_df))

    print("\nPeak Crime Hours")
    print(identify_peak_hours(cleaned_df))
    
    print("\nCrimes by Hour and Category")
    print(analyze_by_hour_and_category(cleaned_df))

    # US#5 - Crime by Neighborhood
    print("\nCrime Grouped by Neighborhood")
    analyze_crime_by_neighbourhood(cleaned_df, True, 10)

    # US#8 - Crime Trends Over Time
    print("\nCRIME TRENDS OVER TIME")
    print("------------------------")

    print("\nMonthly/Yearly Crime Trends")
    print(analyze_crime_trends_over_time(cleaned_df))

    # US#9 - Police Division Activity
    print("\nPOLICE DIVISION ACTIVITY")
    print("------------------------")

    print("\nCrime by Division")
    print(analyze_crime_by_division(cleaned_df))

    # US#10 - Premises Type Analysis
    print("\nPREMISES TYPE ANALYSIS")
    print("------------------------")

    print("\nCrime by Premises Type")
    print(analyze_crime_by_premises_type(cleaned_df))

    print("\nCommercial and Residential Crime Trends")
    print(analyze_commercial_residential_trends(cleaned_df))


if __name__ == "__main__":
    main()