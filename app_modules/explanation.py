import streamlit as st

ALL_ENERGY_TAB_EXPLANATION = """
        ### How to Use the Energy Overview Tab
        **Welcome to the Energy Overview Tab!** Here, you can explore a comprehensive visual representation 
        of various energy data across different regions. Below is a guide to help you navigate through the insights available:

        - **Map Visualization**: On the left, you’ll find a map that provides a geographical representation of 
          energy data across different regions. The color intensity represents the volume of the selected energy type.
          Hover over a region to see more detailed information. Additionally, you can **click on a region** on the map 
          to select it, and the other visualizations will update to reflect data specific to this region.
        
        - **Charts Visualization**:
            - **Pie Chart**: The pie chart provides a visual representation of the proportion of volume sold per energy type. 
              Each segment represents a different type of energy, allowing you to quickly perceive the relative contribution 
              of each to the total volume sold.
            - **Stacked Bar Plot**: Adjacent to the pie chart, you’ll find a stacked bar plot illustrating the evolution of 
              different energy types over time. The bars represent total volume, segmented by energy type, allowing you to 
              explore how each contributes to the total across different time points.
              Beneath the bar plot, a select box titled "Choose Time Aggregation" allows you to adjust the time granularity 
              of the data displayed, offering "Yearly" and "Monthly" options to explore broader trends or more granular shifts, respectively.
        
        - **Region's Stats**: Below, you’ll find a table that displays statistical data for each region, providing 
          a numerical breakdown of the energy data:
            - **region**: The geographical region to which the subsequent data pertains.
            - **total_volume**: The overall volume of energy for the region.
            - **[Energy Type]_total_volume**: The total volume specific to each type of energy (e.g., Onshore Wind, Hydropower, Solar, Geothermal) for the region.
            - **[Energy Type]_percentage**: The percentage that each type of energy contributes to the total volume in the region.
          
          The energy types available in the dataset are Onshore Wind, Hydropower, Solar, and Geothermal. Each of these has two associated columns, 
          indicating their total volume and their percentage contribution to the overall energy volume for the respective region.

        - **Time Interval Selection**: In the sidebar on the left, you can specify a time interval for the data you want to explore. 
          By selecting a start and end date, you adjust the range of data visualized across all charts and tables on this tab. 
          This allows you to focus on specific periods and observe the variations in energy data over time.
          
        Feel free to select different energy types, date ranges, or regions from the sidebar to tailor the visualizations 
        and data to your specific interests. Explore the correlations and dive into the trends of renewable energy 
        across different regions and time frames!

        **Dive Deeper into Specific Energy Types**: For a more specialized view, navigate to the top of the page and select a 
        specific energy type from the dropdown menu. Doing so will present you with visualizations and data that focus solely 
        on the chosen energy type, enabling you to explore its particular trends and impacts across different regions and periods.
        """

SPECIFIC_ENERGY_TAB_EXPLANATION = """
    ### How to Use the [Energy Type] Tab
    
    **Welcome to the [Energy Type] Tab!** This tab provides a detailed visual exploration into [Energy Type], 
    offering insights into its distribution, seasonal variations, and trends across various regions. Here's 
    a guide to assist you in navigating through the available visualizations:
    
    - **Bar Chart: Total Volume Sold Over Time**
        - This chart displays the total volume of [Energy Type] sold over a defined time period.
        - The "Choose Time Aggregation" select box allows you to toggle between 'Monthly' and 'Yearly' views, 
          enabling exploration of the data at different time granularities.
        - It offers a clear visualization of how the sales volume of [Energy Type] has evolved, facilitating 
          the identification of trends and anomalies over time.
        
    - **Bar Chart: Percentage of [Energy Type] Sold per Season**
        - This chart illustrates the distribution of [Energy Type] sales across different seasons: Winter, Spring, 
          Summer, and Autumn.
        - It enables you to identify any seasonal patterns or dependencies in the sales of [Energy Type].
        
    - **Pie Chart: Total Volume Sold by Region**
        - This pie chart visualizes the total volume of [Energy Type] sold, broken down by region.
        - The top regions (based on sales volume) are displayed individually, while others might be grouped together 
          to provide a clear and concise view.
        - It assists in identifying which regions have the highest sales for [Energy Type].

    Explore these visualizations to delve deeper into the analysis of [Energy Type], observing its distribution, 
    performance, and trends across different dimensions and time frames. Adjust the time frames, regions, and other 
    available options to tailor the data and visualizations to your specific analytical needs!
"""
