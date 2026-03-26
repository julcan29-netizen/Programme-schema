import re
import html
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Coffret type froid - rendu BE",
    layout="wide"
)

# =========================================================
# PARSER
# =========================================================

def _has_any(text: str, patterns: list[str]) -> bool:
    return any(p in text for p in patterns)


def _extract_first_temp(text: str, patterns: list[str]) -> str | None:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            value = match.group(1).replace(" ", "")
            if not value.startswith(("+", "-")) and value.isdigit():
                value = f"+{value}"
            return f"{value}°C"
    return None


def parse_analysis(text: str) -> dict:
    t = text.lower()

    setpoint = _extract_first_temp(
        text,
        [
            r"point de consigne[^0-9+-]*([+-]?\d+)",
            r"consigne[^0-9+-]*([+-]?\d+)",
        ],
    )

    pump_on = _extract_first_temp(
        text,
        [
            r"marche[^0-9+-]*([+-]?\d+)",
            r"température\s*[>≥=]+\s*([+-]?\d+)",
        ],
    )

    pump_off = _extract_first_temp(
        text,
        [
            r"arr[eê]t[^0-9+-]*([+-]?\d+)",
            r"température\s*[<≤=]+\s*([+-]?\d+)",
        ],
    )

    diff_match = re.search(r"(diff[ée]rentiel)[^0-9]*([0-9]+)\s*k", t)
    differential = f"{diff_match.group(2)}K" if diff_match else "2K"

    return {
        "project_title": "COFFRET TYPE FROID MONO-VENTIL",
        "has_controller": _has_any(t, ["contrôleur", "controleur", "régulateur", "regulateur", "mpx"]),
        "has_temp_sensor": _has_any(t, ["sonde", "température", "temperature"]),
        "has_pump": "pompe" in t,
        "has_fan": _has_any(t, ["ventilation", "ventilateur"]),
        "has_3way_valve": _has_any(t, ["vanne 3 voies", "vanne 3 voies modulante", "vanne 3 voies motorisée"]),
        "has_defrost": _has_any(t, ["dégivrage", "degivrage"]),
        "setpoint": setpoint or "+4°C",
        "pump_on": pump_on or "+12°C",
        "pump_off": pump_off or "+10°C",
        "differential": differential,
        "refs": {
            "ig1": "IG1",
            "q1": "Q1",
            "dm1": "DM1",
            "q2": "Q2",
            "km1": "KM1",
            "km1_aux": "KM1 13-14",
            "t1": "T1",
            "a1": "A1 MPX PRO",
            "dt1": "DT1",
            "x1": "X1",
            "m1": "M1 Pompe",
            "m2": "M2 Ventilation",
            "yv1": "YV1 Vanne 3 voies",
            "tt1": "TT1 Entrée batterie",
            "tt2": "TT2 Reprise",
            "ps1": "PS1",
            "kv1": "KV1",
        },
    }


# =========================================================
# SVG BASE
# =========================================================

def esc(value: str) -> str:
    return html.escape(str(value), quote=True)


def svg_header(width: int, height: int) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {width} {height}" style="background:#fff">',
        "<style>",
        ".title{font:700 22px Arial,sans-serif; fill:#111;}",
        ".sheet{font:700 14px Arial,sans-serif; fill:#111;}",
        ".text{font:13px Arial,sans-serif; fill:#111;}",
        ".small{font:10px Arial,sans-serif; fill:#111;}",
        ".tiny{font:8px Arial,sans-serif; fill:#111;}",
        ".bold{font:700 13px Arial,sans-serif; fill:#111;}",
        ".line{stroke:#111; stroke-width:2; fill:none;}",
        ".rail{stroke:#111; stroke-width:3; fill:none;}",
        ".thin{stroke:#bdbdbd; stroke-width:1; fill:none; stroke-dasharray:4 4;}",
        ".box{stroke:#111; stroke-width:1.6; fill:#fff;}",
        "</style>",
    ]


def svg_footer(parts: list[str]) -> str:
    parts.append("</svg>")
    return "\n".join(parts)


def line(parts: list[str], x1: int, y1: int, x2: int, y2: int, klass: str = "line") -> None:
    parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{klass}"/>')


def rect(parts: list[str], x: int, y: int, w: int, h: int, klass: str = "box") -> None:
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="{klass}"/>')


def circle(parts: list[str], x: int, y: int, r: int, klass: str = "box") -> None:
    parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" class="{klass}"/>')


def text(parts: list[str], x: int, y: int, value: str, klass: str = "text") -> None:
    parts.append(f'<text x="{x}" y="{y}" class="{klass}">{esc(value)}</text>')


def poly(parts: list[str], points: list[tuple[int, int]], klass: str = "box") -> None:
    value = " ".join(f"{x},{y}" for x, y in points)
    parts.append(f'<polygon points="{value}" class="{klass}"/>')


def draw_sheet(parts: list[str], width: int, height: int, project_title: str, sheet_name: str, folio_no: str) -> None:
    top = 55
    left = 40
    right = width - 40
    bottom = height - 95

    rect(parts, left, top, right - left, bottom - top, "box")
    text(parts, 50, 35, project_title, "title")

    col_w = (right - left) / 10
    for i in range(1, 10):
        x = left + i * col_w
        line(parts, int(x), top, int(x), bottom, "thin")
        text(parts, int(x - col_w / 2), top - 10, str(i - 1), "tiny")

    row_h = (bottom - top) / 8
    for i in range(1, 8):
        y = top + i * row_h
        line(parts, left, int(y), right, int(y), "thin")

    for i, letter in enumerate("ABCDEFGH"):
        text(parts, 18, int(top + i * row_h + 16), letter, "tiny")

    cart_y = height - 70
    rect(parts, 20, cart_y, width - 40, 40, "box")
    line(parts, width - 250, cart_y, width - 250, cart_y + 40)
    line(parts, width - 130, cart_y, width - 130, cart_y + 40)
    text(parts, 30, cart_y + 24, sheet_name, "sheet")
    text(parts, width - 235, cart_y + 24, "Folio", "bold")
    text(parts, width - 95, cart_y + 24, folio_no, "bold")


# =========================================================
# SYMBOLES
# =========================================================

def draw_breaker_3p(parts: list[str], x: int, y: int, label: str) -> None:
    for i in range(3):
        xx = x + i * 18
        line(parts, xx, y - 28, xx, y - 8)
        line(parts, xx - 6, y - 8, xx + 6, y + 8)
        line(parts, xx, y + 8, xx, y + 28)
    text(parts, x + 58, y + 4, label, "text")


def draw_switch_3p(parts: list[str], x: int, y: int, label: str) -> None:
    for i in range(3):
        xx = x + i * 18
        line(parts, xx, y - 28, xx, y + 28)
        line(parts, xx - 6, y - 10, xx + 6, y + 10)
    text(parts, x + 58, y + 4, label, "text")


def draw_contactor_3p(parts: list[str], x: int, y: int, label: str) -> None:
    for i in range(3):
        xx = x + i * 18
        line(parts, xx, y - 26, xx, y - 6)
        line(parts, xx - 8, y - 6, xx, y + 8)
        line(parts, xx, y + 8, xx, y + 26)
    text(parts, x + 58, y + 4, label, "text")


def draw_transformer(parts: list[str], x: int, y: int, label: str) -> None:
    circle(parts, x - 10, y, 12)
    circle(parts, x + 10, y, 12)
    text(parts, x + 28, y + 4, label, "text")


def draw_motor(parts: list[str], x: int, y: int, label: str) -> None:
    circle(parts, x, y, 18)
    text(parts, x - 6, y + 5, "M", "text")
    text(parts, x + 26, y + 5, label, "text")


def draw_controller(parts: list[str], x: int, y: int, w: int, h: int, label: str) -> None:
    rect(parts, x, y, w, h, "box")
    text(parts, x + 10, y + 20, label, "bold")


def draw_sensor(parts: list[str], x: int, y: int, label: str) -> None:
    circle(parts, x, y, 7)
    line(parts, x, y + 7, x, y + 22)
    text(parts, x + 14, y + 4, label, "text")


def draw_contact_no(parts: list[str], x: int, y: int, label: str) -> None:
    line(parts, x - 34, y, x - 8, y)
    line(parts, x + 8, y, x + 34, y)
    line(parts, x - 8, y - 12, x + 8, y + 12)
    text(parts, x + 42, y + 4, label, "text")


def draw_contact_nc(parts: list[str], x: int, y: int, label: str) -> None:
    line(parts, x - 34, y, x - 8, y)
    line(parts, x + 8, y, x + 34, y)
    line(parts, x - 8, y - 12, x + 8, y + 12)
    line(parts, x - 8, y + 12, x + 8, y - 12)
    text(parts, x + 42, y + 4, label, "text")


def draw_coil(parts: list[str], x: int, y: int, label: str) -> None:
    line(parts, x, y - 18, x, y - 10)
    rect(parts, x - 16, y - 10, 32, 20, "box")
    line(parts, x, y + 10, x, y + 18)
    text(parts, x + 22, y + 4, label, "text")
    text(parts, x + 2, y - 14, "A1", "tiny")
    text(parts, x + 2, y + 22, "A2", "tiny")


def draw_terminal(parts: list[str], x: int, y: int, label: str) -> None:
    line(parts, x, y - 10, x, y + 10)
    circle(parts, x, y, 4)
    text(parts, x + 10, y + 4, label, "text")


# =========================================================
# FOLIOS
# =========================================================

def build_power_svg(data: dict) -> str:
    width, height = 1500, 900
    parts = svg_header(width, height)
    draw_sheet(parts, width, height, data["project_title"], "Folio puissance", "10")

    r = data["refs"]

    x0 = 90
    for idx, xx in enumerate([x0, x0 + 40, x0 + 80], start=1):
        line(parts, xx, 95, xx, 720, "rail")
        text(parts, xx - 8, 82, f"L{idx}", "tiny")

    draw_switch_3p(parts, x0, 145, r["ig1"])
    draw_breaker_3p(parts, x0, 225, r["q1"])
    draw_breaker_3p(parts, x0, 310, r["dm1"])
    draw_breaker_3p(parts, x0, 400, r["q2"])
    draw_contactor_3p(parts, x0, 505, r["km1"])
    draw_motor(parts, x0, 625, r["m1"])

    for xx in [x0, x0 + 18, x0 + 36]:
        line(parts, xx, 173, xx, 197)
        line(parts, xx, 253, xx, 282)
        line(parts, xx, 338, xx, 372)
        line(parts, xx, 428, xx, 479)
        line(parts, xx, 531, xx, 607)

    if data["has_fan"]:
        xf = 380
        line(parts, xf, 95, xf, 720, "rail")
        line(parts, xf + 40, 95, xf + 40, 720, "rail")
        text(parts, xf - 6, 82, "L", "tiny")
        text(parts, xf + 32, 82, "N", "tiny")
        draw_breaker_3p(parts, xf, 225, "QF Vent")
        draw_motor(parts, xf, 625, r["m2"])
        line(parts, xf, 253, xf, 607)
        line(parts, xf + 18, 253, xf + 18, 607)

    draw_transformer(parts, 720, 230, r["t1"])
    line(parts, 690, 180, 690, 218)
    line(parts, 750, 180, 750, 218)
    text(parts, 672, 165, "230V/24V", "tiny")

    if data["has_3way_valve"]:
        rect(parts, 1040, 215, 40, 34, "box")
        text(parts, 1048, 237, "PS", "text")
        text(parts, 1095, 237, r["ps1"], "text")

        rect(parts, 1044, 395, 32, 32, "box")
        line(parts, 1060, 427, 1060, 455)
        poly(parts, [(1048, 455), (1072, 455), (1060, 470)], "box")
        text(parts, 1090, 413, r["yv1"], "text")
        line(parts, 1060, 249, 1060, 395)

    return svg_footer(parts)


def build_command_svg(data: dict) -> str:
    width, height = 1600, 900
    parts = svg_header(width, height)
    draw_sheet(parts, width, height, data["project_title"], "Folio commande", "11")

    r = data["refs"]

    xL = 100
    xN = 1500
    line(parts, xL, 90, xL, 790, "rail")
    line(parts, xN, 90, xN, 790, "rail")
    text(parts, xL - 14, 80, "L", "bold")
    text(parts, xN - 10, 80, "N", "bold")

    # Rang 1 pompe avec auto-maintien
    y1 = 180
    line(parts, xL, y1, 220, y1)

    if data["has_defrost"]:
        draw_contact_nc(parts, 270, y1, "DEG")
        line(parts, 304, y1, 360, y1)
    else:
        line(parts, 220, y1, 360, y1)

    draw_contact_no(parts, 420, y1, "REG")
    line(parts, 454, y1, 1180, y1)

    draw_coil(parts, 1320, y1, r["km1"])
    line(parts, 1180, y1, 1304, y1)
    line(parts, 1336, y1, xN, y1)

    # Pont auto-maintien
    line(parts, 360, y1 - 42, 360, y1)
    line(parts, 1180, y1 - 42, 1180, y1)
    line(parts, 360, y1 - 42, 520, y1 - 42)
    draw_contact_no(parts, 570, y1 - 42, r["km1_aux"])
    line(parts, 604, y1 - 42, 1180, y1 - 42)

    # Rang 2 ventilation
    if data["has_fan"]:
        y2 = 285
        line(parts, xL, y2, 1200, y2)
        draw_coil(parts, 1320, y2, r["kv1"])
        line(parts, 1200, y2, 1304, y2)
        line(parts, 1336, y2, xN, y2)
        text(parts, 300, y2 - 10, "Ventilation permanente", "tiny")

    # Bloc régulateur centré
    rx, ry, rw, rh = 640, 430, 210, 120
    draw_controller(parts, rx, ry, rw, rh, r["a1"])

    if data["has_temp_sensor"]:
        draw_sensor(parts, 470, 455, r["tt1"])
        draw_sensor(parts, 470, 520, r["tt2"])
        line(parts, 490, 455, rx, 455)
        line(parts, 490, 520, rx, 520)

    # Sorties du régulateur
    text(parts, rx + 15, ry + 52, "Entrées sondes", "small")
    text(parts, rx + 15, ry + 72, "Sorties relais / AO", "small")

    if data["has_3way_valve"]:
        draw_terminal(parts, 980, 470, "AO+")
        draw_terminal(parts, 1060, 470, "AO-")
        line(parts, rx + rw, 470, 980, 470)
        line(parts, rx + rw, 500, 1060, 500)
        text(parts, 1110, 474, "0-10V vers YV1", "text")

    # Légende BE
    text(parts, 640, 655, f'Consigne : {data["setpoint"]}', "text")
    text(parts, 640, 677, f'Marche pompe : {data["pump_on"]}', "text")
    text(parts, 640, 699, f'Arrêt pompe : {data["pump_off"]}', "text")
    text(parts, 640, 721, f'Différentiel : {data["differential"]}', "text")

    return svg_footer(parts)


def build_terminal_svg(data: dict) -> str:
    width, height = 1450, 900
    parts = svg_header(width, height)
    draw_sheet(parts, width, height, data["project_title"], "Folio bornier", "12")

    r = data["refs"]
    text(parts, 90, 130, f'Bornier {r["x1"]}', "bold")

    x = 90
    y = 165

    rect(parts, x, y, 1180, 34, "box")
    line(parts, x + 140, y, x + 140, y + 34)
    line(parts, x + 620, y, x + 620, y + 34)
    text(parts, x + 20, y + 22, "Repère", "bold")
    text(parts, x + 170, y + 22, "Fonction", "bold")
    text(parts, x + 670, y + 22, "Extérieur", "bold")

    rows = [
        ("1", "Sonde TT1 entrée batterie", "Champ"),
        ("2", "Sonde TT2 reprise", "Champ"),
        ("3", "Sortie 0-10V AO+", "Actionneur YV1"),
        ("4", "Sortie 0-10V AO-", "Actionneur YV1"),
        ("5", "Commande pompe", "KM1"),
        ("6", "Retour neutre", "N"),
        ("7", "Commande ventilation", "KV1"),
        ("8", "Info dégivrage", "Entrée REG"),
    ]

    for i, row in enumerate(rows):
        yy = y + 44 + i * 36
        rect(parts, x, yy, 1180, 28, "box")
        line(parts, x + 140, yy, x + 140, yy + 28)
        line(parts, x + 620, yy, x + 620, yy + 28)
        text(parts, x + 25, yy + 18, row[0], "text")
        text(parts, x + 170, yy + 18, row[1], "text")
        text(parts, x + 670, yy + 18, row[2], "text")

    return svg_footer(parts)


def build_bom_svg(data: dict) -> str:
    width, height = 1450, 900
    parts = svg_header(width, height)
    draw_sheet(parts, width, height, data["project_title"], "Nomenclature simplifiée", "13")

    items = [
        ("IG1", "Interrupteur général", "1"),
        ("Q1", "Protection générale", "1"),
        ("DM1", "Protection moteur pompe", "1"),
        ("Q2", "Protection départ pompe", "1"),
        ("KM1", "Contacteur pompe", "1"),
        ("KV1", "Relais ventilation", "1"),
        ("T1", "Transformateur alimentation commande", "1"),
        ("A1", "Régulateur MPX PRO", "1"),
        ("DT1", "Module interface régulation", "1"),
        ("X1", "Bornier extérieur", "1"),
        ("YV1", "Actionneur vanne 3 voies 0-10V", "1"),
        ("TT1", "Sonde entrée batterie", "1"),
        ("TT2", "Sonde reprise", "1"),
    ]

    x = 90
    y = 150
    rect(parts, x, y, 1180, 34, "box")
    line(parts, x + 180, y, x + 180, y + 34)
    line(parts, x + 930, y, x + 930, y + 34)
    text(parts, x + 20, y + 22, "Repère", "bold")
    text(parts, x + 210, y + 22, "Désignation", "bold")
    text(parts, x + 980, y + 22, "Qté", "bold")

    for i, item in enumerate(items):
        yy = y + 42 + i * 31
        rect(parts, x, yy, 1180, 25, "box")
        line(parts, x + 180, yy, x + 180, yy + 25)
        line(parts, x + 930, yy, x + 930, yy + 25)
        text(parts, x + 20, yy + 17, item[0], "text")
        text(parts, x + 210, yy + 17, item[1], "text")
        text(parts, x + 990, yy + 17, item[2], "text")

    return svg_footer(parts)


# =========================================================
# UI
# =========================================================

def render_svg(svg_code: str, height: int) -> None:
    components.html(svg_code, height=height, scrolling=True)


def build_summary_text(data: dict) -> str:
    lines = []
    if data["has_controller"]:
        lines.append("Contrôleur local détecté")
    if data["has_temp_sensor"]:
        lines.append("Sondes de température détectées")
    if data["has_pump"]:
        lines.append("Pompe détectée")
    if data["has_3way_valve"]:
        lines.append("Vanne 3 voies modulante détectée")
    if data["has_fan"]:
        lines.append("Ventilation détectée")
    if data["has_defrost"]:
        lines.append("Mode dégivrage détecté")
    lines.append(f'Consigne : {data["setpoint"]}')
    lines.append(f'Marche pompe : {data["pump_on"]}')
    lines.append(f'Arrêt pompe : {data["pump_off"]}')
    lines.append(f'Différentiel : {data["differential"]}')
    return "\n".join(lines)


st.title("Générateur de dossier électrique - coffret type froid")
st.caption("Rendu bureau d’étude figé sur un coffret type.")

default_text = """Un contrôleur de boucle, associé à une sonde de température du retour ou de la reprise, permet de moduler l’ouverture d’une vanne 3 voies motorisée en fonction de la température mesurée à l’entrée frigorifère.
La pompe de circulation, à débit fixe, alimente le circuit en eau glycolée froide.
La vanne 3 voies modulante, installée sur le retour du circuit frigorifique, ajuste le mélange entre le retour du fluide et la boucle de dérivation selon le besoin en froid.
La pompe est commandée par la sonde de reprise :
• Marche : température ≥ 12 °C
• Arrêt : température ≤ 10 °C
• Différentiel : 2 K
Ventilation permanente.
Mode dégivrage naturel :
• La pompe de circulation est arrêtée.
• La vanne 3 voies est placée en by-pass 100 %.
• La ventilation continue de fonctionner.
Point de consigne vanne modulante : +4 °C."""

analysis_text = st.text_area("Décris ton installation", value=default_text, height=320)

if st.button("Générer le schéma électrique"):
    data = parse_analysis(analysis_text)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Résumé", "Puissance", "Commande", "Bornier", "Nomenclature"]
    )

    with tab1:
        st.subheader("Éléments détectés")
        st.text(build_summary_text(data))
        st.json(data)

    with tab2:
        st.subheader("Folio puissance")
        render_svg(build_power_svg(data), 840)

    with tab3:
        st.subheader("Folio commande")
        render_svg(build_command_svg(data), 840)

    with tab4:
        st.subheader("Folio bornier")
        render_svg(build_terminal_svg(data), 760)

    with tab5:
        st.subheader("Nomenclature simplifiée")
        render_svg(build_bom_svg(data), 760)
