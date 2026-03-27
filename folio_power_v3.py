import json
from pathlib import Path

import streamlit as st
import svgwrite

PAGE_W = 1800
PAGE_H = 1100

# Barres d'alimentation
Y_L = 115
Y_N = 150
Y_PE = 185

# Bloc gauche
X_SRC = 120
X_Q1 = 260
X_A1 = 360
X_T1 = 520
X_PS1 = 760

Y_Q1 = 210
Y_A1 = 340
Y_T1 = 340
Y_PS1 = 340

# Bloc moteur avec colonne dédiée
X_COL = 900
X_DM1 = X_COL
X_KM1 = X_COL
X_M1 = X_COL + 120

Y_DM1 = 210
Y_KM1 = 330
Y_M1 = 460


def load_config() -> dict:
    path = Path("config_installation.json")
    if not path.exists():
        raise FileNotFoundError("config_installation.json introuvable")
    return json.loads(path.read_text(encoding="utf-8"))


def line(dwg, x1, y1, x2, y2, w=1.2, dash=None):
    kwargs = {
        "start": (x1, y1),
        "end": (x2, y2),
        "stroke": "black",
        "stroke_width": w,
    }
    if dash:
        kwargs["stroke_dasharray"] = dash
    dwg.add(dwg.line(**kwargs))


def rect(dwg, x, y, w, h, sw=1.0):
    dwg.add(
        dwg.rect(
            (x, y),
            (w, h),
            fill="none",
            stroke="black",
            stroke_width=sw,
        )
    )


def txt(dwg, x, y, value, size=12, weight="normal", anchor="start"):
    dwg.add(
        dwg.text(
            str(value),
            insert=(x, y),
            font_size=f"{size}px",
            font_weight=weight,
            text_anchor=anchor,
            font_family="Arial",
        )
    )


def node(dwg, x, y, r=2.4):
    dwg.add(dwg.circle(center=(x, y), r=r, fill="black"))


def wire_no(dwg, x, y, value):
    txt(dwg, x, y, value, 9)


def xref(dwg, x, y, value):
    rect(dwg, x, y - 11, 90, 18, 0.8)
    txt(dwg, x + 5, y + 2, value, 8)


def terminal_arrow_text(dwg, x, y, top_text, bottom_text=None):
    txt(dwg, x, y, "◀", 9)
    txt(dwg, x + 10, y, top_text, 9)
    if bottom_text:
        txt(dwg, x + 10, y + 16, bottom_text, 9)


def draw_frame(dwg, cfg):
    rect(dwg, 10, 10, PAGE_W - 20, PAGE_H - 20, 1.2)
    rect(dwg, 18, 18, PAGE_W - 36, PAGE_H - 145, 1.0)

    usable = PAGE_W - 36
    cell = usable / 20
    for i in range(21):
        xx = 18 + i * cell
        line(dwg, xx, 18, xx, 34, 0.8)
        if i < 20:
            txt(dwg, xx + cell / 2, 30, i + 1, 8, anchor="middle")

    txt(dwg, 55, 78, cfg.get("folio_title", "PUISSANCE"), 24, "bold")

    rect(dwg, 1200, 1015, 520, 55, 0.9)
    line(dwg, 1550, 1015, 1550, 1070, 0.8)
    line(dwg, 1650, 1015, 1650, 1070, 0.8)
    txt(dwg, 1218, 1037, cfg.get("project_name", "Projet"), 10)
    txt(dwg, 1218, 1056, "FOLIO PUISSANCE", 10)
    txt(dwg, 1588, 1037, "FOLIO", 8)
    txt(dwg, 1605, 1060, "10", 18, "bold", "middle")


def draw_buses(dwg):
    line(dwg, 85, Y_L, 1710, Y_L, 1.6)
    line(dwg, 85, Y_N, 1710, Y_N, 1.6)
    line(dwg, 85, Y_PE, 1710, Y_PE, 1.6)

    txt(dwg, 56, Y_L + 4, "L", 12, "bold")
    txt(dwg, 56, Y_N + 4, "N", 12, "bold")
    txt(dwg, 44, Y_PE + 4, "PE", 12, "bold")


def draw_source(dwg):
    rect(dwg, X_SRC - 22, 100, 34, 48, 0.8)
    txt(dwg, X_SRC - 5, 118, "Ph", 8, anchor="middle")
    txt(dwg, X_SRC - 5, 138, "N", 8, anchor="middle")


def draw_q1(dwg):
    x, y = X_Q1, Y_Q1
    txt(dwg, x + 16, y - 18, "Q1", 11, "bold", "middle")
    txt(dwg, x + 16, y - 5, "Disjoncteur général", 8, anchor="middle")

    line(dwg, x + 16, y, x + 16, y + 14, 1.4)
    line(dwg, x + 16, y + 14, x + 30, y + 34, 1.4)
    line(dwg, x + 30, y + 34, x + 16, y + 34, 1.4)
    line(dwg, x + 16, y + 34, x + 16, y + 92, 1.4)

    txt(dwg, x + 36, y + 8, "1", 8)
    txt(dwg, x + 36, y + 82, "2", 8)


def draw_a1(dwg, cfg):
    if not cfg["controller"].get("enabled", False):
        return
    x, y = X_A1, Y_A1
    txt(dwg, x + 45, y - 18, cfg["controller"]["tag"], 11, "bold", "middle")
    txt(dwg, x + 45, y - 5, cfg["controller"]["label"], 8, anchor="middle")
    rect(dwg, x, y, 90, 62, 0.9)
    txt(dwg, x + 45, y + 38, "MXPRO", 16, "bold", "middle")


def draw_t1(dwg, cfg):
    if not cfg["transformer"].get("enabled", False):
        return
    x, y = X_T1, Y_T1

    txt(dwg, x + 40, y - 18, cfg["transformer"]["tag"], 11, "bold", "middle")
    txt(dwg, x + 40, y - 2, "Transformateur 230/24V", 8, anchor="middle")

    line(dwg, x + 15, y, x + 15, y + 14, 1.3)
    line(dwg, x + 60, y, x + 60, y + 14, 1.3)

    dwg.add(dwg.circle(center=(x + 28, y + 40), r=13, fill="none", stroke="black", stroke_width=1.0))
    dwg.add(dwg.circle(center=(x + 50, y + 60), r=13, fill="none", stroke="black", stroke_width=1.0))

    line(dwg, x + 28, y + 73, x + 28, y + 97, 1.3)
    line(dwg, x + 72, y + 73, x + 72, y + 97, 1.3)

    line(dwg, x + 8, y + 70, x + 8, y + 82, 0.8)
    line(dwg, x + 2, y + 82, x + 14, y + 82, 0.8)
    line(dwg, x + 4, y + 86, x + 12, y + 86, 0.8)
    line(dwg, x + 6, y + 90, x + 10, y + 90, 0.8)

    txt(dwg, x + 6, y - 6, "P1", 7)
    txt(dwg, x + 52, y - 6, "P2", 7)
    txt(dwg, x + 22, y + 98, "S1", 7)
    txt(dwg, x + 67, y + 98, "S2", 7)


def draw_ps1(dwg, cfg):
    if not cfg["power_supply"].get("enabled", False):
        return
    x, y = X_PS1, Y_PS1
    txt(dwg, x + 36, y - 18, cfg["power_supply"]["tag"], 11, "bold", "middle")
    txt(dwg, x + 36, y - 5, cfg["power_supply"]["label"], 8, anchor="middle")
    rect(dwg, x, y + 8, 72, 52, 0.9)
    txt(dwg, x + 36, y + 40, "PS", 18, "bold", "middle")


def draw_dm1(dwg, cfg):
    if not cfg["pump"].get("enabled", False):
        return
    x, y = X_DM1, Y_DM1

    txt(dwg, x + 42, y - 16, cfg["pump"]["protection_tag"], 11, "bold", "middle")
    txt(dwg, x + 42, y - 2, "Protection moteur", 8, anchor="middle")

    line(dwg, x + 15, y, x + 15, y + 16, 1.1)
    line(dwg, x + 42, y, x + 42, y + 16, 1.1)
    line(dwg, x + 69, y, x + 69, y + 16, 1.1)

    rect(dwg, x + 7, y + 16, 70, 76, 1.0)

    line(dwg, x + 15, y + 16, x + 15, y + 82, 0.9)
    line(dwg, x + 42, y + 16, x + 42, y + 82, 0.9)
    line(dwg, x + 69, y + 16, x + 69, y + 82, 0.9)

    line(dwg, x + 15, y + 92, x + 15, y + 120, 1.1)
    line(dwg, x + 42, y + 92, x + 42, y + 120, 1.1)
    line(dwg, x + 69, y + 92, x + 69, y + 120, 1.1)

    txt(dwg, x + 10, y - 6, "1", 7)
    txt(dwg, x + 37, y - 6, "3", 7)
    txt(dwg, x + 64, y - 6, "5", 7)
    txt(dwg, x + 10, y + 110, "2", 7)
    txt(dwg, x + 37, y + 110, "4", 7)
    txt(dwg, x + 64, y + 110, "6", 7)


def draw_km1(dwg, cfg):
    if not cfg["pump"].get("enabled", False):
        return
    x, y = X_KM1, Y_KM1

    txt(dwg, x + 42, y - 16, cfg["pump"]["contactor_tag"], 11, "bold", "middle")
    txt(dwg, x + 42, y - 2, "Contact puissance", 8, anchor="middle")

    for xoff, topn, botn in [(15, "1", "2"), (42, "3", "4"), (69, "5", "6")]:
        line(dwg, x + xoff, y + 8, x + xoff, y + 28, 1.0)
        line(dwg, x + xoff + 9, y + 31, x + xoff + 9, y + 58, 1.0)
        line(dwg, x + xoff, y + 28, x + xoff + 9, y + 31, 1.0)
        txt(dwg, x + xoff - 2, y - 1, topn, 7)
        txt(dwg, x + xoff + 5, y + 70, botn, 7)

    line(dwg, x + 15, y + 8, x + 15, y + 115, 0.8, dash=[3, 3])
    line(dwg, x + 42, y + 8, x + 42, y + 115, 0.8, dash=[3, 3])
    line(dwg, x + 69, y + 8, x + 69, y + 115, 0.8, dash=[3, 3])


def draw_motor_chain(dwg, cfg):
    if not cfg["pump"].get("enabled", False):
        return

    dm_x = X_DM1
    km_x = X_KM1
    m_x = X_M1
    m_y = Y_M1

    for dm_off, km_off in [(15, 15), (42, 42), (69, 69)]:
        line(dwg, dm_x + dm_off, Y_DM1 + 120, km_x + km_off, Y_KM1 + 8, 1.0)

    line(dwg, km_x + 15, Y_KM1 + 58, km_x + 15, m_y - 42, 1.0, dash=[3, 3])
    line(dwg, km_x + 42, Y_KM1 + 58, km_x + 42, m_y - 42, 1.0, dash=[3, 3])

    txt(dwg, km_x + 10, m_y - 50, "Brin 1", 7)
    txt(dwg, km_x + 37, m_y - 50, "Brin 2", 7)

    dwg.add(dwg.ellipse(center=(km_x - 35, m_y - 50), r=(24, 8), fill="none", stroke="black", stroke_width=0.8))
    txt(dwg, km_x - 35, m_y - 47, "P1-2", 7, anchor="middle")

    txt(dwg, m_x + 34, m_y - 24, cfg["pump"]["motor_tag"], 11, "bold", "middle")
    txt(dwg, m_x + 34, m_y - 8, cfg["pump"]["motor_label"], 8, anchor="middle")
    dwg.add(dwg.circle(center=(m_x + 34, m_y + 10), r=24, fill="none", stroke="black", stroke_width=1.0))
    txt(dwg, m_x + 34, m_y + 16, "M", 16, "bold", "middle")
    txt(dwg, m_x - 6, m_y - 1, "U1", 7)
    txt(dwg, m_x + 18, m_y - 1, "U2", 7)
    txt(dwg, m_x - 18, m_y + 12, "1~", 8)
    txt(dwg, m_x - 30, m_y - 18, "145 W", 7)
    txt(dwg, m_x - 28, m_y - 4, "1.5 A", 7)

    line(dwg, km_x + 15, m_y - 42, m_x + 2, m_y - 18, 1.0, dash=[3, 3])
    line(dwg, km_x + 42, m_y - 42, m_x + 26, m_y - 18, 1.0, dash=[3, 3])

    line(dwg, m_x + 58, m_y + 16, m_x + 82, m_y + 16, 0.8)
    line(dwg, m_x + 82, m_y + 16, m_x + 82, m_y + 26, 0.8)
    line(dwg, m_x + 72, m_y + 26, m_x + 92, m_y + 26, 0.8)
    line(dwg, m_x + 75, m_y + 30, m_x + 89, m_y + 30, 0.8)
    line(dwg, m_x + 78, m_y + 34, m_x + 86, m_y + 34, 0.8)


def draw_wires_left(dwg, cfg):
    qx = X_Q1 + 16
    qy = Y_Q1 + 92

    line(dwg, qx, Y_L, qx, Y_Q1, 1.0)
    node(dwg, qx, Y_L)
    wire_no(dwg, qx + 6, Y_L - 3, "0")

    if cfg["transformer"].get("enabled", False):
        line(dwg, qx, qy, X_T1 + 15, qy, 1.0)
        line(dwg, X_T1 + 15, qy, X_T1 + 15, Y_T1, 1.0)
        wire_no(dwg, (qx + X_T1 + 15) / 2, qy - 3, "1001")

        line(dwg, X_T1 + 60, Y_N, X_T1 + 60, Y_T1, 1.0)
        node(dwg, X_T1 + 60, Y_N)
        wire_no(dwg, X_T1 + 66, 252, "1002")

    if cfg["power_supply"].get("enabled", False):
        line(dwg, qx, qy + 18, X_PS1, qy + 18, 1.0)
        line(dwg, X_PS1, qy + 18, X_PS1, Y_PS1 + 16, 1.0)
        wire_no(dwg, (qx + X_PS1) / 2, qy + 14, "5")

        line(dwg, X_PS1 + 72, Y_N, X_PS1 + 72, Y_PS1 + 34, 1.0)
        node(dwg, X_PS1 + 72, Y_N)
        wire_no(dwg, X_PS1 + 78, 300, "6")

    if cfg["controller"].get("enabled", False):
        line(dwg, qx, qy, X_A1, qy, 1.0)
        line(dwg, X_A1, qy, X_A1, Y_A1 + 18, 1.0)
        wire_no(dwg, (qx + X_A1) / 2, qy - 3, "1")

        line(dwg, X_A1 + 90, Y_N, X_A1 + 90, Y_A1 + 34, 1.0)
        node(dwg, X_A1 + 90, Y_N)
        wire_no(dwg, X_A1 + 96, 312, "2")


def draw_wires_right(dwg, cfg):
    if not cfg["pump"].get("enabled", False):
        return

    # descente dédiée depuis les barres vers la colonne moteur
    line(dwg, X_COL - 18, Y_L, X_COL - 18, Y_DM1, 1.0)
    line(dwg, X_COL + 9, Y_L, X_COL + 9, Y_DM1, 1.0)
    line(dwg, X_COL + 36, Y_N, X_COL + 36, Y_DM1, 1.0)

    node(dwg, X_COL - 18, Y_L)
    node(dwg, X_COL + 9, Y_L)
    node(dwg, X_COL + 36, Y_N)

    # liaison de la descente vers DM1
    line(dwg, X_COL - 18, Y_DM1, X_DM1 + 15, Y_DM1, 1.0)
    line(dwg, X_COL + 9, Y_DM1, X_DM1 + 42, Y_DM1, 1.0)
    line(dwg, X_COL + 36, Y_DM1, X_DM1 + 69, Y_DM1, 1.0)

    wire_no(dwg, X_DM1 + 74, Y_DM1 + 8, "10")


def draw_bottom_feeds(dwg, cfg):
    if cfg["controller"].get("enabled", False):
        x1 = X_Q1 + 16
        x2 = X_Q1 + 52
        y_start = Y_Q1 + 92
        y_drop = 540

        line(dwg, x1, y_start, x1, y_drop, 1.0)
        line(dwg, x2, Y_N, x2, y_drop, 1.0)

        wire_no(dwg, x1 + 5, 455, "1001")
        wire_no(dwg, x2 + 5, 455, "1002")

        terminal_arrow_text(dwg, x1 - 6, y_drop + 22, "A1 PRO1 N")
        terminal_arrow_text(dwg, x2 - 6, y_drop + 22, "A1 PRO1 Ph")

        txt(dwg, (x1 + x2) / 2, y_drop + 60, "Alim", 8, anchor="middle")
        txt(dwg, (x1 + x2) / 2, y_drop + 77, cfg["controller"]["label"], 8, anchor="middle")

    if cfg["power_supply"].get("enabled", False):
        x24 = X_T1 + 28
        x0 = X_T1 + 72
        y_start = Y_T1 + 97
        y_drop = 540

        line(dwg, x24, y_start, x24, y_drop, 1.0)
        line(dwg, x0, y_start, x0, y_drop, 1.0)

        wire_no(dwg, x24 + 5, 468, "1003")
        wire_no(dwg, x0 + 5, 468, "1004")

        terminal_arrow_text(dwg, x24 - 6, y_drop + 22, "X1:7")
        terminal_arrow_text(dwg, x0 - 6, y_drop + 22, "X1:8")

        txt(dwg, (x24 + x0) / 2, y_drop + 60, "Alimentation", 8, anchor="middle")
        txt(dwg, (x24 + x0) / 2, y_drop + 77, "Vanne", 8, anchor="middle")


def render_power_folio_streamlit():
    try:
        cfg = load_config()
    except Exception as e:
        st.error(f"Erreur chargement configuration : {e}")
        return

    dwg = svgwrite.Drawing(size=("100%", "100%"))
    dwg.viewbox(0, 0, PAGE_W, PAGE_H)

    draw_frame(dwg, cfg)
    draw_buses(dwg)
    draw_source(dwg)
    draw_q1(dwg)
    draw_a1(dwg, cfg)
    draw_t1(dwg, cfg)
    draw_ps1(dwg, cfg)
    draw_dm1(dwg, cfg)
    draw_km1(dwg, cfg)
    draw_motor_chain(dwg, cfg)
    draw_wires_left(dwg, cfg)
    draw_wires_right(dwg, cfg)
    draw_bottom_feeds(dwg, cfg)

    html = f"""
    <div style="width:100%;overflow:auto;background:white;border:1px solid #bbb;">
        <div style="min-width:1650px;padding:8px;">
            {dwg.tostring()}
        </div>
    </div>
    """

    st.subheader("Folio 10 - Puissance")
    st.components.v1.html(html, height=980, scrolling=True)

    with st.expander("Configuration chargée"):
        st.json(cfg)
