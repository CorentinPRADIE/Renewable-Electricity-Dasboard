# Renewable Electricity Production Visualization App

This project visualizes the production of electricity of renewable origin competing in the auctions for Origin Guarantees (GO) at the level of electricity distribution and transmission networks in France. It provides comprehensive insights into the dynamics of renewable energy production, focusing on energy types such as Onshore Wind, Hydropower, Solar, and Geothermal. The visualizations are created with Python using Streamlit and Plotly for interactive and expressive charts.

## Dataset Description

The dataset used for this application is sourced from [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/productions-delectricite-dorigine-renouvelable-aux-encheres-des-garanties-dorigine/).

### Overview

The dataset presents, by region and sector, the productions of renewable origin electricity that compete in the auctions for Origin Guarantees (GO) at the level of electricity distribution and transmission networks.

### Details

- **Target:** Renewable electricity production installations with installed capacity greater than 100 kW.
- **Scope:** Installations benefiting from a support mechanism of either obligatory purchase or supplemental remuneration.
- **Time Frame:** Since March 2019.
- **Update Frequency:** Monthly.
- **Data Providers:** The ORE Agency and the DSOs.

#### Data Process

Since March 2019, the DSOs mandate the ORE Agency to make available to the entity responsible for conducting the auctions, a database of the concerned installations. This database is updated monthly by the co-contractors and supplemented by the DSOs within 2 months following a month of production of the value of the net monthly production injected into the network.

## App Features

1. **Interactive Filters**: Enables users to filter data based on date ranges, regions, and energy types, providing a tailored view of the data.
2. **Dynamic Visualizations**: Offers a variety of charts such as bar, pie, and maps, allowing users to discern patterns and trends in renewable energy production.
3. **Responsive Design**: Adapts to different screen sizes, ensuring accessibility from various devices.
4. **User-friendly Interface**: Provides a clean and intuitive interface for seamless navigation through different features and visualizations.

## How to Use

Navigate through different tabs to explore various visualizations and insights. Utilize the sidebar options to filter the data as per your requirements, and interact with the visualizations for a more in-depth understanding.

### Note

Ensure you have all the necessary libraries installed and the required dataset is in the correct path to run the application seamlessly.

## Libraries Used

- Streamlit
- Plotly
- Pandas
- Folium

## Developer Notes

This app aims to provide an analytical view of the renewable electricity production data, helping stakeholders, researchers, and enthusiasts to draw meaningful conclusions and insights from the renewable energy sector in France.

### Contributions

Contributions, bug reports, and improvements are welcome. Please refer to the project’s style and contribution guidelines for submitting patches and additions.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

We would like to acknowledge [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/productions-delectricite-dorigine-renouvelable-aux-encheres-des-garanties-dorigine/) for providing the dataset used in this project.

