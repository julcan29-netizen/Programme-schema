import streamlit as st
from folio_power_v2 import render_power_folio_streamlit

st.set_page_config(layout="wide")

st.title("APP FINAL TEST V2")

st.success("SI TU VOIS CE MESSAGE → IMPORT V2 OK")

render_power_folio_streamlit()
