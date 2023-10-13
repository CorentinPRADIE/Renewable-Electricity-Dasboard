import streamlit as st
import pandas as pd

# From app_modules/charts.py
from app_modules.charts import (
    display_combined_chart,
    display_combined_energy_chart,
    create_energy_region_pie_chart,
)

# From app_modules/map.py
from app_modules.map import display_map

# From app_modules/sidebar.py
from app_modules.sidebar import display_date_filter_sidebar


# From app_modules/filter.py
from app_modules.filter import (
    filter_dataframe_by_date,
    filter_dataframe_by_energy_type,
    filter_dataframe_by_region,
    compute_regional_energy_statistics,
)

from app_modules.explanation import (
    ALL_ENERGY_TAB_EXPLANATION,
    SPECIFIC_ENERGY_TAB_EXPLANATION,
)


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


def display_energy_overview_tab(
    regions_data, filtered_data, energy_type, start_date, end_date
):
    """
    Display the Energy Overview tab with the map, combined chart, and regional data table.

    :param regions_data: DataFrame containing data grouped by regions.
    :param filtered_data: DataFrame filtered based on user selection.
    :param energy_type: String representing the selected energy type.
    :param start_date: Start date selected by the user.
    :param end_date: End date selected by the user.
    :param key: Unique key used by Streamlit components.
    """
    col1, col2 = st.columns([0.25, 0.75])

    with col1:
        st.write("")
        st.write("")
        st.write("")
        # Displaying the map visualization
        display_map(regions_data, energy_type, start_date, end_date, key=energy_type)
        filtered_data_by_region = filter_dataframe_by_region(
            filtered_data, st.session_state["region"]
        )

    with col2:
        # Displaying combined chart visualization
        display_combined_chart(
            filtered_data_by_region,
            st.session_state["region"],
            width=1000,
            height=500,
            time_interval=st.session_state.get("time_interval", "Yearly"),
        )
        sub_col1, sub_col2, sub_col3 = st.columns([0.4, 0.35, 0.15])
        with sub_col2:
            st.selectbox(
                "Choose Time Aggregation:",
                ("Yearly", "Monthly"),
                key="time_interval",
                label_visibility="hidden",
            )

    # Removing columns ending with '_millions' and displaying the table
    cols_to_drop = [col for col in regions_data.columns if col.endswith("_millions")]
    st.write("Region's stats :")
    st.dataframe(format_dataframe(regions_data), height=463, use_container_width=True)

    st.write("")
    st.markdown(ALL_ENERGY_TAB_EXPLANATION)


def display_specific_energy_tab(
    regions_data, filtered_data_by_energy, energy_type, start_date, end_date, key
):
    """
    Displays the tab for specific energy types with relevant visualizations and data.

    :param regions_data: DataFrame containing data grouped by regions.
    :param filtered_data_by_energy: DataFrame filtered by the selected energy type.
    :param energy_type: String representing the selected energy type.
    :param start_date: Start date selected by the user.
    :param end_date: End date selected by the user.
    :param key: Unique key used by Streamlit components.
    """
    col1, col2 = st.columns([0.25, 0.75])

    with col1:
        # Displaying map and pie chart visualizations
        display_map(regions_data, energy_type, start_date, end_date, key)
        filtered_data_by_energy_by_region = filter_dataframe_by_region(
            filtered_data_by_energy, st.session_state["region"]
        )

    with col2:
        # Displaying combined energy chart and time aggregation selection
        display_combined_energy_chart(
            filtered_data_by_energy_by_region,
            st.session_state["region"],
            energy_type,
            st.session_state.get("time_interval", "Yearly"),
        )
        sub_col1, sub_col2 = st.columns([0.48, 0.52])
        with sub_col1:
            st.selectbox(
                "Choose Time Aggregation:",
                ("Yearly", "Monthly"),
                key="time_interval",
                label_visibility="hidden",
            )

    col3, col4 = st.columns([0.5, 0.5])
    with col3:
        fig = create_energy_region_pie_chart(regions_data, energy_type, 5)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.write("Region's stats :")

        cols_to_drop = [
            col for col in regions_data.columns if col.endswith("_millions")
        ]
        energy_cols = ["region", "total_volume"] + [
            col
            for col in regions_data.drop(cols_to_drop, axis=1)
            if col.startswith(energy_type)
        ]
        st.dataframe(regions_data.drop(cols_to_drop, axis=1)[energy_cols], height=458)
    st.write("")
    st.write(SPECIFIC_ENERGY_TAB_EXPLANATION.replace("[Energy Type]", energy_type))


def adjust_selectbox_position():
    """Adjusts the positioning of the selectbox by applying custom CSS."""
    st.markdown(
        """
        <style>
        [data-baseweb="select"] {
            margin-top: -70px;
        }
        .leaflet-bottom {
            display: none;
            visibility: hidden !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    """
    Main function to load data, display sidebar, and render selected energy type tab.
    """
    st.set_page_config(
        layout="wide",
        page_title="Renewable Electricity App",
        page_icon="🌎",
    )
    adjust_selectbox_position()
    st.markdown(
        """
        ### Welcome to the Renewable Electricity App 🌎

        Explore comprehensive insights into France's renewable electricity data, with a particular 
        focus on four main energy types: Onshore Wind, Hydropower, Solar, and Geothermal. Navigate 
        through the visualizations and interact with the data to uncover trends, correlations, and 
        patterns in the energy landscape across different regions and timeframes.

        #### How to Navigate:
        - **Choose an Energy Type**: Select an energy type from the dropdown menu to explore specific visualizations and insights.
        - **Sidebar Filters**: Utilize the date filter in the sidebar to view data within a specific timeframe.
        - **Interactive Maps and Charts**: Hover over maps and charts for detailed data points, and click on map regions to refine your data view.
        - **Detailed Insights**: Scroll down for detailed visual representations and statistics pertaining to your selected energy type and date range.

        Dive into the wealth of data and explore the evolution of renewable energy in various regions across France. 
        Whether you're interested in the general overview or specifics of each energy type, the dashboard is designed 
        to cater to a wide spectrum of informational needs.
        """
    )

    # Loading and formatting the data
    dataset = pd.read_csv("data/France_Region_Auction_Data.csv")
    dataset["date"] = pd.to_datetime(dataset["date"], format="%Y-%m")

    # Displaying sidebar and filtering data based on user selection
    start_date, end_date = display_date_filter_sidebar(dataset)
    filtered_data = filter_dataframe_by_date(dataset, start_date, end_date)
    regions_data = compute_regional_energy_statistics(filtered_data)

    # Creating a dropdown for energy type selection and displaying the corresponding tab
    st.subheader("Choose an Energy Type:")
    st.write("")
    st.write("")
    selected_energy_type = st.selectbox(
        "Choose an Energy Type:",
        ["All Energy Types", "Onshore Wind", "Hydropower", "Solar", "Geothermal"],
        label_visibility="hidden",
    )
    if selected_energy_type == "All Energy Types":
        st.title("All Energy Types: Onshore Wind, Hydropower, Solar, and Geothermal")
        display_energy_overview_tab(
            regions_data, filtered_data, "All Renewables", start_date, end_date
        )
    else:
        st.title(selected_energy_type)
        st.write("")
        st.write("")
        st.write("")
        filtered_data_by_energy = filter_dataframe_by_energy_type(
            filtered_data, selected_energy_type
        )
        display_specific_energy_tab(
            regions_data,
            filtered_data_by_energy,
            selected_energy_type,
            start_date,
            end_date,
            key=selected_energy_type,
        )
    adjust_selectbox_position()


if __name__ == "__main__":
    main()
