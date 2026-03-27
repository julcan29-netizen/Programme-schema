# folio_power.py
import streamlit as st
import svgwrite

PAGE_W = 1800
PAGE_H = 1150

# Cadre utile
LEFT = 80
RIGHT = 1720
TOP = 70
BOTTOM = 1040

# Barres
Y_L = 140
Y_N = 175
Y_PE = 210

# Colonnes principales
X_Q1 = 220
X_A1 = 430
X_T1 = 650
X_PS1 = 900
X_DM1 = 1210
X_KM1 = 1210
X_X1 = 1450
X_YV1 = 1590
X_M1 = 1560

# Niveaux
Y_Q1 = 250
Y_A1 = 330
Y_T1 = 330
Y_PS1 = 330
Y_DM1 = 250
Y_KM1 = 520
Y_X1 = 500
Y_YV1 = 330
Y_M1 = 760


def line(dwg, x1, y1, x2, y2, w=1.8):
    dwg.add(dwg.line((x1, y1), (x2, y2), stroke="black", stroke_width=w))


def rect(dwg, x, y, w, h, sw=1.5):
    dwg.add(dwg.rect((x, y), (w, h), fill="none", stroke="black", stroke_width=sw))


def text(dwg, x, y, value, size=14, weight="normal", anchor="start"):
    dwg.add(
        dwg.text(
            value,
            insert=(x, y),
            font_size=f"{size}px",
            font_weight=weight,
            text_anchor=anchor,
            font_family="Arial"
        )
    )


def node(dwg, x, y, r=4):
    dwg.add(dwg.circle(center=(x, y), r=r, fill="black"))


def wire_no(dwg, x, y, value):
    text(dwg, x, y, value, size=11, weight="bold")


def xref(dwg, x, y, value):
    rect(dwg, x, y - 14, 118, 22, 1)
    text(dwg, x + 6, y + 2, value, size=10)


def draw_frame(dwg):
    rect(dwg, 15, 15, PAGE_W - 30, PAGE_H - 30, 1.5)
    rect(dwg, 30, 30, PAGE_W - 60, PAGE_H - 150, 1)

    # Grille haute 1..20
    usable = PAGE_W - 60
    cell = usable / 20
    for i in range(21):
        x = 30 + i * cell
        line(dwg, x, 30, x, 48, 1)
        if i < 20:
            text(dwg, x + cell / 2, 43, str(i + 1), size=11, anchor="middle")

    text(dwg, 70, 95, "PUISSANCE", size=28, weight="bold")

    # Cartouche
    cx = 1170
    cy = 1065
    rect(dwg, cx, cy, 590, 60, 1)
    line(dwg, cx + 455, cy, cx + 455, cy + 60, 1)
    text(dwg, cx + 18, cy + 24, "CUISINE CENTRALE", size=15)
    text(dwg, cx + 18, cy + 47, "FOLIO PUISSANCE", size=15, weight="bold")
    text(dwg, cx + 485, cy + 22, "FOLIO", size=11)
    text(dwg, cx + 505, cy + 47, "10", size=22, weight="bold")


def draw_buses(dwg):
    line(dwg, LEFT, Y_L, RIGHT, Y_L, 2)
    line(dwg, LEFT, Y_N, RIGHT, Y_N, 2)
    line(dwg, LEFT, Y_PE, RIGHT, Y_PE, 2)

    text(dwg, 45, Y_L + 5, "L", size=17, weight="bold")
    text(dwg, 45, Y_N + 5, "N", size=17, weight="bold")
    text(dwg, 35, Y_PE + 5, "PE", size=17, weight="bold")


def draw_q1(dwg):
    x, y = X_Q1, Y_Q1
    text(dwg, x + 28, y - 24, "Q1", 15, "bold", "middle")
    text(dwg, x + 28, y - 8, "Disjoncteur général", 11, "middle")

    cx = x + 28
    line(dwg, cx, y, cx, y + 15, 2)
    line(dwg, cx, y + 15, cx + 18, y + 38, 2)
    line(dwg, cx + 18, y + 38, cx, y + 38, 2)
    line(dwg, cx, y + 38, cx, y + 92, 2)


def draw_a1(dwg):
    x, y = X_A1, Y_A1
    text(dwg, x + 52, y - 24, "A1", 15, "bold", "middle")
    text(dwg, x + 52, y - 8, "Régulateur MXPRO", 11, "middle")
    rect(dwg, x, y, 104, 82)
    text(dwg, x + 52, y + 50, "MXPRO", 18, "bold", "middle")


def draw_t1(dwg):
    x, y = X_T1, Y_T1
    text(dwg, x + 45, y - 24, "T1", 15, "bold", "middle")
    text(dwg, x + 45, y - 8, "Transformateur 230/24V", 11, "middle")

    line(dwg, x + 18, y, x + 18, y + 18, 2)
    line(dwg, x + 70, y, x + 70, y + 18, 2)

    dwg.add(dwg.circle(center=(x + 32, y + 46), r=15, fill="none", stroke="black", stroke_width=1.4))
    dwg.add(dwg.circle(center=(x + 56, y + 46), r=15, fill="none", stroke="black", stroke_width=1.4))

    line(dwg, x + 18, y + 74, x + 18, y + 108, 2)
    line(dwg, x + 70, y + 74, x + 70, y + 108, 2)

    text(dwg, x + 10, y - 4, "P1", 9)
    text(dwg, x + 62, y - 4, "P2", 9)
    text(dwg, x + 10, y + 104, "S1", 9)
    text(dwg, x + 62, y + 104, "S2", 9)


def draw_ps1(dwg):
    x, y = X_PS1, Y_PS1
    text(dwg, x + 52, y - 24, "PS1", 15, "bold", "middle")
    text(dwg, x + 52, y - 8, "Alimentation vanne 24V", 11, "middle")
    rect(dwg, x, y, 104, 82)
    text(dwg, x + 52, y + 50, "PS", 22, "bold", "middle")


def draw_dm1(dwg):
    x, y = X_DM1, Y_DM1
    text(dwg, x + 38, y - 24, "DM1", 15, "bold", "middle")
    text(dwg, x + 38, y - 8, "Protection moteur", 11, "middle")
    rect(dwg, x + 8, y + 8, 60, 82)
    line(dwg, x + 38, y, x + 38, y + 8, 2)
    line(dwg, x + 38, y + 90, x + 38, y + 122, 2)
    text(dwg, x + 38, y + 57, "DM", 20, "bold", "middle")


def draw_km1(dwg):
    x, y = X_KM1, Y_KM1
    text(dwg, x + 38, y - 24, "KM1", 15, "bold", "middle")
    text(dwg, x + 38, y - 8, "Contact puissance", 11, "middle")

    line(dwg, x + 38, y, x + 38, y + 18, 2)
    line(dwg, x + 20, y + 24, x + 20, y + 76, 1.5)
    line(dwg, x + 56, y + 24, x + 56, y + 76, 1.5)
    line(dwg, x + 20, y + 50, x + 56, y + 50, 2)
    line(dwg, x + 38, y + 76, x + 38, y + 112, 2)


def draw_x1(dwg):
    x, y = X_X1, Y_X1
    text(dwg, x + 36, y - 24, "X1", 15, "bold", "middle")
    text(dwg, x + 36, y - 8, "Bornier terrain", 11, "middle")
    rect(dwg, x, y, 72, 180)

    positions = [35, 70, 105, 140]
    labels = ["5", "6", "7", "8"]
    for lab, dy in zip(labels, positions):
        yy = y + dy
        line(dwg, x, yy, x + 72, yy, 1)
        text(dwg, x + 10, yy - 8, lab, 11)


def draw_yv1(dwg):
    x, y = X_YV1, Y_YV1
    text(dwg, x + 42, y - 24, "YV1", 15, "bold", "middle")
    text(dwg, x + 42, y - 8, "Vanne 3 voies modulante", 11, "middle")
    rect(dwg, x, y, 84, 74)
    text(dwg, x + 42, y + 47, "YV", 20, "bold", "middle")


def draw_m1(dwg):
    x, y = X_M1, Y_M1
    text(dwg, x + 55, y - 28, "M1", 15, "bold", "middle")
    text(dwg, x + 55, y - 10, "Circulateur", 11, "middle")

    line(dwg, x, y + 20, x + 24, y + 20, 1.5)
    line(dwg, x, y + 50, x + 24, y + 50, 1.5)

    dwg.add(dwg.circle(center=(x + 62, y + 38), r=30, fill="none", stroke="black", stroke_width=1.5))
    text(dwg, x + 62, y + 46, "M", 22, "bold", "middle")

    gx = x + 62
    gy = y + 96
    line(dwg, gx, gy - 8, gx, gy, 1.2)
    line(dwg, gx - 12, gy, gx + 12, gy, 1.2)
    line(dwg, gx - 8, gy + 5, gx + 8, gy + 5, 1.2)
    line(dwg, gx - 4, gy + 10, gx + 4, gy + 10, 1.2)


def draw_supply_drops(dwg):
    # L -> Q1
    q1x = X_Q1 + 28
    line(dwg, q1x, Y_L, q1x, Y_Q1, 1.5)
    node(dwg, q1x, Y_L)
    wire_no(dwg, q1x + 8, Y_L - 6, "0")

    # N -> A1
    a1n = X_A1
    line(dwg, a1n, Y_N, a1n, Y_A1 + 58, 1.3)
    node(dwg, a1n, Y_N)
    wire_no(dwg, a1n + 8, Y_A1 + 35, "2")

    # N -> T1 P2
    t1n = X_T1 + 70
    line(dwg, t1n, Y_N, t1n, Y_T1, 1.3)
    node(dwg, t1n, Y_N)
    wire_no(dwg, t1n + 8, Y_T1 - 8, "4")

    # N -> PS1
    ps1n = X_PS1
    line(dwg, ps1n, Y_N, ps1n, Y_PS1 + 58, 1.3)
    node(dwg, ps1n, Y_N)
    wire_no(dwg, ps1n + 8, Y_PS1 + 35, "6")

    # N -> X1.6
    x1n = X_X1
    line(dwg, x1n, Y_N, x1n, Y_X1 + 70, 1.3)
    node(dwg, x1n, Y_N)
    wire_no(dwg, x1n + 8, Y_X1 + 30, "14")

    # PE -> M1
    mex = X_M1 + 62
    line(dwg, mex, Y_PE, mex, Y_M1 + 96, 1.3)
    node(dwg, mex, Y_PE)
    wire_no(dwg, mex + 8, Y_PE - 6, "16")


def draw_wires(dwg):
    q1_out = (X_Q1 + 28, Y_Q1 + 92)

    # Q1 -> A1
    a1_l = (X_A1, Y_A1 + 24)
    line(dwg, q1_out[0], q1_out[1], q1_out[0], a1_l[1], 1.3)
    line(dwg, q1_out[0], a1_l[1], a1_l[0], a1_l[1], 1.3)
    wire_no(dwg, (q1_out[0] + a1_l[0]) / 2, a1_l[1] - 6, "1")

    # Q1 -> T1 P1
    t1_p1 = (X_T1 + 18, Y_T1)
    line(dwg, q1_out[0], q1_out[1], q1_out[0], t1_p1[1], 1.3)
    line(dwg, q1_out[0], t1_p1[1], t1_p1[0], t1_p1[1], 1.3)
    wire_no(dwg, (q1_out[0] + t1_p1[0]) / 2, t1_p1[1] - 6, "3")

    # Q1 -> PS1
    ps1_l = (X_PS1, Y_PS1 + 24)
    line(dwg, q1_out[0], q1_out[1], q1_out[0], ps1_l[1], 1.3)
    line(dwg, q1_out[0], ps1_l[1], ps1_l[0], ps1_l[1], 1.3)
    wire_no(dwg, (q1_out[0] + ps1_l[0]) / 2, ps1_l[1] - 6, "5")

    # Q1 -> DM1
    dm1_in = (X_DM1 + 38, Y_DM1)
    line(dwg, q1_out[0], q1_out[1], q1_out[0], dm1_in[1], 1.3)
    line(dwg, q1_out[0], dm1_in[1], dm1_in[0], dm1_in[1], 1.3)
    wire_no(dwg, (q1_out[0] + dm1_in[0]) / 2, dm1_in[1] - 6, "10")

    # DM1 -> KM1
    dm1_out = (X_DM1 + 38, Y_DM1 + 122)
    km1_in = (X_KM1 + 38, Y_KM1)
    line(dwg, dm1_out[0], dm1_out[1], dm1_out[0], km1_in[1] - 36, 1.3)
    line(dwg, dm1_out[0], km1_in[1] - 36, km1_in[0], km1_in[1] - 36, 1.3)
    line(dwg, km1_in[0], km1_in[1] - 36, km1_in[0], km1_in[1], 1.3)
    wire_no(dwg, km1_in[0] + 8, km1_in[1] - 42, "11")

    # KM1 -> X1.5
    km1_out = (X_KM1 + 38, Y_KM1 + 112)
    x1_5 = (X_X1, Y_X1 + 35)
    line(dwg, km1_out[0], km1_out[1], km1_out[0], x1_5[1], 1.3)
    line(dwg, km1_out[0], x1_5[1], x1_5[0], x1_5[1], 1.3)
    wire_no(dwg, (km1_out[0] + x1_5[0]) / 2, x1_5[1] - 6, "12")
    text(dwg, x1_5[0] + 8, x1_5[1] + 14, "X1.5", 10)

    # X1.5 -> M1 L
    m1_l = (X_M1, Y_M1 + 20)
    line(dwg, x1_5[0], x1_5[1], x1_5[0], m1_l[1], 1.3)
    line(dwg, x1_5[0], m1_l[1], m1_l[0], m1_l[1], 1.3)
    wire_no(dwg, (x1_5[0] + m1_l[0]) / 2, m1_l[1] - 6, "13")

    # X1.6 -> M1 N
    x1_6 = (X_X1, Y_X1 + 70)
    m1_n = (X_M1, Y_M1 + 50)
    line(dwg, x1_6[0], x1_6[1], x1_6[0], m1_n[1], 1.3)
    line(dwg, x1_6[0], m1_n[1], m1_n[0], m1_n[1], 1.3)
    wire_no(dwg, (x1_6[0] + m1_n[0]) / 2, m1_n[1] - 6, "15")
    text(dwg, x1_6[0] + 8, x1_6[1] + 14, "X1.6", 10)

    # PS1 +24 -> X1.7
    ps1_24 = (X_PS1 + 104, Y_PS1 + 24)
    x1_7 = (X_X1, Y_X1 + 105)
    line(dwg, ps1_24[0], ps1_24[1], X_X1 - 40, ps1_24[1], 1.3)
    line(dwg, X_X1 - 40, ps1_24[1], X_X1 - 40, x1_7[1], 1.3)
    line(dwg, X_X1 - 40, x1_7[1], x1_7[0], x1_7[1], 1.3)
    wire_no(dwg, X_X1 - 62, x1_7[1] - 6, "30")
    text(dwg, x1_7[0] + 8, x1_7[1] + 14, "X1.7", 10)

    # X1.7 -> YV1 24V
    yv1_24 = (X_YV1, Y_YV1 + 24)
    line(dwg, x1_7[0], x1_7[1], yv1_24[0], x1_7[1], 1.3)
    line(dwg, yv1_24[0], x1_7[1], yv1_24[0], yv1_24[1], 1.3)
    wire_no(dwg, (x1_7[0] + yv1_24[0]) / 2, x1_7[1] - 6, "32")

    # PS1 0V -> X1.8
    ps1_0v = (X_PS1 + 104, Y_PS1 + 58)
    x1_8 = (X_X1, Y_X1 + 140)
    line(dwg, ps1_0v[0], ps1_0v[1], X_X1 - 15, ps1_0v[1], 1.3)
    line(dwg, X_X1 - 15, ps1_0v[1], X_X1 - 15, x1_8[1], 1.3)
    line(dwg, X_X1 - 15, x1_8[1], x1_8[0], x1_8[1], 1.3)
    wire_no(dwg, X_X1 - 37, x1_8[1] - 6, "31")
    text(dwg, x1_8[0] + 8, x1_8[1] + 14, "X1.8", 10)

    # X1.8 -> YV1 0V
    yv1_0v = (X_YV1, Y_YV1 + 56)
    line(dwg, x1_8[0], x1_8[1], yv1_0v[0], x1_8[1], 1.3)
    line(dwg, yv1_0v[0], x1_8[1], yv1_0v[0], yv1_0v[1], 1.3)
    wire_no(dwg, (x1_8[0] + yv1_0v[0]) / 2, x1_8[1] - 6, "33")

    # T1 secondaire -> renvois folio 11
    s1 = (X_T1 + 18, Y_T1 + 108)
    s2 = (X_T1 + 70, Y_T1 + 108)

    line(dwg, s1[0], s1[1], s1[0], s1[1] + 82, 1.3)
    wire_no(dwg, s1[0] + 8, s1[1] + 42, "20")
    xref(dwg, s1[0] + 18, s1[1] + 84, "→ 11 T1")

    line(dwg, s2[0], s2[1], s2[0], s2[1] + 112, 1.3)
    wire_no(dwg, s2[0] + 8, s2[1] + 56, "21")
    xref(dwg, s2[0] + 18, s2[1] + 114, "→ 11 T1")

    # KM1 -> renvoi bobine
    kref_y = Y_KM1 + 18
    line(dwg, X_KM1 + 38, kref_y, X_KM1 + 150, kref_y, 1.3)
    wire_no(dwg, X_KM1 + 78, kref_y - 6, "17")
    xref(dwg, X_KM1 + 160, kref_y, "→ 11 KM1")

    # YV1 -> AO folio 11
    aoref_y = Y_YV1 + 24
    line(dwg, X_YV1, aoref_y, X_YV1 + 120, aoref_y, 1.3)
    wire_no(dwg, X_YV1 + 48, aoref_y - 6, "34")
    xref(dwg, X_YV1 + 130, aoref_y, "→ 11 YV1 AO")


def render_power_folio_svg() -> str:
    dwg = svgwrite.Drawing(size=("100%", "100%"))
    dwg.viewbox(0, 0, PAGE_W, PAGE_H)

    draw_frame(dwg)
    draw_buses(dwg)

    draw_q1(dwg)
    draw_a1(dwg)
    draw_t1(dwg)
    draw_ps1(dwg)
    draw_dm1(dwg)
    draw_km1(dwg)
    draw_x1(dwg)
    draw_yv1(dwg)
    draw_m1(dwg)

    draw_supply_drops(dwg)
    draw_wires(dwg)

    return dwg.tostring()


def render_power_folio_streamlit():
    st.subheader("Folio 10 - Puissance")
    svg = render_power_folio_svg()

    html = f"""
    <div style="width:100%;overflow:auto;background:white;border:1px solid #bbb;">
        <div style="min-width:1500px;padding:8px;">
            {svg}
        </div>
    </div>
    """
    st.components.v1.html(html, height=980, scrolling=True)
