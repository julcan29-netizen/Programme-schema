# folio_power.py
import streamlit as st
import svgwrite

PAGE_W = 1600
PAGE_H = 1000

# Barres
Y_L = 120
Y_N = 150
Y_PE = 180

# Colonnes
X_COL = {
    "Q1": 250,
    "T1": 500,
    "A1": 750,
    "PS1": 900,
    "DM1": 1150,
    "KM1": 1150,
    "X1": 1350,
    "YV1": 1450,
    "M1": 1350,
}

# Positions verticales
Y_POS = {
    "Q1": 220,
    "T1": 350,
    "A1": 350,
    "PS1": 350,
    "DM1": 250,
    "KM1": 500,
    "X1": 600,
    "YV1": 450,
    "M1": 780,
}


# ========= OUTILS =========

def line(dwg, x1, y1, x2, y2, w=2):
    dwg.add(dwg.line((x1, y1), (x2, y2), stroke="black", stroke_width=w))


def txt(dwg, x, y, t, s=14, w="normal", a="start"):
    dwg.add(dwg.text(
        t,
        insert=(x, y),
        font_size=f"{s}px",
        font_weight=w,
        text_anchor=a
    ))


def node(dwg, x, y):
    dwg.add(dwg.circle(center=(x, y), r=4, fill="black"))


def wire_label(dwg, x, y, t):
    txt(dwg, x, y, t, 12, "bold")


def cross_ref(dwg, x, y, t):
    dwg.add(dwg.rect((x, y-14), (110, 22), fill="white", stroke="black"))
    txt(dwg, x+5, y+2, t, 11)


# ========= STRUCTURE =========

def draw_frame(dwg):
    dwg.add(dwg.rect((10,10),(PAGE_W-20,PAGE_H-20),
                     fill="white", stroke="black"))

    txt(dwg, 60, 80, "PUISSANCE", 26, "bold")

    # Cartouche
    dwg.add(dwg.rect((1100,900),(450,70),
                     fill="none", stroke="black"))
    txt(dwg, 1120, 940, "INSTALLATION CVC", 14)
    txt(dwg, 1120, 965, "FOLIO 10", 16, "bold")


def draw_buses(dwg):
    line(dwg, 80, Y_L, 1550, Y_L, 2)
    line(dwg, 80, Y_N, 1550, Y_N, 2)
    line(dwg, 80, Y_PE, 1550, Y_PE, 2)

    txt(dwg, 50, Y_L+5, "L", 16, "bold")
    txt(dwg, 50, Y_N+5, "N", 16, "bold")
    txt(dwg, 40, Y_PE+5, "PE", 16, "bold")


# ========= SYMBOLS =========

def draw_q1(dwg):
    x = X_COL["Q1"]; y = Y_POS["Q1"]
    txt(dwg, x+25, y-25, "Q1", 14, "bold", "middle")
    txt(dwg, x+25, y-10, "Disjoncteur", 11, "middle")

    cx = x+25
    line(dwg, cx, y, cx, y+80, 2)


def draw_t1(dwg):
    x = X_COL["T1"]; y = Y_POS["T1"]
    txt(dwg, x+40, y-25, "T1", 14, "bold", "middle")
    txt(dwg, x+40, y-10, "230/24V", 11, "middle")

    dwg.add(dwg.circle((x+30,y+40),15,fill="none",stroke="black"))
    dwg.add(dwg.circle((x+50,y+40),15,fill="none",stroke="black"))


def draw_a1(dwg):
    x = X_COL["A1"]; y = Y_POS["A1"]
    txt(dwg, x+50, y-25, "A1", 14, "bold", "middle")
    txt(dwg, x+50, y-10, "MXPRO", 11, "middle")
    dwg.add(dwg.rect((x,y),(100,70),fill="none",stroke="black"))


def draw_ps1(dwg):
    x = X_COL["PS1"]; y = Y_POS["PS1"]
    txt(dwg, x+50, y-25, "PS1", 14, "bold", "middle")
    dwg.add(dwg.rect((x,y),(100,70),fill="none",stroke="black"))
    txt(dwg, x+50, y+40, "PS", 18, "bold", "middle")


def draw_dm1(dwg):
    x = X_COL["DM1"]; y = Y_POS["DM1"]
    txt(dwg, x+30, y-25, "DM1", 14, "bold", "middle")
    dwg.add(dwg.rect((x,y),(60,80),fill="none",stroke="black"))


def draw_km1(dwg):
    x = X_COL["KM1"]; y = Y_POS["KM1"]
    txt(dwg, x+30, y-25, "KM1", 14, "bold", "middle")
    line(dwg, x+30, y, x+30, y+100, 2)


def draw_x1(dwg):
    x = X_COL["X1"]; y = Y_POS["X1"]
    txt(dwg, x+35, y-25, "X1", 14, "bold", "middle")
    dwg.add(dwg.rect((x,y),(70,150),fill="none",stroke="black"))

    for i,t in enumerate(["5","6","7","8"]):
        yy = y+30+i*30
        line(dwg,x,yy,x+70,yy,1)
        txt(dwg,x+10,yy-5,t,11)


def draw_yv1(dwg):
    x = X_COL["YV1"]; y = Y_POS["YV1"]
    txt(dwg, x+30, y-25, "YV1", 14, "bold", "middle")
    dwg.add(dwg.rect((x,y),(60,60),fill="none",stroke="black"))


def draw_m1(dwg):
    x = X_COL["M1"]; y = Y_POS["M1"]
    txt(dwg, x+40, y-25, "M1", 14, "bold", "middle")

    dwg.add(dwg.circle((x+40,y+40),30,fill="none",stroke="black"))
    txt(dwg, x+40, y+45, "M", 18, "bold", "middle")


# ========= LIAISONS =========

def draw_wires(dwg):

    # Q1 depuis L
    line(dwg, X_COL["Q1"]+25, Y_L, X_COL["Q1"]+25, Y_POS["Q1"])
    node(dwg, X_COL["Q1"]+25, Y_L)

    # Q1 → DM1
    line(dwg, X_COL["Q1"]+25, Y_POS["Q1"]+80,
         X_COL["DM1"]+30, Y_POS["DM1"])

    # DM1 → KM1
    line(dwg, X_COL["DM1"]+30, Y_POS["DM1"]+80,
         X_COL["KM1"]+30, Y_POS["KM1"])

    # KM1 → X1
    line(dwg, X_COL["KM1"]+30, Y_POS["KM1"]+100,
         X_COL["X1"], Y_POS["X1"]+30)

    # X1 → M1
    line(dwg, X_COL["X1"], Y_POS["X1"]+30,
         X_COL["M1"], Y_POS["M1"]+20)

    # PS1 → YV1
    line(dwg, X_COL["PS1"]+100, Y_POS["PS1"]+30,
         X_COL["YV1"], Y_POS["YV1"]+20)


# ========= RENDER =========

def render_svg():
    dwg = svgwrite.Drawing(size=("100%","100%"))
    dwg.viewbox(0,0,PAGE_W,PAGE_H)

    draw_frame(dwg)
    draw_buses(dwg)

    draw_q1(dwg)
    draw_t1(dwg)
    draw_a1(dwg)
    draw_ps1(dwg)
    draw_dm1(dwg)
    draw_km1(dwg)
    draw_x1(dwg)
    draw_yv1(dwg)
    draw_m1(dwg)

    draw_wires(dwg)

    return dwg.tostring()


def render_power_folio_streamlit():
    svg = render_svg()

    html = f"""
    <div style="width:100%;overflow:auto;background:white">
        <div style="min-width:1400px">
            {svg}
        </div>
    </div>
    """

    st.components.v1.html(html, height=900)
