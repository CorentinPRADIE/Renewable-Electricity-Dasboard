"""
This module defines color mappings for different energy types to be used in visualizations throughout the application.
"""

# Define constant dictionaries to hold the color and gradient values associated with each energy type.

# A Dictionary containing color mappings for individual energy types
ENERGY_TYPE_COLORS = {
    "Onshore Wind": "#7852A9",  # A shade of purple representing Onshore Wind
    "Hydropower": "#246fbe",  # A shade of blue representing Hydropower
    "Solar": "#FFD300",  # A shade of yellow representing Solar
    "Geothermal": "#ad262b",  # A shade of red representing Geothermal
}

# A Dictionary containing color gradient mappings for individual and combined energy types
ENERGY_TYPE_COLOR_GRADIENTS = {
    "All Renewables": "Greens",  # A green gradient representing all renewable energy types combined
    "Onshore Wind": "Purples",  # A purple gradient representing Onshore Wind
    "Hydropower": "Blues",  # A blue gradient representing Hydropower
    "Solar": "YlOrRd",  # A yellow to red gradient representing Solar
    "Geothermal": "Reds",  # A red gradient representing Geothermal
}
