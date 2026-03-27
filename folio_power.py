# folio_power.py
import streamlit as st
import svgwrite

PAGE_W = 1800
PAGE_H = 1200

# Barres d'alimentation
BUS_X1 = 140
BUS_X2 = 1700
Y_L = 120
Y_N = 155
Y_PE = 190

# Colonnes fonctionnelles
X_Q1 = 320
X_T1 = 560
X_PS1 = 860
X_DM1 = 1220
X_KM1 = 1220
X_X1 = 1460
X_YV1 = 1600
X_M1 = 1460

Y_Q1 = 210
Y_T1 = 350
Y_PS1 = 350
Y_DM1 = 230
Y_KM1 = 520
Y_X1 = 620
Y_YV1 = 420
Y_M1 = 820


def line(dwg, x1, y1, x2, y2, w=2):
    dwg.add(dwg.line((x1, y1), (x2, y2), stroke="black", stroke_width=w))


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


def junction(dwg, x, y, r=4):
    dwg.add(dwg.circle(center=(x, y), r=r, fill="black"))


def wire_label(dwg, x, y, value):
    text(dwg, x, y, value, size=12, weight="bold")


def terminal_label(dwg, x, y, value):
    text(dwg, x, y, value, size=11)


def cross_ref(dwg, x, y, value):
    dwg.add(dwg.rect((x, y - 16), (120, 24), fill="white", stroke="black", stroke_width=1))
    text(dwg, x + 6, y + 1, value, size=11)


def draw_frame(dwg):
    dwg.add(dwg.rect((10, 10), (PAGE_W - 20, PAGE_H - 20), fill="white", stroke="black", stroke_width=1.5))
    dwg.add(dwg.rect((20, 20), (PAGE_W - 40, PAGE_H - 140), fill="none", stroke="black", stroke_width=1))

    # grille haute 1..20
    top_x = 20
    usable_w = PAGE_W - 40
    cell_w = usable_w / 20
    for i in range(21):
        x = top_x + i * cell_w
        line(dwg, x, 20, x, 40, 1)
        if i < 20:
            text(dwg, x + cell_w / 2, 35, str(i + 1), size=11, anchor="middle")

    text(dwg, 70, 85, "PUISSANCE", size=28, weight="bold")

    # cartouche
    cart_x = 1180
    cart_y = 1080
    dwg.add(dwg.rect((cart_x, cart_y), (580, 70), fill="none", stroke="black", stroke_width=1))
    line(dwg, cart_x + 430, cart_y, cart_x + 430, cart_y + 70, 1)
    text(dwg, cart_x + 20, cart_y + 28, "CUISINE CENTRALE", size=16)
    text(dwg, cart_x + 20, cart_y + 54, "PUISSANCE", size=16, weight="bold")
    text(dwg, cart_x + 470, cart_y + 28, "FOLIO", size=12)
    text(dwg, cart_x + 495, cart_y + 56, "10", size=24, weight="bold")


def draw_buses(dwg):
    line(dwg, BUS_X1, Y_L, BUS_X2, Y_L, 2)
    line(dwg, BUS_X1, Y_N, BUS_X2, Y_N, 2)
    line(dwg, BUS_X1, Y_PE, BUS_X2, Y_PE, 2)

    text(dwg, 95, Y_L + 5, "L", size=18, weight="bold")
    text(dwg, 95, Y_N + 5, "N", size=18, weight="bold")
    text(dwg, 85, Y_PE + 5, "PE", size=18, weight="bold")


def draw_breaker_q1(dwg, x, y):
    text(dwg, x + 30, y - 28, "Q1", size=16, weight="bold", anchor="middle")
    text(dwg, x + 30, y - 10, "Disjoncteur général", size=12, anchor="middle")

    cx = x + 30
    line(dwg, cx, y, cx, y + 18, 2)
    line(dwg, cx, y + 18, cx + 18, y + 42, 2)
    line(dwg, cx + 18, y + 42, cx, y + 42, 2)
    line(dwg, cx, y + 42, cx, y + 92, 2)

    wire_label(dwg, cx + 8, y + 58, "Q")


def draw_transformer_t1(dwg, x, y):
    text(dwg, x + 40, y - 28, "T1", size=16, weight="bold", anchor="middle")
    text(dwg, x + 40, y - 10, "Transformateur 230/24V", size=12, anchor="middle")

    # primaire
    line(dwg, x + 18, y, x + 18, y + 22, 2)
    line(dwg, x + 62, y, x + 62, y + 22, 2)

    dwg.add(dwg.circle(center=(x + 30, y + 55), r=18, fill="none", stroke="black", stroke_width=1.5))
    dwg.add(dwg.circle(center=(x + 50, y + 55), r=18, fill="none", stroke="black", stroke_width=1.5))

    # secondaire
    line(dwg, x + 18, y + 88, x + 18, y + 120, 2)
    line(dwg, x + 62, y + 88, x + 62, y + 120, 2)

    text(dwg, x + 12, y - 2, "P1", size=10)
    text(dwg, x + 56, y - 2, "P2", size=10)
    text(dwg, x + 10, y + 116, "S1", size=10)
    text(dwg, x + 54, y + 116, "S2", size=10)


def draw_ps1(dwg, x, y):
    text(dwg, x + 50, y - 28, "PS1", size=16, weight="bold", anchor="middle")
    text(dwg, x + 50, y - 10, "Alimentation vanne 24V", size=12, anchor="middle")
    dwg.add(dwg.rect((x, y), (100, 80), fill="none", stroke="black", stroke_width=1.5))
    text(dwg, x + 50, y + 50, "PS", size=26, weight="bold", anchor="middle")


def draw_dm1(dwg, x, y):
    text(dwg, x + 35, y - 28, "DM1", size=16, weight="bold", anchor="middle")
    text(dwg, x + 35, y - 10, "Protection moteur circulateur", size=12, anchor="middle")

    dwg.add(dwg.rect((x + 10, y + 10), (50, 80), fill="none", stroke="black", stroke_width=1.5))
    line(dwg, x + 35, y, x + 35, y + 10, 2)
    line(dwg, x + 35, y + 90, x + 35, y + 120, 2)
    text(dwg, x + 35, y + 58, "DM", size=20, weight="bold", anchor="middle")


def draw_km1_power(dwg, x, y):
    text(dwg, x + 35, y - 28, "KM1", size=16, weight="bold", anchor="middle")
    text(dwg, x + 35, y - 10, "Contact puissance circulateur", size=12, anchor="middle")

    line(dwg, x + 35, y, x + 35, y + 22, 2)
    line(dwg, x + 20, y + 28, x + 20, y + 76, 1.5)
    line(dwg, x + 50, y + 28, x + 50, y + 76, 1.5)
    line(dwg, x + 20, y + 52, x + 50, y + 52, 2)
    line(dwg, x + 35, y + 76, x + 35, y + 110, 2)


def draw_x1(dwg, x, y):
    text(dwg, x + 35, y - 28, "X1", size=16, weight="bold", anchor="middle")
    text(dwg, x + 35, y - 10, "Bornier terrain", size=12, anchor="middle")

    dwg.add(dwg.rect((x, y), (70, 170), fill="none", stroke="black", stroke_width=1.5))

    rows = [("5", 30), ("6", 65), ("7", 100), ("8", 135)]
    for label, dy in rows:
        yy = y + dy
        line(dwg, x, yy, x + 70, yy, 1)
        text(dwg, x + 10, yy - 8, label, size=11)


def draw_yv1(dwg, x, y):
    text(dwg, x + 40, y - 28, "YV1", size=16, weight="bold", anchor="middle")
    text(dwg, x + 40, y - 10, "Vanne 3 voies modulante", size=12, anchor="middle")
    dwg.add(dwg.rect((x, y), (80, 70), fill="none", stroke="black", stroke_width=1.5))
    text(dwg, x + 40, y + 43, "YV", size=22, weight="bold", anchor="middle")


def draw_m1(dwg, x, y):
    text(dwg, x + 50, y - 30, "M1", size=16, weight="bold", anchor="middle")
    text(dwg, x + 50, y - 12, "Circulateur", size=12, anchor="middle")

    # bornes L/N à gauche
    line(dwg, x, y + 20, x + 20, y + 20, 1.5)
    line(dwg, x, y + 50, x + 20, y + 50, 1.5)

    dwg.add(dwg.circle(center=(x + 55, y + 42), r=28, fill="none", stroke="black", stroke_width=1.5))
    text(dwg, x + 55, y + 49, "M", size=22, weight="bold", anchor="middle")

    # terre
    gx = x + 55
    gy = y + 100
    line(dwg, gx, gy - 10, gx, gy, 1.2)
    line(dwg, gx - 12, gy, gx + 12, gy, 1.2)
    line(dwg, gx - 8, gy + 5, gx + 8, gy + 5, 1.2)
    line(dwg, gx - 4, gy + 10, gx + 4, gy + 10, 1.2)


def draw_supply_drops(dwg):
    # Q1 depuis L
    line(dwg, X_Q1 + 30, Y_L, X_Q1 + 30, Y_Q1, 1.6)
    junction(dwg, X_Q1 + 30, Y_L)
    wire_label(dwg, X_Q1 + 38, Y_L - 6, "0")

    # N vers T1, PS1, X1.6
    for x, y in [
        (X_T1 + 62, Y_T1),
        (X_PS1, Y_PS1 + 60),
        (X_X1, Y_X1 + 65),
    ]:
        line(dwg, x, Y_N, x, y, 1.4)
        junction(dwg, x, Y_N)

    # PE vers M1
    line(dwg, X_M1 + 55, Y_PE, X_M1 + 55, Y_M1 + 100, 1.4)
    junction(dwg, X_M1 + 55, Y_PE)
    wire_label(dwg, X_M1 + 62, Y_PE - 6, "16")


def draw_power_paths(dwg):
    # Q1 sortie -> A1 L
    q1_out = (X_Q1 + 30, Y_Q1 + 92)
    a1_l = (X_PS1 - 260, Y_PS1 + 25)  # zone A1 simulée
    # A1 bloc
    text(dwg, X_PS1 - 210, Y_PS1 - 28, "A1", size=16, weight="bold", anchor="middle")
    text(dwg, X_PS1 - 210, Y_PS1 - 10, "Régulateur MXPRO", size=12, anchor="middle")
    dwg.add(dwg.rect((X_PS1 - 260, Y_PS1), (100, 80), fill="none", stroke="black", stroke_width=1.5))
    text(dwg, X_PS1 - 210, Y_PS1 + 50, "MXPRO", size=20, weight="bold", anchor="middle")

    line(dwg, q1_out[0], q1_out[1], q1_out[0], a1_l[1], 1.4)
    line(dwg, q1_out[0], a1_l[1], a1_l[0], a1_l[1], 1.4)
    wire_label(dwg, (q1_out[0] + a1_l[0]) / 2, a1_l[1] - 6, "1")

    # N -> A1 N
    a1_n_x = X_PS1 - 260
    a1_n_y = Y_PS1 + 60
    line(dwg, a1_n_x, Y_N, a1_n_x, a1_n_y, 1.4)
    junction(dwg, a1_n_x, Y_N)
    wire_label(dwg, a1_n_x + 8, (Y_N + a1_n_y) / 2, "2")

    # Q1 -> T1 P1
    t1_p1 = (X_T1 + 18, Y_T1)
    line(dwg, q1_out[0], q1_out[1], q1_out[0], t1_p1[1], 1.4)
    line(dwg, q1_out[0], t1_p1[1], t1_p1[0], t1_p1[1], 1.4)
    wire_label(dwg, (q1_out[0] + t1_p1[0]) / 2, t1_p1[1] - 6, "3")

    # N -> T1 P2
    wire_label(dwg, X_T1 + 70, (Y_N + Y_T1) / 2, "4")

    # Q1 -> PS1 L
    ps1_l = (X_PS1, Y_PS1 + 25)
    line(dwg, q1_out[0], q1_out[1], q1_out[0], ps1_l[1], 1.4)
    line(dwg, q1_out[0], ps1_l[1], ps1_l[0], ps1_l[1], 1.4)
    wire_label(dwg, (q1_out[0] + ps1_l[0]) / 2, ps1_l[1] - 6, "5")

    # N -> PS1 N
    wire_label(dwg, X_PS1 + 8, (Y_N + (Y_PS1 + 60)) / 2, "6")

    # Q1 -> DM1
    dm1_in = (X_DM1 + 35, Y_DM1)
    line(dwg, q1_out[0], q1_out[1], q1_out[0], dm1_in[1], 1.4)
    line(dwg, q1_out[0], dm1_in[1], dm1_in[0], dm1_in[1], 1.4)
    wire_label(dwg, (q1_out[0] + dm1_in[0]) / 2, dm1_in[1] - 6, "10")

    # DM1 -> KM1
    dm1_out = (X_DM1 + 35, Y_DM1 + 120)
    km1_in = (X_KM1 + 35, Y_KM1)
    line(dwg, dm1_out[0], dm1_out[1], dm1_out[0], km1_in[1] - 40, 1.4)
    line(dwg, dm1_out[0], km1_in[1] - 40, km1_in[0], km1_in[1] - 40, 1.4)
    line(dwg, km1_in[0], km1_in[1] - 40, km1_in[0], km1_in[1], 1.4)
    wire_label(dwg, km1_in[0] + 8, km1_in[1] - 46, "11")

    # KM1 -> X1.5
    km1_out = (X_KM1 + 35, Y_KM1 + 110)
    x1_5 = (X_X1, Y_X1 + 25)
    line(dwg, km1_out[0], km1_out[1], km1_out[0], x1_5[1], 1.4)
    line(dwg, km1_out[0], x1_5[1], x1_5[0], x1_5[1], 1.4)
    wire_label(dwg, (km1_out[0] + x1_5[0]) / 2, x1_5[1] - 6, "12")
    terminal_label(dwg, x1_5[0] + 8, x1_5[1] + 16, "X1.5")

    # X1.5 -> M1 L
    m1_l = (X_M1, Y_M1 + 20)
    line(dwg, x1_5[0], x1_5[1], x1_5[0], m1_l[1], 1.4)
    line(dwg, x1_5[0], m1_l[1], m1_l[0], m1_l[1], 1.4)
    wire_label(dwg, (x1_5[0] + m1_l[0]) / 2, m1_l[1] - 6, "13")

    # N -> X1.6 -> M1 N
    x1_6 = (X_X1, Y_X1 + 60)
    m1_n = (X_M1, Y_M1 + 50)
    line(dwg, x1_6[0], x1_6[1], m1_n[0], x1_6[1], 1.4)
    line(dwg, m1_n[0], x1_6[1], m1_n[0], m1_n[1], 1.4)
    wire_label(dwg, (x1_6[0] + m1_n[0]) / 2, x1_6[1] - 6, "15")
    terminal_label(dwg, x1_6[0] + 8, x1_6[1] + 16, "X1.6")

    # PS1 +24 -> X1.7 -> YV1
    ps1_24 = (X_PS1 + 100, Y_PS1 + 28)
    x1_7 = (X_X1, Y_X1 + 95)
    yv1_24 = (X_YV1, Y_YV1 + 25)
    line(dwg, ps1_24[0], ps1_24[1], x1_7[0] - 50, ps1_24[1], 1.4)
    line(dwg, x1_7[0] - 50, ps1_24[1], x1_7[0] - 50, x1_7[1], 1.4)
    line(dwg, x1_7[0] - 50, x1_7[1], x1_7[0], x1_7[1], 1.4)
    wire_label(dwg, x1_7[0] - 70, x1_7[1] - 6, "30")
    terminal_label(dwg, x1_7[0] + 8, x1_7[1] + 16, "X1.7")

    line(dwg, x1_7[0], x1_7[1], yv1_24[0], x1_7[1], 1.4)
    line(dwg, yv1_24[0], x1_7[1], yv1_24[0], yv1_24[1], 1.4)
    wire_label(dwg, (x1_7[0] + yv1_24[0]) / 2, x1_7[1] - 6, "32")

    # PS1 0V -> X1.8 -> YV1
    ps1_0v = (X_PS1 + 100, Y_PS1 + 58)
    x1_8 = (X_X1, Y_X1 + 130)
    yv1_0v = (X_YV1, Y_YV1 + 55)
    line(dwg, ps1_0v[0], ps1_0v[1], x1_8[0] - 20, ps1_0v[1], 1.4)
    line(dwg, x1_8[0] - 20, ps1_0v[1], x1_8[0] - 20, x1_8[1], 1.4)
    line(dwg, x1_8[0] - 20, x1_8[1], x1_8[0], x1_8[1], 1.4)
    wire_label(dwg, x1_8[0] - 40, x1_8[1] - 6, "31")
    terminal_label(dwg, x1_8[0] + 8, x1_8[1] + 16, "X1.8")

    line(dwg, x1_8[0], x1_8[1], yv1_0v[0], x1_8[1], 1.4)
    line(dwg, yv1_0v[0], x1_8[1], yv1_0v[0], yv1_0v[1], 1.4)
    wire_label(dwg, (x1_8[0] + yv1_0v[0]) / 2, x1_8[1] - 6, "33")

    # Renvois folio
    t1_s1 = (X_T1 + 18, Y_T1 + 120)
    t1_s2 = (X_T1 + 62, Y_T1 + 120)
    line(dwg, t1_s1[0], t1_s1[1], t1_s1[0], t1_s1[1] + 80, 1.4)
    wire_label(dwg, t1_s1[0] + 8, t1_s1[1] + 40, "20")
    cross_ref(dwg, t1_s1[0] + 20, t1_s1[1] + 82, "→ 11 T1")

    line(dwg, t1_s2[0], t1_s2[1], t1_s2[0], t1_s2[1] + 110, 1.4)
    wire_label(dwg, t1_s2[0] + 8, t1_s2[1] + 55, "21")
    cross_ref(dwg, t1_s2[0] + 20, t1_s2[1] + 112, "→ 11 T1")

    km1_ref_x = X_KM1 + 35
    km1_ref_y = Y_KM1 + 20
    line(dwg, km1_ref_x, km1_ref_y, km1_ref_x + 120, km1_ref_y, 1.4)
    wire_label(dwg, km1_ref_x + 50, km1_ref_y - 6, "17")
    cross_ref(dwg, km1_ref_x + 130, km1_ref_y, "→ 11 KM1")

    yv1_ao_x = X_YV1
    yv1_ao_y = Y_YV1 + 25
    line(dwg, yv1_ao_x, yv1_ao_y, yv1_ao_x + 120, yv1_ao_y, 1.4)
    wire_label(dwg, yv1_ao_x + 50, yv1_ao_y - 6, "34")
    cross_ref(dwg, yv1_ao_x + 130, yv1_ao_y, "→ 11 YV1 AO")


def render_power_folio_svg() -> str:
    dwg = svgwrite.Drawing(size=("100%", "100%"))
    dwg.viewbox(0, 0, PAGE_W, PAGE_H)

    draw_frame(dwg)
    draw_buses(dwg)

    draw_breaker_q1(dwg, X_Q1, Y_Q1)
    draw_transformer_t1(dwg, X_T1, Y_T1)
    draw_ps1(dwg, X_PS1, Y_PS1)
    draw_dm1(dwg, X_DM1, Y_DM1)
    draw_km1_power(dwg, X_KM1, Y_KM1)
    draw_x1(dwg, X_X1, Y_X1)
    draw_yv1(dwg, X_YV1, Y_YV1)
    draw_m1(dwg, X_M1, Y_M1)

    draw_supply_drops(dwg)
    draw_power_paths(dwg)

    return dwg.tostring()


def render_power_folio_streamlit():
    st.subheader("Folio 10 - Puissance")
    svg = render_power_folio_svg()

    html = f"""
    <div style="width:100%; overflow:auto; background:white; border:1px solid #ccc;">
        <div style="min-width:1400px;">
            {svg}
        </div>
    </div>
    """
    st.components.v1.html(html, height=980, scrolling=True)
