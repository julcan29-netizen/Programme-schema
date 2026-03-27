import streamlit as st
from folio_power import render_power_folio_streamlit

st.set_page_config(layout="wide")

st.title("Générateur de schémas électriques CVC")

render_power_folio_streamlit()
