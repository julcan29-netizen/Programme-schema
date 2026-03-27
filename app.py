import streamlit as st
import svgwrite

st.set_page_config(layout="wide")

st.title("TEST DIRECT")

dwg = svgwrite.Drawing(size=("100%", "100%"))
dwg.viewbox(0, 0, 1200, 800)

dwg.add(dwg.rect((20, 20), (1160, 760), fill="white", stroke="black"))
dwg.add(dwg.text("RENDER DIRECT APP.PY", insert=(100, 200), font_size="40px", font_weight="bold"))

st.components.v1.html(dwg.tostring(), height=800)
