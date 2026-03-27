import streamlit as st
from folio_power_v2 import render_power_folio_streamlit

st.set_page_config(layout="wide")
st.title("Générateur de schémas électriques CVC")
st.success("MOTEUR V2 ACTIF")

render_power_folio_streamlit()
