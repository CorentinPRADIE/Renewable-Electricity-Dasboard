from streamlit_folium import st_folium
import folium
from app_modules.colors import ENERGY_TYPE_COLOR_GRADIENTS
import streamlit as st


def display_map(regions_df, energy_type, start_date, end_date, key):
    """ Displays a map visualization for the given energy_type and date range. """

    # Initializing and configuring the map.
    map = initialize_map()
    select_map_type(energy_type)
    
    # Setting column names and creating choropleth layer.
    column_to_display_as_color, total_volume_per_energy, percentage_per_energy = configure_map_settings(energy_type)
    choropleth = create_choropleth(regions_df, column_to_display_as_color, energy_type)
    choropleth.geojson.add_to(map)

    # Updating feature properties and attaching tooltips.
    update_features(choropleth, regions_df, energy_type, start_date, end_date, total_volume_per_energy, percentage_per_energy)
    attach_tooltip(choropleth, energy_type)
    
    # Rendering the map in Streamlit.
    render_streamlit_map(map, key)


def initialize_map():
    """ Initializes the map with specified settings. Returns a folium Map object. """
    return folium.Map(location=[46.603354, 3], scrollWheelZoom=False, zoom_control=False, zoom_start=5, tiles="CartoDB positron")


def select_map_type(energy_type):
    """ Renders a selection box for map type if the energy_type is not 'All Renewables'. """
    if energy_type != "All Renewables":
        adjust_selectbox_position()
        st.selectbox("", ["Pourcentage in the Renewables", "Volume Sold"], key="map_type")


def adjust_selectbox_position():
    """ Adjusts the positioning of the selectbox by applying custom CSS. """
    st.markdown(
        """
        <style>
        [data-baseweb="select"] {
            margin-top: -50px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def configure_map_settings(energy_type):
    """ Configures settings and prepares columns for map visualization based on the selected energy type. """
    total_volume_per_energy = f"{energy_type}_total_volume" if energy_type != "All Renewables" else "total_volume_millions"
    percentage_per_energy = f"{energy_type}_percentage" if energy_type != "All Renewables" else ""
    column_to_display_as_color = total_volume_per_energy if energy_type == "All Renewables" or st.session_state.get("map_type", "") == "Volume Sold" else percentage_per_energy
    return column_to_display_as_color, total_volume_per_energy, percentage_per_energy


def create_choropleth(regions_df, column_to_display_as_color, energy_type):
    """ Creates a choropleth layer for the map visualization. """
    return folium.Choropleth(
        geo_data="data/france_regions.geojson",
        data=regions_df,
        columns=["region", column_to_display_as_color],
        key_on="feature.properties.nom",
        fill_opacity=0.7,
        line_opacity=0.8,
        highlight=True,
        fill_color=ENERGY_TYPE_COLOR_GRADIENTS[energy_type],
        nan_fill_color="grey",
        nan_fill_opacity=1,
    )


def update_features(choropleth, regions_df, energy_type, start_date, end_date, total_volume_per_energy, percentage_per_energy):
    """ Updates features of the choropleth layer based on the provided data. """
    for feature in choropleth.geojson.data["features"]:
        region_name = feature["properties"]["nom"]
        region = regions_df[regions_df["region"] == region_name]
        
        # Update properties based on availability of data.
        if region.empty:
            feature["properties"].update({"total_volume": "Total: No data", "avg_volume": "Average: No data"})
        else:
            feature["properties"]["period"] = f"From {start_date.strftime('%Y-%m')} to {end_date.strftime('%Y-%m')}"
            if energy_type == "All Renewables":
                feature["properties"]["total_volume"] = f"Total Sold: {region[total_volume_per_energy].iloc[0]:.1f} Millions €"
            else:
                feature["properties"]["total_volume"] = f"Total Sold: {int(region[total_volume_per_energy].iloc[0]): ,} €"
                feature["properties"]["percentage"] = f"{energy_type}: {region[percentage_per_energy].iloc[0]: .0f}%"


def attach_tooltip(choropleth, energy_type):
    """ Attaches tooltip to the choropleth layer. """
    fields = ["nom", "total_volume", "period"] if energy_type == "All Renewables" else ["nom", "total_volume", "percentage", "period"]
    tooltip_style = "background-color: lightgreen;"
    choropleth.geojson.add_child(folium.features.GeoJsonTooltip(fields, labels=False, style=tooltip_style))


def render_streamlit_map(map, key):
    """ Renders the map visualization in the Streamlit app. """
    st_map = st_folium(map, height=350, key=key, use_container_width=True, zoom=5)
    if "region" not in st.session_state:
        st.session_state["region"] = "All Regions"

    st.write('Click on a region on the map to select it, or :')
    if st.button("Click here to select all regions"):
        st.session_state["region"] = "All Regions"
    elif st_map["last_active_drawing"]:
        st.session_state["region"] = st_map["last_active_drawing"]["properties"]["nom"]
