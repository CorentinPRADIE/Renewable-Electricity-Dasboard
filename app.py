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
    format_dataframe
)

# From app_modules/explanation.py
from app_modules.explanation import (
    WELCOME_MESSAGE,
    ALL_ENERGY_TAB_EXPLANATION,
    SPECIFIC_ENERGY_TAB_EXPLANATION,
)

from app_modules.helpers import adjust_selectbox_position

# --------------------------------------------
# --       ALL ENERGY TYPE DISPLAY          --
# --------------------------------------------

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

   
    st.subheader("Region's stats ranked by volume sold:")
    st.dataframe(format_dataframe(regions_data), height=463, use_container_width=True)

    st.write("---")
    st.markdown(ALL_ENERGY_TAB_EXPLANATION)


# -----------------------------------------------
# --         ENERGY SPECIFIC TYPE DISPLAY      --
# -----------------------------------------------


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
        st.subheader(f"Region's stats ranked by {energy_type} volume:")

        cols_to_drop = [
            col for col in regions_data.columns if col.endswith("_millions")
        ]
        energy_cols = ["region"] + [
            col
            for col in regions_data.drop(cols_to_drop, axis=1)
            if col.startswith(energy_type)
        ] + ["total_volume"]
        regions_data = regions_data.drop(cols_to_drop, axis=1)[energy_cols]
        regions_data = regions_data.sort_values(by=f'{energy_type}_total_volume', ascending=False).reset_index(drop=True)
        st.dataframe(regions_data, height=458)
    st.write('---')
    st.write(SPECIFIC_ENERGY_TAB_EXPLANATION.replace("[Energy Type]", energy_type))


def main():
    """
    Main function to load data, display sidebar, and render selected energy type tab.
    """
    st.set_page_config(
        layout="wide",
        page_title="Renewable Electricity Dashboard",
        page_icon="🌎",
    )
    adjust_selectbox_position()
    st.markdown(WELCOME_MESSAGE)

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

    # All Energy Tab
    if selected_energy_type == "All Energy Types":
        st.write('---')
        st.title("All Energy Types: Onshore Wind, Hydropower, Solar, and Geothermal")
        display_energy_overview_tab(
            regions_data, filtered_data, "All Renewables", start_date, end_date
        )

    # Energy Specific tab
    else:
        st.write('---')
        st.title('Selected Energy Type : ' + selected_energy_type)
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
    st.subheader('Author : Corentin PRADIE')
    st.subheader('Github : [CorentinPRADIE](https://github.com/CorentinPRADIE)')


if __name__ == "__main__":
    main()
