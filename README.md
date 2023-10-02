# Renewable Electricity Production App

Explore interactive visualizations of renewable electricity production in France using this app.<br> Access it [here](https://pradie-corentin-renewable-electricity-app.streamlit.app/).

## Overview

This app provides insights into renewable electricity production across various regions and sectors in France. It displays data related to renewable energy installations participating in the auctions for Origin Guarantees (GO), focused on the transmission and distribution networks of electricity.

### Data Source and Description

The app utilizes a dataset from [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/productions-delectricite-dorigine-renouvelable-aux-encheres-des-garanties-dorigine/), presenting details about renewable electricity produced from installations with a capacity greater than 100 kW. These installations benefit from support mechanisms such as obligatory purchase or supplemental remuneration.

The Obligations of Renewable Energy (ORE) Agency, mandated by Distribution System Operators (DSOs), provides a monthly updated database of the installations participating in the auctions for Origin Guarantees since March 2019. This database contains the net monthly production values injected into the network, updated by co-contractors and supplemented by DSOs within two months following a production month.

For more information about the dataset, you can refer to the [official dataset description](https://www.data.gouv.fr/fr/datasets/productions-delectricite-dorigine-renouvelable-aux-encheres-des-garanties-dorigine/).

## Features

The app offers a user-friendly interface with various interactive features:
- **Data Filters**: Customize views based on date ranges, regions, and energy types.
- **Interactive Visualizations**: Explore data through interactive bar charts, pie charts, combined charts, and geographical maps that represent renewable electricity production details concisely and clearly.

## Technologies

- **Streamlit**: To build the web application with Python.
- **Plotly**: For creating interactive and responsive plots.
- **Folium**: To create dynamic maps.
- **Pandas**: Employed for data manipulation and analysis.

## License

This project is open source, under the MIT License. For more details, see the [LICENSE](LICENSE) file.

Thank you for your interest in this project! Dive in, interact, and gain insights into renewable electricity production in France [here](https://pradie-corentin-renewable-electricity-app.streamlit.app/).
