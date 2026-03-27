import json
from pathlib import Path

import streamlit as st
import svgwrite

PAGE_W = 1800
PAGE_H = 1100

Y_L = 130
Y_N = 160
Y_PE = 190

X = {
    "Q1": 220,
    "A1": 430,
    "T1": 650,
    "PS1": 900,
    "DM1": 1180,
    "KM1": 1180,
    "X1": 1430,
    "YV1": 1570,
    "M1": 1540,
}

Y = {
    "Q1": 230,
    "A1": 340,
    "T1": 340,
    "PS1": 340,
    "DM1": 230,
    "KM1": 520,
    "X1": 500,
    "YV1": 340,
    "M1": 760,
}


def load_config() -> dict:
    config_path = Path("config_installation.json")
    if not config_path.exists():
        raise FileNotFoundError("Le fichier config_installation.json est introuvable.")
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def line(dwg, x1, y1, x2, y2, w=1.6):
    dwg.add(dwg.line((x1, y1), (x2, y2), stroke="black", stroke_width=w))


def rect(dwg, x, y, w, h, sw=1.2):
    dwg.add(dwg.rect((x, y), (w, h), fill="none", stroke="black", stroke_width=sw))


def txt(dwg, x, y, value, size=14, weight="normal", anchor="start"):
    dwg.add(
        dwg.text(
            value,
            insert=(x, y),
            font_size=f"{size}px",
            font_weight=weight,
            text_anchor=anchor,
            font_family="Arial",
        )
    )


def node(dwg, x, y, r=3):
    dwg.add(dwg.circle(center=(x, y), r=r, fill="black"))


def wire_no(dwg, x, y, value):
    txt(dwg, x, y, value, 11, "bold")


def xref(dwg, x, y, value):
    rect(dwg, x, y - 14, 118, 22, 1)
    txt(dwg, x + 6, y + 2, value, 10)


def draw_frame(dwg, cfg):
    rect(dwg, 15, 15, PAGE_W - 30, PAGE_H - 30, 1.4)
    rect(dwg, 30, 30, PAGE_W - 60, PAGE_H - 140, 1)

    cell = (PAGE_W - 60) / 20
    for i in range(21):
        xx = 30 + i * cell
        line(dwg, xx, 30, xx, 48, 1)
        if i < 20:
            txt(dwg, xx + cell / 2, 43, str(i + 1), 11, anchor="middle")

    txt(dwg, 70, 90, cfg.get("folio_title", "PUISSANCE"), 28, "bold")

    cx = 1160
    cy = 1045
    rect(dwg, cx, cy, 600, 60, 1)
    line(dwg, cx + 460, cy, cx + 460, cy + 60, 1)
    txt(dwg, cx + 18, cy + 24, cfg.get("project_name", "Projet"), 15)
    txt(dwg, cx + 18, cy + 47, "FOLIO PUISSANCE", 15, "bold")
    txt(dwg, cx + 490, cy + 22, "FOLIO", 11)
    txt(dwg, cx + 512, cy + 47, "10", 22, "bold")


def draw_buses(dwg):
    line(dwg, 70, Y_L, 1730, Y_L, 2)
    line(dwg, 70, Y_N, 1730, Y_N, 2)
    line(dwg, 70, Y_PE, 1730, Y_PE, 2)
    txt(dwg, 42, Y_L + 5, "L", 16, "bold")
    txt(dwg, 42, Y_N + 5, "N", 16, "bold")
    txt(dwg, 30, Y_PE + 5, "PE", 16, "bold")


def draw_q1(dwg):
    x, y = X["Q1"], Y["Q1"]
    txt(dwg, x + 28, y - 22, "Q1", 15, "bold", "middle")
    txt(dwg, x + 28, y - 6, "Disjoncteur général", 11, anchor="middle")
    cx = x + 28
    line(dwg, cx, y, cx, y + 12, 2)
    line(dwg, cx, y + 12, cx + 18, y + 35, 2)
    line(dwg, cx + 18, y + 35, cx, y + 35, 2)
    line(dwg, cx, y + 35, cx, y + 92, 2)


def draw_controller(dwg, cfg):
    controller = cfg["controller"]
    if not controller.get("enabled", False):
        return
    x, y = X["A1"], Y["A1"]
    txt(dwg, x + 55, y - 22, controller["tag"], 15, "bold", "middle")
    txt(dwg, x + 55, y - 6, controller["label"], 11, anchor="middle")
    rect(dwg, x, y, 110, 84)
    txt(dwg, x + 55, y + 50, "MXPRO", 18, "bold", "middle")


def draw_transformer(dwg, cfg):
    transformer = cfg["transformer"]
    if not transformer.get("enabled", False):
        return
    x, y = X["T1"], Y["T1"]
    txt(dwg, x + 44, y - 22, transformer["tag"], 15, "bold", "middle")
    txt(dwg, x + 44, y - 6, transformer["label"], 11, anchor="middle")
    line(dwg, x + 18, y, x + 18, y + 18, 2)
    line(dwg, x + 70, y, x + 70, y + 18, 2)
    dwg.add(dwg.circle(center=(x + 32, y + 44), r=15, fill="none", stroke="black", stroke_width=1.3))
    dwg.add(dwg.circle(center=(x + 56, y + 44), r=15, fill="none", stroke="black", stroke_width=1.3))
    line(dwg, x + 18, y + 72, x + 18, y + 106, 2)
    line(dwg, x + 70, y + 72, x + 70, y + 106, 2)
    txt(dwg, x + 10, y - 3, "P1", 9)
    txt(dwg, x + 62, y - 3, "P2", 9)
    txt(dwg, x + 10, y + 103, "S1", 9)
    txt(dwg, x + 62, y + 103, "S2", 9)


def draw_power_supply(dwg, cfg):
    ps = cfg["power_supply"]
    if not ps.get("enabled", False):
        return
    x, y = X["PS1"], Y["PS1"]
    txt(dwg, x + 52, y - 22, ps["tag"], 15, "bold", "middle")
    txt(dwg, x + 52, y - 6, ps["label"], 11, anchor="middle")
    rect(dwg, x, y, 104, 82)
    txt(dwg, x + 52, y + 49, "PS", 22, "bold", "middle")


def draw_pump_chain(dwg, cfg):
    pump = cfg["pump"]
    if not pump.get("enabled", False):
        return

    # DM1
    x, y = X["DM1"], Y["DM1"]
    txt(dwg, x + 38, y - 22, pump["protection_tag"], 15, "bold", "middle")
    txt(dwg, x + 38, y - 6, "Protection moteur", 11, anchor="middle")
    rect(dwg, x + 8, y + 8, 60, 82)
    line(dwg, x + 38, y, x + 38, y + 8, 2)
    line(dwg, x + 38, y + 90, x + 38, y + 122, 2)
    txt(dwg, x + 38, y + 56, "DM", 20, "bold", "middle")

    # KM1
    x, y = X["KM1"], Y["KM1"]
    txt(dwg, x + 38, y - 22, pump["contactor_tag"], 15, "bold", "middle")
    txt(dwg, x + 38, y - 6, "Contact puissance", 11, anchor="middle")
    line(dwg, x + 38, y, x + 38, y + 18, 2)
    line(dwg, x + 20, y + 24, x + 20, y + 76, 1.5)
    line(dwg, x + 56, y + 24, x + 56, y + 76, 1.5)
    line(dwg, x + 20, y + 50, x + 56, y + 50, 2)
    line(dwg, x + 38, y + 76, x + 38, y + 112, 2)

    # M1
    x, y = X["M1"], Y["M1"]
    txt(dwg, x + 56, y - 24, pump["motor_tag"], 15, "bold", "middle")
    txt(dwg, x + 56, y - 8, pump["motor_label"], 11, anchor="middle")
    line(dwg, x, y + 20, x + 24, y + 20, 1.4)
    line(dwg, x, y + 50, x + 24, y + 50, 1.4)
    dwg.add(dwg.circle(center=(x + 62, y + 38), r=30, fill="none", stroke="black", stroke_width=1.4))
    txt(dwg, x + 62, y + 46, "M", 22, "bold", "middle")
    gx = x + 62
    gy = y + 96
    line(dwg, gx, gy - 8, gx, gy, 1.1)
    line(dwg, gx - 12, gy, gx + 12, gy, 1.1)
    line(dwg, gx - 8, gy + 5, gx + 8, gy + 5, 1.1)
    line(dwg, gx - 4, gy + 10, gx + 4, gy + 10, 1.1)


def draw_terminal_block(dwg, cfg):
    tb = cfg["terminal_block"]
    if not tb.get("enabled", False):
        return
    x, y = X["X1"], Y["X1"]
    txt(dwg, x + 36, y - 22, tb["tag"], 15, "bold", "middle")
    txt(dwg, x + 36, y - 6, "Bornier terrain", 11, anchor="middle")
    rect(dwg, x, y, 72, 180)
    for lab, dy in zip(["5", "6", "7", "8"], [35, 70, 105, 140]):
        yy = y + dy
        line(dwg, x, yy, x + 72, yy, 1)
        txt(dwg, x + 10, yy - 8, lab, 11)


def draw_valve(dwg, cfg):
    valve = cfg["valve"]
    if not valve.get("enabled", False):
        return
    x, y = X["YV1"], Y["YV1"]
    txt(dwg, x + 42, y - 22, valve["tag"], 15, "bold", "middle")
    txt(dwg, x + 42, y - 6, valve["label"], 11, anchor="middle")
    rect(dwg, x, y, 84, 74)
    txt(dwg, x + 42, y + 46, "YV", 20, "bold", "middle")


def draw_supply_drops(dwg, cfg):
    q1x = X["Q1"] + 28
    line(dwg, q1x, Y_L, q1x, Y["Q1"], 1.4)
    node(dwg, q1x, Y_L)
    wire_no(dwg, q1x + 8, Y_L - 6, "0")

    if cfg["controller"].get("enabled", False):
        a1n = X["A1"]
        line(dwg, a1n, Y_N, a1n, Y["A1"] + 60, 1.2)
        node(dwg, a1n, Y_N)
        wire_no(dwg, a1n + 8, Y["A1"] + 38, "2")

    if cfg["transformer"].get("enabled", False):
        t1n = X["T1"] + 70
        line(dwg, t1n, Y_N, t1n, Y["T1"], 1.2)
        node(dwg, t1n, Y_N)
        wire_no(dwg, t1n + 8, Y["T1"] - 8, "4")

    if cfg["power_supply"].get("enabled", False):
        ps1n = X["PS1"]
        line(dwg, ps1n, Y_N, ps1n, Y["PS1"] + 60, 1.2)
        node(dwg, ps1n, Y_N)
        wire_no(dwg, ps1n + 8, Y["PS1"] + 38, "6")

    if cfg["terminal_block"].get("enabled", False):
        x1n = X["X1"]
        line(dwg, x1n, Y_N, x1n, Y["X1"] + 70, 1.2)
        node(dwg, x1n, Y_N)
        wire_no(dwg, x1n + 8, Y["X1"] + 28, "14")

    if cfg["pump"].get("enabled", False):
        mex = X["M1"] + 62
        line(dwg, mex, Y_PE, mex, Y["M1"] + 96, 1.2)
        node(dwg, mex, Y_PE)
        wire_no(dwg, mex + 8, Y_PE - 6, "16")


def draw_wires(dwg, cfg):
    q1_out = (X["Q1"] + 28, Y["Q1"] + 92)

    if cfg["controller"].get("enabled", False):
        a1_l = (X["A1"], Y["A1"] + 24)
        line(dwg, q1_out[0], q1_out[1], q1_out[0], a1_l[1], 1.2)
        line(dwg, q1_out[0], a1_l[1], a1_l[0], a1_l[1], 1.2)
        wire_no(dwg, (q1_out[0] + a1_l[0]) / 2, a1_l[1] - 6, "1")

    if cfg["transformer"].get("enabled", False):
        t1_p1 = (X["T1"] + 18, Y["T1"])
        line(dwg, q1_out[0], q1_out[1], q1_out[0], t1_p1[1], 1.2)
        line(dwg, q1_out[0], t1_p1[1], t1_p1[0], t1_p1[1], 1.2)
        wire_no(dwg, (q1_out[0] + t1_p1[0]) / 2, t1_p1[1] - 6, "3")

        s1 = (X["T1"] + 18, Y["T1"] + 106)
        s2 = (X["T1"] + 70, Y["T1"] + 106)
        line(dwg, s1[0], s1[1], s1[0], s1[1] + 82, 1.2)
        wire_no(dwg, s1[0] + 8, s1[1] + 42, "20")
        xref(dwg, s1[0] + 18, s1[1] + 84, "→ 11 T1")

        line(dwg, s2[0], s2[1], s2[0], s2[1] + 112, 1.2)
        wire_no(dwg, s2[0] + 8, s2[1] + 56, "21")
        xref(dwg, s2[0] + 18, s2[1] + 114, "→ 11 T1")

    if cfg["power_supply"].get("enabled", False):
        ps1_l = (X["PS1"], Y["PS1"] + 24)
        line(dwg, q1_out[0], q1_out[1], q1_out[0], ps1_l[1], 1.2)
        line(dwg, q1_out[0], ps1_l[1], ps1_l[0], ps1_l[1], 1.2)
        wire_no(dwg, (q1_out[0] + ps1_l[0]) / 2, ps1_l[1] - 6, "5")

    if cfg["pump"].get("enabled", False):
        dm1_in = (X["DM1"] + 38, Y["DM1"])
        line(dwg, q1_out[0], q1_out[1], q1_out[0], dm1_in[1], 1.2)
        line(dwg, q1_out[0], dm1_in[1], dm1_in[0], dm1_in[1], 1.2)
        wire_no(dwg, (q1_out[0] + dm1_in[0]) / 2, dm1_in[1] - 6, "10")

        dm1_out = (X["DM1"] + 38, Y["DM1"] + 122)
        km1_in = (X["KM1"] + 38, Y["KM1"])
        line(dwg, dm1_out[0], dm1_out[1], dm1_out[0], km1_in[1] - 38, 1.2)
        line(dwg, dm1_out[0], km1_in[1] - 38, km1_in[0], km1_in[1] - 38, 1.2)
        line(dwg, km1_in[0], km1_in[1] - 38, km1_in[0], km1_in[1], 1.2)
        wire_no(dwg, km1_in[0] + 8, km1_in[1] - 44, "11")

        if cfg["terminal_block"].get("enabled", False):
            km1_out = (X["KM1"] + 38, Y["KM1"] + 112)
            x1_5 = (X["X1"], Y["X1"] + 35)
            line(dwg, km1_out[0], km1_out[1], km1_out[0], x1_5[1], 1.2)
            line(dwg, km1_out[0], x1_5[1], x1_5[0], x1_5[1], 1.2)
            wire_no(dwg, (km1_out[0] + x1_5[0]) / 2, x1_5[1] - 6, "12")
            txt(dwg, x1_5[0] + 8, x1_5[1] + 14, "X1.5", 10)

            m1_l = (X["M1"], Y["M1"] + 20)
            line(dwg, x1_5[0], x1_5[1], x1_5[0], m1_l[1], 1.2)
            line(dwg, x1_5[0], m1_l[1], m1_l[0], m1_l[1], 1.2)
            wire_no(dwg, (x1_5[0] + m1_l[0]) / 2, m1_l[1] - 6, "13")

            x1_6 = (X["X1"], Y["X1"] + 70)
            m1_n = (X["M1"], Y["M1"] + 50)
            line(dwg, x1_6[0], x1_6[1], x1_6[0], m1_n[1], 1.2)
            line(dwg, x1_6[0], m1_n[1], m1_n[0], m1_n[1], 1.2)
            wire_no(dwg, (x1_6[0] + m1_n[0]) / 2, m1_n[1] - 6, "15")
            txt(dwg, x1_6[0] + 8, x1_6[1] + 14, "X1.6", 10)

        kref_y = Y["KM1"] + 18
        line(dwg, X["KM1"] + 38, kref_y, X["KM1"] + 150, kref_y, 1.2)
        wire_no(dwg, X["KM1"] + 78, kref_y - 6, "17")
        xref(dwg, X["KM1"] + 160, kref_y, "→ 11 KM1")

    if cfg["power_supply"].get("enabled", False) and cfg["terminal_block"].get("enabled", False) and cfg["valve"].get("enabled", False):
        ps1_24 = (X["PS1"] + 104, Y["PS1"] + 24)
        x1_7 = (X["X1"], Y["X1"] + 105)
        line(dwg, ps1_24[0], ps1_24[1], X["X1"] - 40, ps1_24[1], 1.2)
        line(dwg, X["X1"] - 40, ps1_24[1], X["X1"] - 40, x1_7[1], 1.2)
        line(dwg, X["X1"] - 40, x1_7[1], x1_7[0], x1_7[1], 1.2)
        wire_no(dwg, X["X1"] - 62, x1_7[1] - 6, "30")
        txt(dwg, x1_7[0] + 8, x1_7[1] + 14, "X1.7", 10)

        yv1_24 = (X["YV1"], Y["YV1"] + 24)
        line(dwg, x1_7[0], x1_7[1], yv1_24[0], x1_7[1], 1.2)
        line(dwg, yv1_24[0], x1_7[1], yv1_24[0], yv1_24[1], 1.2)
        wire_no(dwg, (x1_7[0] + yv1_24[0]) / 2, x1_7[1] - 6, "32")

        ps1_0v = (X["PS1"] + 104, Y["PS1"] + 58)
        x1_8 = (X["X1"], Y["X1"] + 140)
        line(dwg, ps1_0v[0], ps1_0v[1], X["X1"] - 15, ps1_0v[1], 1.2)
        line(dwg, X["X1"] - 15, ps1_0v[1], X["X1"] - 15, x1_8[1], 1.2)
        line(dwg, X["X1"] - 15, x1_8[1], x1_8[0], x1_8[1], 1.2)
        wire_no(dwg, X["X1"] - 37, x1_8[1] - 6, "31")
        txt(dwg, x1_8[0] + 8, x1_8[1] + 14, "X1.8", 10)

        yv1_0v = (X["YV1"], Y["YV1"] + 56)
        line(dwg, x1_8[0], x1_8[1], yv1_0v[0], x1_8[1], 1.2)
        line(dwg, yv1_0v[0], x1_8[1], yv1_0v[0], yv1_0v[1], 1.2)
        wire_no(dwg, (x1_8[0] + yv1_0v[0]) / 2, x1_8[1] - 6, "33")

        aoref_y = Y["YV1"] + 24
        line(dwg, X["YV1"], aoref_y, X["YV1"] + 120, aoref_y, 1.2)
        wire_no(dwg, X["YV1"] + 48, aoref_y - 6, "34")
        xref(dwg, X["YV1"] + 130, aoref_y, "→ 11 YV1 AO")


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
    draw_q1(dwg)
    draw_controller(dwg, cfg)
    draw_transformer(dwg, cfg)
    draw_power_supply(dwg, cfg)
    draw_pump_chain(dwg, cfg)
    draw_terminal_block(dwg, cfg)
    draw_valve(dwg, cfg)
    draw_supply_drops(dwg, cfg)
    draw_wires(dwg, cfg)

    html = f"""
    <div style="width:100%;overflow:auto;background:white;border:1px solid #bbb;">
        <div style="min-width:1550px;padding:8px;">
            {dwg.tostring()}
        </div>
    </div>
    """

    st.subheader("Folio 10 - Puissance")
    st.components.v1.html(html, height=980, scrolling=True)

    with st.expander("Configuration chargée"):
        st.json(cfg)
