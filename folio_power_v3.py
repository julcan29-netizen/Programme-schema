import streamlit as st
import svgwrite

PAGE_W = 1600
PAGE_H = 900


# =========================
# MODELE DE DONNÉES
# =========================

def build_power_case():
    return {
        "components": [
            {"type": "Q", "tag": "Q1", "x": 200},
            {"type": "A", "tag": "A1", "x": 400},
            {"type": "T", "tag": "T1", "x": 600},
            {"type": "PS", "tag": "PS1", "x": 800},
            {"type": "DM", "tag": "DM1", "x": 1100},
            {"type": "KM", "tag": "KM1", "x": 1100, "y": 500},
            {"type": "X", "tag": "X1", "x": 1300, "y": 450},
            {"type": "M", "tag": "M1", "x": 1500, "y": 650},
        ]
    }


# =========================
# SYMBOLS
# =========================

def draw_component(dwg, comp):
    x = comp["x"]
    y = comp.get("y", 300)
    t = comp["type"]
    tag = comp["tag"]

    if t == "Q":
        dwg.add(dwg.text(tag, insert=(x, y - 20), font_size="14px", font_weight="bold"))
        dwg.add(dwg.line((x, y), (x, y + 80), stroke="black", stroke_width=2))

    elif t == "A":
        dwg.add(dwg.rect((x, y), (100, 70), fill="none", stroke="black"))
        dwg.add(dwg.text(tag, insert=(x + 50, y + 40), text_anchor="middle"))

    elif t == "T":
        dwg.add(dwg.circle(center=(x + 30, y + 30), r=15, fill="none", stroke="black"))
        dwg.add(dwg.circle(center=(x + 60, y + 30), r=15, fill="none", stroke="black"))
        dwg.add(dwg.text(tag, insert=(x + 45, y - 10), text_anchor="middle"))

    elif t == "PS":
        dwg.add(dwg.rect((x, y), (100, 60), fill="none", stroke="black"))
        dwg.add(dwg.text("PS", insert=(x + 50, y + 35), text_anchor="middle"))

    elif t == "DM":
        dwg.add(dwg.rect((x, y), (60, 80), fill="none", stroke="black"))
        dwg.add(dwg.text("DM", insert=(x + 30, y + 45), text_anchor="middle"))

    elif t == "KM":
        dwg.add(dwg.line((x + 30, y), (x + 30, y + 80), stroke="black"))
        dwg.add(dwg.line((x + 10, y + 40), (x + 50, y + 40), stroke="black"))

    elif t == "X":
        dwg.add(dwg.rect((x, y), (60, 120), fill="none", stroke="black"))
        dwg.add(dwg.text("X1", insert=(x + 30, y - 10), text_anchor="middle"))

    elif t == "M":
        dwg.add(dwg.circle(center=(x + 40, y + 40), r=30, fill="none", stroke="black"))
        dwg.add(dwg.text("M", insert=(x + 40, y + 45), text_anchor="middle"))


# =========================
# RENDER
# =========================

def render_power_folio_streamlit():
    data = build_power_case()

    dwg = svgwrite.Drawing(size=("100%", "100%"))
    dwg.viewbox(0, 0, PAGE_W, PAGE_H)

    # cadre
    dwg.add(dwg.rect((20, 20), (PAGE_W - 40, PAGE_H - 40),
                     fill="white", stroke="black"))

    # barre L N PE
    dwg.add(dwg.line((50, 100), (1500, 100), stroke="black", stroke_width=2))
    dwg.add(dwg.line((50, 130), (1500, 130), stroke="black", stroke_width=2))
    dwg.add(dwg.line((50, 160), (1500, 160), stroke="black", stroke_width=2))

    # composants
    for comp in data["components"]:
        draw_component(dwg, comp)

    html = f"""
    <div style="width:100%;overflow:auto;background:white;">
        {dwg.tostring()}
    </div>
    """

    st.subheader("Folio 10 - Puissance")
    st.components.v1.html(html, height=900)
