import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

from app_modules.colors import (
    ENERGY_TYPE_COLORS,
    ENERGY_TYPE_COLOR_GRADIENTS,
)  # Importing custom color mappings

SUPTITLE_FONT_SIZE = 34  # Global constant to maintain uniformity in subtitle font size

# -------------------------------------------------------------
# -- Visualization Functions for All Energy Types (Main Tab) --
# -------------------------------------------------------------


def create_pie_chart(df):
    """
    Function to create a pie chart representation for different energy types in the provided dataframe.

    Args:
        df (pd.DataFrame): The input DataFrame containing energy data.

    Returns:
        plotly.graph_objs.Figure: A pie chart figure visualizing the proportion of different energy types.
    """
    tech_volume = df.groupby("energy_type")["total_volume_sold"].sum().reset_index()
    tech_volume["percent"] = (
        tech_volume["total_volume_sold"] / tech_volume["total_volume_sold"].sum()
    ) * 100

    pie_fig = px.pie(
        tech_volume,
        values="total_volume_sold",
        names="energy_type",
        color="energy_type",
        color_discrete_map=ENERGY_TYPE_COLORS,
    )
    pie_fig.update_traces(textinfo="percent+label")
    return pie_fig


def create_bar_chart(df, time_interval):
    """
    Function to create a bar chart representation for different energy types over time in the provided dataframe.

    Args:
        df (pd.DataFrame): The input DataFrame containing energy data.
        time_interval (str): String denoting the time interval for grouping data; can be 'Monthly' or 'Yearly'.

    Returns:
        plotly.graph_objs.Figure: A bar chart figure visualizing the total volume sold over time.
    """
    df["date"] = pd.to_datetime(df["date"])
    grouped_df = (
        df.groupby(["date", "energy_type"])["total_volume_sold"].sum().reset_index()
    )

    if time_interval == "Yearly":
        grouped_df["year"] = grouped_df["date"].dt.year
        grouped_df = grouped_df.groupby(["year", "energy_type"], as_index=False)[
            "total_volume_sold"
        ].sum()
        x_col = "year"
    else:
        x_col = "date"

    bar_fig = px.bar(
        grouped_df,
        x=x_col,
        y="total_volume_sold",
        color="energy_type",
        color_discrete_map=ENERGY_TYPE_COLORS,
    )
    return bar_fig


def display_combined_chart(df, region, width, height, time_interval):
    """
    Function to create and display a combined chart with pie and bar charts for the provided data.

    Args:
        df (pd.DataFrame): The input DataFrame containing energy data.
        region (str): String representing the region for which the chart is displayed.
        width (int): Integer representing the width of the chart.
        height (int): Integer representing the height of the chart.
        time_interval (str): String representing the time interval for the bar chart; can be 'Monthly' or 'Yearly'.
    """
    pie_fig = create_pie_chart(df)
    bar_fig = create_bar_chart(df, time_interval)

    # Initializing subplot and configuring layout
    fig = make_subplots(
        rows=1,
        cols=2,
        column_widths=[0.5, 0.5],
        subplot_titles=(
            "Proportion of Volume by Energy Type",
            "Total Volume per Energy Type over Time",
        ),
        specs=[[{"type": "domain"}, {"type": "xy"}]],
    )
    for annotation in fig["layout"]["annotations"]:
        annotation["font"] = dict(size=20)

    # Adding traces for pie and bar charts to the subplot
    fig.add_trace(
        go.Pie(
            labels=pie_fig["data"][0]["labels"],
            values=pie_fig["data"][0]["values"],
            textinfo="percent+label",
            name="",
            domain={"column": 0},
            showlegend=False,
            marker_colors=[
                ENERGY_TYPE_COLORS[label] for label in pie_fig["data"][0]["labels"]
            ],
        ),
        row=1,
        col=1,
    )
    for trace in bar_fig["data"]:
        fig.add_trace(trace.update(showlegend=True), row=1, col=2)

    # Updating layout and displaying the combined chart
    fig.update_layout(
        legend_traceorder="reversed",
        height=height,
        width=width,
        barmode="stack",
        title_text=f"{region}",
        title_x=0.3,
        title_font=dict(size=SUPTITLE_FONT_SIZE),
        legend_title_text="Energy Types :",
        legend_font_size=22,
        legend_title_font_size=18,
    )
    st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------------------------
# -- Visualization Functions for Specific Energy Types (Other Tabs) --
# --------------------------------------------------------------------


def create_energy_bar_chart(df, energy_type, time_interval):
    """
    Creates a bar chart representing total volume sold over time for a specific energy type.

    Args:
        df (pd.DataFrame): The filtered input DataFrame containing energy data.
        energy_type (str): String representing the specific energy type.
        time_interval (str): String representing the time interval; can be 'Monthly' or 'Yearly'.

    Returns:
        plotly.graph_objs.Figure: A bar chart figure visualizing the total volume sold over time.
    """
    if df["energy_type"].nunique() != 1:
        raise ValueError("DataFrame should have only one unique value in 'energy_type'")

    grouped_df = df.groupby(["date", "energy_type"], as_index=False)[
        "total_volume_sold"
    ].sum()
    grouped_df["date"] = pd.to_datetime(grouped_df["date"])

    if time_interval == "Yearly":
        grouped_df.set_index("date", inplace=True)
        grouped_df = grouped_df.resample("Y").sum()
        grouped_df.reset_index(inplace=True)

    fig = px.bar(
        grouped_df,
        x="date",
        y="total_volume_sold",
        labels={"total_volume_sold": "Total Volume Sold"},
        title=f"Total Volume Sold Over Time for {energy_type} Energy",
    )
    fig.update_traces(marker_color=ENERGY_TYPE_COLORS.get(energy_type, "grey"))
    return fig


def create_energy_season_bar_chart(df, energy_type):
    """
    Creates a bar chart representing the percentage of total volume sold in different seasons for a specific energy type.

    Args:
        df (pd.DataFrame): The filtered input DataFrame containing energy data.
        energy_type (str): String representing the specific energy type.

    Returns:
        plotly.graph_objs.Figure: A bar chart figure visualizing the percentage of total volume sold in different seasons.
    """
    if df["energy_type"].nunique() != 1:
        raise ValueError("DataFrame should have only one unique value in 'energy_type'")

    seasons_mapping = {
        12: "Winter",
        1: "Winter",
        2: "Winter",
        3: "Spring",
        4: "Spring",
        5: "Spring",
        6: "Summer",
        7: "Summer",
        8: "Summer",
        9: "Autumn",
        10: "Autumn",
        11: "Autumn",
    }
    df["season"] = df["date"].dt.month.map(seasons_mapping)
    grouped_df = df.groupby("season")["total_volume_sold"].sum().reset_index()
    grouped_df["percentage_of_total"] = (
        grouped_df["total_volume_sold"] / df["total_volume_sold"].sum()
    ) * 100
    grouped_df["season"] = grouped_df["season"].astype(
        pd.CategoricalDtype(
            categories=["Winter", "Spring", "Summer", "Autumn"], ordered=True
        )
    )
    grouped_df = grouped_df.sort_values(by="season")

    fig = px.bar(
        grouped_df,
        x="season",
        y="percentage_of_total",
        color="season",
        color_discrete_map={
            "Spring": "green",
            "Summer": "yellow",
            "Winter": "blue",
            "Autumn": "orange",
        },
        labels={"percentage_of_total": "Percentage of Sold Energy", "season": "Season"},
        title=f"Percentage of {energy_type} Sold per Season",
    )
    return fig


def display_combined_energy_chart(df, region, energy_type, time_interval):
    """
    Creates and displays a combined chart with bar charts for the provided data representing a specific energy type.

    Args:
        df (pd.DataFrame): The input DataFrame containing energy data.
        region (str): String representing the region for which the chart is displayed.
        energy_type (str): String representing the specific energy type.
        time_interval (str): String representing the time interval for the bar chart; can be 'Monthly' or 'Yearly'.
    """
    energy_bar_fig = create_energy_bar_chart(df, energy_type, time_interval)
    energy_season_fig = create_energy_season_bar_chart(df, energy_type)

    fig = make_subplots(
        rows=1,
        cols=2,
        column_widths=[0.5, 0.5],
        subplot_titles=(
            f"Total Volume Sold Over Time for {energy_type} Energy",
            f"Percentage of {energy_type} Sold per Season",
        ),
    )
    for trace in energy_season_fig["data"]:
        fig.add_trace(trace.update(width=0.4, showlegend=False), row=1, col=2)
    for trace in energy_bar_fig["data"]:
        fig.add_trace(trace.update(showlegend=False), row=1, col=1)

    fig.update_layout(
        title_text=region, title_x=0.4, title_font=dict(size=SUPTITLE_FONT_SIZE)
    )
    st.plotly_chart(fig, use_container_width=True)


def create_energy_region_pie_chart(region_df, energy_type, n):
    """
    Creates a pie chart visualizing total volume sold by region for a specific energy type.

    Args:
        region_df (pd.DataFrame): The input DataFrame containing energy data.
        energy_type (str): String representing the specific energy type.
        n (int): Integer representing the number of top regions to be displayed separately in the pie chart.

    Returns:
        plotly.graph_objs.Figure: A pie chart figure visualizing the total volume sold by region.
    """
    col_name = energy_type + "_total_volume"
    if col_name not in region_df.columns:
        raise ValueError(f"{col_name} does not exist in the DataFrame")

    # Sort and select data
    sorted_df = region_df.sort_values(by=col_name, ascending=False)
    top_n_df = sorted_df.head(n)

    if len(region_df) > n:
        other_df = pd.DataFrame(
            {
                "region": ["Other regions"],
                col_name: [sorted_df.iloc[n:][col_name].sum()],
            }
        )
        final_df = pd.concat([top_n_df, other_df], ignore_index=True)
    else:
        final_df = top_n_df

    # Get the color scale based on the energy type
    colorscale = px.colors.sequential.__dict__[ENERGY_TYPE_COLOR_GRADIENTS[energy_type]]

    # Select colors evenly spaced across the whole color scale
    selected_colors = [colorscale[i * len(colorscale) // n] for i in range(n)]

    # Assign colors: selected colors for top n and grey for 'Other regions'
    colors = ["grey"] + selected_colors

    fig = px.pie(
        final_df,
        names="region",
        values=col_name,
        title=f"{energy_type} Total Volume Sold by Region",
        height=600,
        category_orders={"region": ["Other regions"] + list(top_n_df["region"])[::-1]},
    )
    fig.update_traces(textinfo="label+percent", showlegend=False, marker_colors=colors)
    return fig
