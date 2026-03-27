import streamlit as st
from folio_power_v3 import render_power_folio_streamlit

st.set_page_config(layout="wide")

st.title("TEST V3")

st.success("IMPORT V3 OK")

render_power_folio_streamlit()
