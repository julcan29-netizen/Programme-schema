import json
from pathlib import Path

import streamlit as st
import svgwrite

PAGE_W = 1800
PAGE_H = 1100

# Barres
Y_L = 115
Y_N = 150
Y_PE = 185

# Colonnes principales
X_SRC = 140
X_Q1 = 300
X_T1 = 510
X_PS1 = 760
X_DM1 = 1110
X_KM1 = 1110
X_M1 = 1360

# Niveaux
Y_Q1 = 210
Y_T1 = 330
Y_PS1 = 330
Y_DM1 = 210
Y_KM1 = 500
Y_M1 = 760


def load_config() -> dict:
    path = Path("config_installation.json")
    if not path.exists():
        raise FileNotFoundError("config_installation.json introuvable")
    return json.loads(path.read_text(encoding="utf-8"))


def line(dwg, x1, y1, x2, y2, w=1.4, dash=None):
    dwg.add(
        dwg.line(
            (x1, y1),
            (x2, y2),
            stroke="black",
            stroke_width=w,
            stroke_dasharray=dash,
        )
    )


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


def node(dwg, x, y, r=2.6):
    dwg.add(dwg.circle(center=(x, y), r=r, fill="black"))


def wire_no(dwg, x, y, value):
    txt(dwg, x, y, value, 10, "normal")


def xref(dwg, x, y, value):
    rect(dwg, x, y - 11, 95, 18, 0.8)
    txt(dwg, x + 5, y + 2, value, 9)


def terminal_arrow_text(dwg, x, y, top_text, bottom_text=None):
    txt(dwg, x, y, "◀", 10)
    txt(dwg, x + 12, y, top_text, 10)
    if bottom_text:
        txt(dwg, x + 12, y + 18, bottom_text, 10)


def draw_frame(dwg, cfg):
    rect(dwg, 10, 10, PAGE_W - 20, PAGE_H - 20, 1.4)
    rect(dwg, 18, 18, PAGE_W - 36, PAGE_H - 150, 1.0)

    # grille haute
    usable = PAGE_W - 36
    cell = usable / 20
    for i in range(21):
        xx = 18 + i * cell
        line(dwg, xx, 18, xx, 34, 0.8)
        if i < 20:
            txt(dwg, xx + cell / 2, 31, i + 1, 9, anchor="middle")

    txt(dwg, 60, 82, cfg.get("folio_title", "PUISSANCE"), 26, "bold")

    # cartouche bas
    rect(dwg, 1180, 1015, 560, 62, 1.0)
    line(dwg, 1535, 1015, 1535, 1077, 0.8)
    line(dwg, 1670, 1015, 1670, 1077, 0.8)

    txt(dwg, 1200, 1040, cfg.get("project_name", "Projet"), 12)
    txt(dwg, 1200, 1061, "FOLIO PUISSANCE", 12)
    txt(dwg, 1588, 1040, "FOLIO", 9)
    txt(dwg, 1612, 1066, "10", 22, "bold", "middle")


def draw_buses(dwg):
    line(dwg, 90, Y_L, 1710, Y_L, 1.8)
    line(dwg, 90, Y_N, 1710, Y_N, 1.8)
    line(dwg, 90, Y_PE, 1710, Y_PE, 1.8)

    txt(dwg, 58, Y_L + 4, "L", 14, "bold")
    txt(dwg, 58, Y_N + 4, "N", 14, "bold")
    txt(dwg, 46, Y_PE + 4, "PE", 14, "bold")


def draw_source(dwg):
    # petit cartouche source à gauche comme la référence
    rect(dwg, X_SRC - 28, 98, 38, 52, 0.8)
    txt(dwg, X_SRC - 9, 118, "Ph", 9, anchor="middle")
    txt(dwg, X_SRC - 9, 140, "N", 9, anchor="middle")


def draw_q1(dwg):
    x, y = X_Q1, Y_Q1
    txt(dwg, x + 18, y - 22, "Q1", 13, "bold", "middle")
    txt(dwg, x + 18, y - 8, "Disjoncteur général", 9, anchor="middle")

    # symbole vertical simple proche de la référence
    line(dwg, x + 18, y, x + 18, y + 18, 1.6)
    line(dwg, x + 18, y + 18, x + 35, y + 40, 1.6)
    line(dwg, x + 35, y + 40, x + 18, y + 40, 1.6)
    line(dwg, x + 18, y + 40, x + 18, y + 95, 1.6)

    txt(dwg, x + 45, y + 10, "1", 9)
    txt(dwg, x + 45, y + 84, "2", 9)


def draw_t1(dwg, cfg):
    if not cfg["transformer"].get("enabled", False):
        return
    x, y = X_T1, Y_T1

    txt(dwg, x + 45, y - 20, cfg["transformer"]["tag"], 13, "bold", "middle")
    txt(dwg, x + 45, y + 4, "230V", 10, anchor="middle")
    txt(dwg, x + 45, y + 22, "24V", 10, anchor="middle")

    line(dwg, x + 18, y - 5, x + 18, y + 15, 1.5)
    line(dwg, x + 68, y - 5, x + 68, y + 15, 1.5)

    dwg.add(dwg.circle(center=(x + 32, y + 48), r=17, fill="none", stroke="black", stroke_width=1.1))
    dwg.add(dwg.circle(center=(x + 56, y + 74), r=17, fill="none", stroke="black", stroke_width=1.1))

    line(dwg, x + 32, y + 91, x + 32, y + 118, 1.5)
    line(dwg, x + 80, y + 91, x + 80, y + 118, 1.5)

    # petite terre fonctionnelle
    line(dwg, x + 9, y + 83, x + 9, y + 96, 0.9)
    line(dwg, x + 2, y + 96, x + 16, y + 96, 0.9)
    line(dwg, x + 4, y + 100, x + 14, y + 100, 0.9)
    line(dwg, x + 6, y + 104, x + 12, y + 104, 0.9)

    txt(dwg, x + 8, y - 8, "P1", 8)
    txt(dwg, x + 58, y - 8, "P2", 8)
    txt(dwg, x + 26, y + 118, "S1", 8)
    txt(dwg, x + 74, y + 118, "S2", 8)


def draw_controller_feeds(dwg, cfg):
    if not cfg["controller"].get("enabled", False):
        return

    x1 = X_Q1 + 18
    x_n = X_Q1 + 75
    y_bus_out = Y_Q1 + 95
    y_drop = 560

    # conducteurs vers bas
    line(dwg, x1, y_bus_out, x1, y_drop, 1.1)
    line(dwg, x_n, Y_N, x_n, y_drop, 1.1)

    wire_no(dwg, x1 + 6, 470, "1001")
    wire_no(dwg, x_n + 6, 470, "1002")

    terminal_arrow_text(dwg, x1 - 8, y_drop + 22, f"{cfg['controller']['tag']} PRO1 N")
    terminal_arrow_text(dwg, x_n - 8, y_drop + 22, f"{cfg['controller']['tag']} PRO1 Ph")

    txt(dwg, (x1 + x_n) / 2, y_drop + 68, "Alim", 10, anchor="middle")
    txt(dwg, (x1 + x_n) / 2, y_drop + 88, cfg["controller"]["label"], 10, anchor="middle")


def draw_valve_feeds(dwg, cfg):
    if not cfg["power_supply"].get("enabled", False):
        return

    x24 = X_T1 + 32
    x0 = X_T1 + 80
    y_start = Y_T1 + 118
    y_drop = 560

    line(dwg, x24, y_start, x24, y_drop, 1.1)
    line(dwg, x0, y_start, x0, y_drop, 1.1)

    wire_no(dwg, x24 + 6, 470, "1003")
    wire_no(dwg, x0 + 6, 470, "1004")

    terminal_arrow_text(dwg, x24 - 8, y_drop + 22, "X1:7")
    terminal_arrow_text(dwg, x0 - 8, y_drop + 22, "X1:8")

    txt(dwg, (x24 + x0) / 2, y_drop + 68, "Alimentation", 10, anchor="middle")
    txt(dwg, (x24 + x0) / 2, y_drop + 88, "Vanne", 10, anchor="middle")


def draw_ps1(dwg, cfg):
    if not cfg["power_supply"].get("enabled", False):
        return
    x, y = X_PS1, Y_PS1
    txt(dwg, x + 40, y - 20, cfg["power_supply"]["tag"], 13, "bold", "middle")
    txt(dwg, x + 40, y - 4, cfg["power_supply"]["label"], 9, anchor="middle")
    rect(dwg, x, y + 8, 80, 60, 1.0)
    txt(dwg, x + 40, y + 45, "PS", 22, "bold", "middle")


def draw_dm1(dwg, cfg):
    if not cfg["pump"].get("enabled", False):
        return
    x, y = X_DM1, Y_DM1

    txt(dwg, x + 50, y - 18, cfg["pump"]["protection_tag"], 13, "bold", "middle")
    txt(dwg, x + 50, y, "Protection moteur", 9, anchor="middle")

    # arrivée 3 pôles en haut, rendu compact type protection moteur
    line(dwg, x + 18, y, x + 18, y + 18, 1.2)
    line(dwg, x + 50, y, x + 50, y + 18, 1.2)
    line(dwg, x + 82, y, x + 82, y + 18, 1.2)

    rect(dwg, x + 8, y + 18, 84, 98, 1.1)

    line(dwg, x + 18, y + 18, x + 18, y + 98, 1.0)
    line(dwg, x + 50, y + 18, x + 50, y + 98, 1.0)
    line(dwg, x + 82, y + 18, x + 82, y + 98, 1.0)

    # bas
    line(dwg, x + 18, y + 116, x + 18, y + 145, 1.2)
    line(dwg, x + 50, y + 116, x + 50, y + 145, 1.2)
    line(dwg, x + 82, y + 116, x + 82, y + 145, 1.2)

    txt(dwg, x + 12, y - 8, "1", 8)
    txt(dwg, x + 44, y - 8, "3", 8)
    txt(dwg, x + 76, y - 8, "5", 8)
    txt(dwg, x + 12, y + 132, "2", 8)
    txt(dwg, x + 44, y + 132, "4", 8)
    txt(dwg, x + 76, y + 132, "6", 8)


def draw_km1(dwg, cfg):
    if not cfg["pump"].get("enabled", False):
        return
    x, y = X_KM1, Y_KM1

    txt(dwg, x + 50, y - 18, cfg["pump"]["contactor_tag"], 13, "bold", "middle")
    txt(dwg, x + 50, y, "Contact puissance", 9, anchor="middle")

    # trois contacts visibles
    for xoff, topn, botn in [(18, "1", "2"), (50, "3", "4"), (82, "5", "6")]:
        line(dwg, x + xoff, y + 10, x + xoff, y + 34, 1.1)
        line(dwg, x + xoff + 10, y + 38, x + xoff + 10, y + 72, 1.1)
        line(dwg, x + xoff, y + 34, x + xoff + 10, y + 38, 1.1)
        txt(dwg, x + xoff - 3, y, topn, 8)
        txt(dwg, x + xoff + 7, y + 88, botn, 8)

    # pointillés de liaison mécanique
    line(dwg, x + 18, y + 10, x + 18, y + 150, 0.8, dash="3,3")
    line(dwg, x + 50, y + 10, x + 50, y + 150, 0.8, dash="3,3")
    line(dwg, x + 82, y + 10, x + 82, y + 150, 0.8, dash="3,3")


def draw_motor_chain(dwg, cfg):
    if not cfg["pump"].get("enabled", False):
        return

    # Liaisons DM -> KM -> M
    dm_x = X_DM1
    km_x = X_KM1
    m_x = X_M1
    m_y = Y_M1

    # sortie DM bas -> entrée KM haut
    for dm_off, km_off in [(18, 18), (50, 50), (82, 82)]:
        line(dwg, dm_x + dm_off, Y_DM1 + 145, km_x + km_off, Y_KM1 + 10, 1.1)

    # sortie KM -> moteur seulement 2 fils visibles vers U1/U2 comme la référence
    line(dwg, km_x + 18, Y_KM1 + 72, km_x + 18, m_y - 60, 1.1, dash="3,3")
    line(dwg, km_x + 50, Y_KM1 + 72, km_x + 50, m_y - 60, 1.1, dash="3,3")

    # renvoi bornier
    txt(dwg, km_x + 12, m_y - 74, "Brin 1", 8)
    txt(dwg, km_x + 44, m_y - 74, "Brin 2", 8)

    # petites pastilles terrain
    dwg.add(dwg.ellipse(center=(km_x - 80, m_y - 72), r=(28, 10), fill="none", stroke="black", stroke_width=0.8))
    txt(dwg, km_x - 80, m_y - 68, "P1-2", 8, anchor="middle")
    txt(dwg, km_x - 36, m_y - 72, "Brin 1", 8)
    txt(dwg, km_x - 6, m_y - 72, "Brin 2", 8)

    # moteur
    txt(dwg, m_x + 40, m_y - 32, cfg["pump"]["motor_tag"], 13, "bold", "middle")
    txt(dwg, m_x + 40, m_y - 12, cfg["pump"]["motor_label"], 9, anchor="middle")
    dwg.add(dwg.circle(center=(m_x + 40, m_y + 10), r=30, fill="none", stroke="black", stroke_width=1.2))
    txt(dwg, m_x + 40, m_y + 17, "M", 20, "bold", "middle")
    txt(dwg, m_x - 10, m_y - 5, "U1", 8)
    txt(dwg, m_x + 22, m_y - 5, "U2", 8)
    txt(dwg, m_x - 24, m_y + 12, "1~", 9)
    txt(dwg, m_x - 38, m_y - 18, "145 W", 9)
    txt(dwg, m_x - 34, m_y - 2, "1.5 A", 9)

    # arrivée moteur
    line(dwg, km_x + 18, m_y - 60, m_x + 10, m_y - 20, 1.1, dash="3,3")
    line(dwg, km_x + 50, m_y - 60, m_x + 42, m_y - 20, 1.1, dash="3,3")

    # terre moteur
    line(dwg, m_x + 70, m_y + 16, m_x + 100, m_y + 16, 1.0)
    line(dwg, m_x + 100, m_y + 16, m_x + 100, m_y + 28, 1.0)
    line(dwg, m_x + 88, m_y + 28, m_x + 112, m_y + 28, 1.0)
    line(dwg, m_x + 92, m_y + 33, m_x + 108, m_y + 33, 1.0)
    line(dwg, m_x + 96, m_y + 38, m_x + 104, m_y + 38, 1.0)


def draw_wires_left(dwg, cfg):
    qx = X_Q1 + 18
    qy = Y_Q1 + 95

    # arrivée source -> Q1
    line(dwg, qx, Y_L, qx, Y_Q1, 1.1)
    node(dwg, qx, Y_L)
    wire_no(dwg, qx + 8, Y_L - 3, "0")

    # Q1 -> T1 P1
    if cfg["transformer"].get("enabled", False):
        line(dwg, qx, qy, X_T1 + 18, qy, 1.1)
        line(dwg, X_T1 + 18, qy, X_T1 + 18, Y_T1 - 5, 1.1)
        wire_no(dwg, (qx + X_T1 + 18) / 2, qy - 4, "1001")

    # N -> T1 P2
    if cfg["transformer"].get("enabled", False):
        line(dwg, X_T1 + 68, Y_N, X_T1 + 68, Y_T1 - 5, 1.1)
        node(dwg, X_T1 + 68, Y_N)
        wire_no(dwg, X_T1 + 74, 260, "1002")

    # Q1 -> PS1
    if cfg["power_supply"].get("enabled", False):
        line(dwg, qx, qy + 24, X_PS1, qy + 24, 1.1)
        line(dwg, X_PS1, qy + 24, X_PS1, Y_PS1 + 20, 1.1)
        wire_no(dwg, (qx + X_PS1) / 2, qy + 20, "5")

        line(dwg, X_PS1 + 104, Y_N, X_PS1 + 104, Y_PS1 + 48, 1.1)
        node(dwg, X_PS1 + 104, Y_N)
        wire_no(dwg, X_PS1 + 110, 300, "6")

    # Q1 -> A1 petite alimentation
    if cfg["controller"].get("enabled", False):
        line(dwg, qx, qy, X_A1, qy, 1.1)
        line(dwg, X_A1, qy, X_A1, Y_A1 + 24, 1.1)
        wire_no(dwg, (qx + X_A1) / 2, qy - 4, "1")

        line(dwg, X_A1 + 110, Y_N, X_A1 + 110, Y_A1 + 48, 1.1)
        node(dwg, X_A1 + 110, Y_N)
        wire_no(dwg, X_A1 + 116, 312, "2")


def draw_wires_right(dwg, cfg):
    if not cfg["pump"].get("enabled", False):
        return

    # arrivée DM1 depuis barre L
    line(dwg, X_DM1 + 18, Y_L, X_DM1 + 18, Y_DM1, 1.1)
    line(dwg, X_DM1 + 50, Y_L, X_DM1 + 50, Y_DM1, 1.1)
    line(dwg, X_DM1 + 82, Y_L, X_DM1 + 82, Y_DM1, 1.1)
    node(dwg, X_DM1 + 18, Y_L)
    node(dwg, X_DM1 + 50, Y_L)
    node(dwg, X_DM1 + 82, Y_L)

    # repère fil principal
    wire_no(dwg, X_DM1 + 88, 245, "10")


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
    draw_t1(dwg, cfg)
    draw_controller_feeds(dwg, cfg)
    draw_valve_feeds(dwg, cfg)
    draw_ps1(dwg, cfg)
    draw_dm1(dwg, cfg)
    draw_km1(dwg, cfg)
    draw_motor_chain(dwg, cfg)
    draw_wires_left(dwg, cfg)
    draw_wires_right(dwg, cfg)

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
