import streamlit as st
import svgwrite


def render_power_folio_streamlit():
    dwg = svgwrite.Drawing(size=("100%", "100%"))
    dwg.viewbox(0, 0, 1400, 900)

    dwg.add(dwg.rect((20, 20), (1360, 860), fill="white", stroke="black"))
    dwg.add(dwg.text("FOLIO_POWER IMPORT OK", insert=(120, 180), font_size="42px", font_weight="bold"))
    dwg.add(dwg.text("SIGNATURE FP-888", insert=(120, 260), font_size="28px", font_weight="bold"))
    dwg.add(dwg.text("SI TU VOIS ÇA, APP.PY APPELLE BIEN CE FICHIER", insert=(120, 340), font_size="24px"))

    html = f"""
    <div style="width:100%;overflow:auto;background:white;border:1px solid #bbb;">
        <div style="min-width:1200px;padding:8px;">
            {dwg.tostring()}
        </div>
    </div>
    """

    st.subheader("Folio 10 - Puissance")
    st.components.v1.html(html, height=900, scrolling=True)
