import pandas as pd
import streamlit as st


def filter_dataframe_by_date(df, start_date, end_date):
    """
    Filters a DataFrame to include only rows where the 'date' column is within the specified date range.

    Args:
        df (pd.DataFrame): The original DataFrame to be filtered.
        start_date (datetime): The start date of the filtering range.
        end_date (datetime): The end date of the filtering range.

    Returns:
        pd.DataFrame: A new DataFrame consisting only of rows within the specified date range.
    """
    mask = (df["date"] >= start_date) & (df["date"] <= end_date)
    return df[mask]


def filter_dataframe_by_region(df, region):
    """
    Filters a DataFrame to include only rows where the 'region' column matches the specified region.

    Args:
        df (pd.DataFrame): The original DataFrame to be filtered.
        region (str): The target region to filter by.

    Returns:
        pd.DataFrame: If 'All Regions' is selected, returns the original DataFrame;
                      otherwise, returns a DataFrame consisting only of rows where the 'region' column matches the specified region.
    """
    return df if region == "All Regions" else df[df["region"] == region]


def filter_dataframe_by_energy_type(df, energy_type):
    """
    Filters a DataFrame to include only rows where the 'energy_type' column matches the specified energy type.

    Args:
        df (pd.DataFrame): The original DataFrame to be filtered.
        energy_type (str): The target energy type to filter by.

    Returns:
        pd.DataFrame: If an empty string is provided for energy_type, returns the original DataFrame;
                      otherwise, returns a DataFrame consisting only of rows where the 'energy_type' column matches the specified energy type.
    """
    return df if energy_type == "" else df[df["energy_type"] == energy_type]


def compute_regional_energy_statistics(filtered_df):
    """
    Aggregates energy statistics at the regional level, computing total volumes and percentages for each energy type.

    Args:
        filtered_df (pd.DataFrame): The DataFrame containing energy data to be aggregated.

    Returns:
        pd.DataFrame: A new DataFrame with aggregated energy statistics at the regional level.
    """
    energy_types = filtered_df["energy_type"].unique()
    total_volume_df = (
        filtered_df.groupby("region")
        .agg(total_volume=("total_volume_sold", "sum"))
        .reset_index()
    )
    total_volume_df["total_volume_millions"] = (
        total_volume_df["total_volume"] / 1_000_000
    )

    # Iterate over each unique energy type and merge the corresponding aggregated data into the regions_df DataFrame
    regions_df = total_volume_df
    for energy_type in energy_types:
        energy_df = filtered_df[filtered_df["energy_type"] == energy_type]
        grouped_df = (
            energy_df.groupby("region")
            .agg(**{f"{energy_type}_total_volume": ("total_volume_sold", "sum")})
            .reset_index()
        )
        grouped_df[f"{energy_type}_total_volume_millions"] = (
            grouped_df[f"{energy_type}_total_volume"] / 1_000_000
        )
        grouped_df[f"{energy_type}_percentage"] = (
            grouped_df[f"{energy_type}_total_volume"] / regions_df["total_volume"]
        ) * 100
        regions_df = pd.merge(regions_df, grouped_df, on="region", how="left")

    return regions_df



def format_volume(number):
    """
    Format the volume numbers to a readable format using 'k' for thousands and 'M' for millions.
    Appends the Euro symbol at the end.

    Args:
    number (float or int): The number to format

    Returns:
    str: The formatted string
    """
    if abs(number) >= 1_000_000:  # Check for millions
        return f"{number/1_000_000:.2f} M€"
    elif abs(number) >= 1_000:  # Check for thousands
        return f"{number/1_000:.2f} k€"
    else:
        return f"{number:.2f}€"


def format_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Format the dataframe columns: append a Euro sign for columns ending with "volume"
    and a percentage sign for columns ending with "percentage".

    Args:
    df (pd.DataFrame): The input DataFrame

    Returns:
    pd.DataFrame: The formatted DataFrame
    """
    formatted_df = df.copy()

    # Drop columns ending with "_millions"
    cols_to_drop = [col for col in df.columns if col.endswith("_millions")]
    formatted_df = formatted_df.drop(cols_to_drop, axis=1)

    # Sort by total_volume
    formatted_df = formatted_df.sort_values(
        by="total_volume", ascending=False
    ).reset_index(drop=True)

    # Iterate through each column in the dataframe
    for col in formatted_df.columns:
        if col.endswith("_total_volume") or col == "total_volume":
            # If column ends with "_total_volume" or is "total_volume", apply the format_volume function
            formatted_df[col] = formatted_df[col].apply(format_volume)
            # Rename the column to remove the suffix
            formatted_df.rename(
                columns={col: col.replace("_total_volume", "")}, inplace=True
            )
        elif col.endswith("_percentage"):
            # If column ends with "_percentage", append percentage sign to each value
            formatted_df[col] = formatted_df[col].apply(lambda x: f"{x:.2f}%")
            # Rename the column to replace the suffix with ' %'
            formatted_df.rename(
                columns={col: col.replace("_percentage", " %")}, inplace=True
            )

    return formatted_df