import streamlit as st

st.set_page_config(layout="wide")

st.title("APP FINAL TEST")

st.success("SI TU VOIS CE MESSAGE → APP.PY EST BIEN CELUI-CI")

from folio_power import render_power_folio_streamlit

render_power_folio_streamlit()
