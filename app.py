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


def display_energy_overview_tab(regions_data, filtered_data, energy_type, start_date, end_date):
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
        filtered_data_by_region = filter_dataframe_by_region(filtered_data, st.session_state["region"])

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
            st.selectbox("Choose Time Aggregation:", ("Yearly", "Monthly"), key="time_interval", label_visibility='hidden')
            
    # Removing columns ending with '_millions' and displaying the table
    cols_to_drop = [col for col in regions_data.columns if col.endswith("_millions")]
    st.write(regions_data.drop(cols_to_drop, axis=1).sort_values(by="total_volume", ascending=False).reset_index(drop=True))


def display_specific_energy_tab(regions_data, filtered_data_by_energy, energy_type, start_date, end_date, key):
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
        fig = create_energy_region_pie_chart(regions_data, energy_type, 5)
        st.plotly_chart(fig, use_container_width=True)

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
                "Choose Time Aggregation:", ("Yearly", "Monthly"), key="time_interval", label_visibility='hidden'
            )
        st.write(regions_data)


def adjust_selectbox_position():
    """ Adjusts the positioning of the selectbox by applying custom CSS. """
    st.markdown(
        """
        <style>
        [data-baseweb="select"] {
            margin-top: -70px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def main():
    """
    Main function to load data, display sidebar, and render selected energy type tab.
    """
    st.set_page_config(layout="wide")
    adjust_selectbox_position()

    # Loading and formatting the data
    dataset = pd.read_csv("data/France_Region_Auction_Data.csv")
    dataset["date"] = pd.to_datetime(dataset["date"], format="%Y-%m")

    # Displaying sidebar and filtering data based on user selection
    start_date, end_date = display_date_filter_sidebar(dataset)
    filtered_data = filter_dataframe_by_date(dataset, start_date, end_date)
    regions_data = compute_regional_energy_statistics(filtered_data)

    # Creating a dropdown for energy type selection and displaying the corresponding tab
    st.subheader('Choose an Energy Type:')
    st.write('')
    st.write('')
    selected_energy_type = st.selectbox("Choose an Energy Type:", ["All Energy Types", "Onshore Wind", "Hydropower", "Solar", "Geothermal"], label_visibility='hidden')
    if selected_energy_type == "All Energy Types":
        st.title("All Energy Types: Onshore Wind, Hydropower, Solar, and Geothermal")
        display_energy_overview_tab(regions_data, filtered_data, "All Renewables", start_date, end_date)
    else:
        st.title(selected_energy_type)
        st.write('')
        st.write('')
        st.write('')
        filtered_data_by_energy = filter_dataframe_by_energy_type(filtered_data, selected_energy_type)
        display_specific_energy_tab(regions_data, filtered_data_by_energy, selected_energy_type, start_date, end_date, key=selected_energy_type)

if __name__ == "__main__":
    main()



