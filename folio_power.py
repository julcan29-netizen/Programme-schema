import streamlit as st
import svgwrite

def render_power_folio_streamlit():
    dwg = svgwrite.Drawing(size=("100%", "100%"))
    dwg.viewbox(0, 0, 1200, 800)

    dwg.add(dwg.rect((20, 20), (1160, 760), fill="white", stroke="black"))
    dwg.add(dwg.text("FOLIO POWER TEST V777", insert=(100, 100), font_size="40px", font_weight="bold"))
    dwg.add(dwg.text("SI TU VOIS CE TEXTE, C'EST BIEN CE FICHIER QUI TOURNE", insert=(100, 180), font_size="24px"))

    html = f"""
    <div style="width:100%;overflow:auto;background:white;border:1px solid #bbb;">
        <div style="min-width:1200px;padding:8px;">
            {dwg.tostring()}
        </div>
    </div>
    """
    st.subheader("Folio 10 - Puissance")
    st.components.v1.html(html, height=850, scrolling=True)
