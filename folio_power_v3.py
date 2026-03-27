import streamlit as st
import svgwrite

def render_power_folio_streamlit():
    dwg = svgwrite.Drawing(size=("100%", "100%"))
    dwg.viewbox(0, 0, 1200, 800)

    dwg.add(dwg.rect((50, 50), (1100, 700), fill="white", stroke="black"))

    dwg.add(dwg.text("V3 OK - NOUVEAU CODE", insert=(200, 300),
                     font_size="40px", font_weight="bold"))

    html = f"""
    <div style="width:100%;overflow:auto;background:white;">
        {dwg.tostring()}
    </div>
    """

    st.components.v1.html(html, height=800)
