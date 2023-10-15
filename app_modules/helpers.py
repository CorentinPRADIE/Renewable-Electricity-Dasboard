import streamlit as st

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
