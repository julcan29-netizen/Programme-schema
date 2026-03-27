# app.py
import streamlit as st
from folio_power import render_power_folio_streamlit

st.set_page_config(layout="wide")
st.title("Générateur de schémas électriques CVC")

page = st.sidebar.selectbox(
    "Choisir un folio",
    ["Folio 10 - Puissance"]
)

if page == "Folio 10 - Puissance":
    render_power_folio_streamlit()
