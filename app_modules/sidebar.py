import streamlit as st
import pandas as pd
import datetime


def display_date_filter_sidebar(dataframe):
    """
    Display a sidebar with interactive sliders allowing users to filter the displayed data based on date ranges.
    
    Args:
        dataframe (pd.DataFrame): The input DataFrame containing the data to be filtered.

    Returns:
        tuple: A tuple containing the start_date and end_date selected by the user.
    """
    # Displaying a header in the sidebar
    st.sidebar.header("Filter Data")

    # Providing a dropdown select box for the user to choose the date interval type (Month or Year).
    interval_type = st.sidebar.selectbox("Select Interval type (Month or Year)", ("Month", "Year"))

    # Updating the 'interval' column in the DataFrame based on the selected interval type
    dataframe['interval'] = dataframe['date'].dt.to_period('M') if interval_type == "Month" else dataframe['date'].dt.to_period('Y')

    # Retrieving unique intervals for slider creation
    unique_intervals = sorted(dataframe['interval'].unique().astype(str))
    start_interval = pd.to_datetime(unique_intervals[0]).to_pydatetime()
    end_interval = pd.to_datetime(unique_intervals[-1]).to_pydatetime()

    # Creating sliders in the sidebar, enabling users to select the date range based on the selected interval type
    if interval_type == "Year":
        selected_start_date, selected_end_date = st.sidebar.slider(
            "Select a Year interval:",
            min_value=start_interval,
            max_value=end_interval,
            value=(start_interval, end_interval),
            format="YYYY",
            step=datetime.timedelta(days=366)  # Approximate days in a year considering leap years
        )
    else:  # for "Month"
        selected_start_date, selected_end_date = st.sidebar.slider(
            "Select a Month interval:",
            min_value=start_interval,
            max_value=end_interval,
            value=(start_interval, end_interval),
            format="YYYY-MM",
            step=datetime.timedelta(days=31)  # Maximum days in a month
        )

    # Displaying the selected date range in the sidebar
    st.sidebar.success(f"Selected interval: \n\n    {selected_start_date.strftime('%Y-%m')} to {selected_end_date.strftime('%Y-%m')}", icon="🕓")

    return selected_start_date, selected_end_date

