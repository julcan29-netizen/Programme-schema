import re
import html
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Generateur schema electrique V7", layout="wide")


# =========================
# ANALYSE TEXTE
# =========================

def has_any(text: str, patterns: list[str]) -> bool:
    return any(p in text for p in patterns)


def extract_setpoint(text: str) -> str | None:
    patterns = [
        r"consigne[^0-9+-]*([+-]?\d+)\s*°?\s*c",
        r"point de consigne[^0-9+-]*([+-]?\d+)\s*°?\s*c",
        r"\+([0-9]+)\s*°?\s*c",
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            return f"+{m.group(1)}°C" if not m.group(1).startswith("-") else f"{m.group(1)}°C"
    return None


def extract_threshold(text: str, keyword: str) -> str | None:
    patterns = [
        rf"{keyword}[^0-9+-]*([+-]?\d+)\s*°?\s*c",
        rf"{keyword}\s*:\s*température\s*[<>]=?\s*([+-]?\d+)\s*°?\s*c",
        rf"{keyword}\s*:\s*t[^0-9+-]*([+-]?\d+)\s*°?\s*c",
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            return f"{m.group(1)}°C"
    return None


def parse_analysis(text: str) -> dict:
    t = text.lower()

    data = {
        "has_controller": has_any(t, ["contrôleur", "controleur", "régulateur", "regulateur"]),
        "has_temp_sensor": has_any(t, ["sonde", "température", "temperature"]),
        "has_pump": "pompe" in t,
        "has_3way_valve": has_any(t, ["vanne 3 voies", "vanne 3 voies modulante", "vanne 3 voies motorisée"]),
        "has_fan": has_any(t, ["ventilation", "ventilateur"]),
        "has_defrost": has_any(t, ["dégivrage", "degivrage"]),
        "has_bypass": has_any(t, ["by-pass", "bypass"]),
        "has_glycol": has_any(t, ["glycol", "glycolée", "glycolee"]),
    }

    data["setpoint"] = extract_setpoint(t)
    data["pump_on"] = extract_threshold(t, "marche")
    data["pump_off"] = extract_threshold(t, "arrêt") or extract_threshold(t, "arret")

    m = re.search(r"(différentiel|differentiel)[^0-9]*([0-9]+)\s*k", t)
    data["differential"] = f"{m.group(2)}K" if m else None

    return data


# =========================
# SVG OUTILS
# =========================

def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def svg_header(width: int, height: int) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {width} {height}" style="background:#fff">',
        "<style>",
        ".t{font:14px Arial,sans-serif; fill:#111;}",
        ".ts{font:12px Arial,sans-serif; fill:#111;}",
        ".tb{font:700 20px Arial,sans-serif; fill:#111;}",
        ".line{stroke:#111; stroke-width:2; fill:none;}",
        ".thin{stroke:#999; stroke-width:1; fill:none; stroke-dasharray:4 4;}",
        ".box{stroke:#111; stroke-width:2; fill:#fff;}",
        ".rail{stroke:#111; stroke-width:3; fill:none;}",
        "</style>",
    ]


def svg_footer(parts: list[str]) -> str:
    parts.append("</svg>")
    return "\n".join(parts)


def line(parts: list[str], x1: int, y1: int, x2: int, y2: int, klass: str = "line") -> None:
    parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{klass}"/>')


def text(parts: list[str], x: int, y: int, value: str, klass: str = "t") -> None:
    parts.append(f'<text x="{x}" y="{y}" class="{klass}">{esc(value)}</text>')


def rect(parts: list[str], x: int, y: int, w: int, h: int, klass: str = "box") -> None:
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="{klass}"/>')


def circle(parts: list[str], x: int, y: int, r: int, klass: str = "box") -> None:
    parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" class="{klass}"/>')


def draw_page(parts: list[str], width: int, height: int, title: str) -> None:
    top = 50
    bottom = height - 80
    left = 40
    right = width - 40

    rect(parts, left, top, right - left, bottom - top, "box")
    text(parts, 50, 35, title, "tb")

    col_w = (right - left) / 10
    for i in range(1, 10):
        x = left + i * col_w
        line(parts, int(x), top, int(x), bottom, "thin")
        text(parts, int(x - col_w / 2), top - 10, str(i - 1), "ts")

    row_h = (bottom - top) / 8
    for i in range(1, 8):
        y = top + i * row_h
        line(parts, left, int(y), right, int(y), "thin")

    for i, letter in enumerate("ABCDEFGH"):
        text(parts, 20, int(top + i * row_h + 18), letter, "ts")

    # cartouche
    rect(parts, 20, height - 55, width - 40, 35, "box")
    text(parts, 30, height - 32, title.replace("Folio ", ""), "t")


# =========================
# SYMBOLES ELECTRIQUES
# =========================

def draw_motor(parts: list[str], x: int, y: int, label: str) -> None:
    circle(parts, x, y, 18)
    text(parts, x - 6, y + 5, "M", "t")
    text(parts, x + 28, y + 5, label, "t")


def draw_breaker_3p(parts: list[str], x: int, y: int, label: str) -> None:
    for i in range(3):
        xx = x + i * 18
        line(parts, xx, y - 30, xx, y - 8)
        line(parts, xx - 6, y - 8, xx + 6, y + 8)
        line(parts, xx, y + 8, xx, y + 30)
    text(parts, x + 70, y + 5, label, "t")


def draw_contactor_3p(parts: list[str], x: int, y: int, label: str) -> None:
    for i in range(3):
        xx = x + i * 18
        line(parts, xx, y - 28, xx, y - 6)
        line(parts, xx - 7, y - 6, xx, y + 8)
        line(parts, xx, y + 8, xx, y + 28)
    text(parts, x + 70, y + 5, label, "t")


def draw_power_supply(parts: list[str], x: int, y: int, label: str) -> None:
    rect(parts, x - 18, y - 18, 36, 36)
    text(parts, x - 12, y + 5, "PS", "t")
    text(parts, x + 28, y + 5, label, "t")


def draw_valve_actuator(parts: list[str], x: int, y: int, label: str) -> None:
    rect(parts, x - 16, y - 16, 32, 32)
    line(parts, x, y + 16, x, y + 38)
    parts.append(f'<polygon points="{x-12},{y+38} {x+12},{y+38} {x},{y+52}" class="box"/>')
    text(parts, x + 26, y + 5, label, "t")


def draw_controller(parts: list[str], x: int, y: int, label: str) -> None:
    rect(parts, x - 35, y - 20, 70, 40)
    text(parts, x - 16, y + 5, "REG", "t")
    text(parts, x + 45, y + 5, label, "t")


def draw_sensor(parts: list[str], x: int, y: int, label: str) -> None:
    circle(parts, x, y, 8)
    line(parts, x, y + 8, x, y + 26)
    text(parts, x + 14, y + 5, label, "t")


def draw_coil(parts: list[str], x: int, y: int, label: str) -> None:
    line(parts, x, y - 20, x, y - 10)
    rect(parts, x - 15, y - 10, 30, 20)
    line(parts, x, y + 10, x, y + 20)
    text(parts, x + 24, y + 5, label, "t")
    text(parts, x + 2, y - 14, "A1", "ts")
    text(parts, x + 2, y + 22, "A2", "ts")


def draw_contact_no(parts: list[str], x: int, y: int, label: str) -> None:
    line(parts, x - 32, y, x - 8, y)
    line(parts, x + 8, y, x + 32, y)
    line(parts, x - 8, y - 12, x + 8, y + 12)
    text(parts, x + 40, y + 5, label, "t")


def draw_contact_nc(parts: list[str], x: int, y: int, label: str) -> None:
    line(parts, x - 32, y, x - 8, y)
    line(parts, x + 8, y, x + 32, y)
    line(parts, x - 8, y - 12, x + 8, y + 12)
    line(parts, x - 8, y + 12, x + 8, y - 12)
    text(parts, x + 40, y + 5, label, "t")


def draw_terminal(parts: list[str], x: int, y: int, label: str) -> None:
    line(parts, x, y - 12, x, y + 12)
    circle(parts, x, y, 4)
    text(parts, x + 10, y + 5, label, "t")


def render_svg(svg_code: str, height: int) -> None:
    components.html(svg_code, height=height, scrolling=True)


# =========================
# FOLIO PUISSANCE
# =========================

def build_power_svg(data: dict) -> str:
    width, height = 1400, 900
    parts = svg_header(width, height)
    draw_page(parts, width, height, "Folio puissance")

    # colonnes pompes
    x1, x2, x3 = 90, 150, 210
    for xx, name in [(x1, "L1"), (x2, "L2"), (x3, "L3")]:
        line(parts, xx, 90, xx, 700, "rail")
        text(parts, xx - 10, 80, name, "ts")

    if data["has_pump"]:
        draw_breaker_3p(parts, 90, 170, "QF1")
        draw_contactor_3p(parts, 90, 300, "KM1")
        draw_motor(parts, 90, 490, "M1 Pompe")

        for xx in [90, 108, 126]:
            line(parts, xx, 200, xx, 272)
            line(parts, xx, 328, xx, 470)

    if data["has_fan"]:
        xf = 420
        for i, name in enumerate(["L1", "L2", "L3"]):
            xx = xf + i * 60
            line(parts, xx, 90, xx, 700, "rail")
            if i == 0:
                text(parts, xx - 10, 80, "L1", "ts")
        draw_breaker_3p(parts, xf, 170, "QF2")
        draw_motor(parts, xf, 490, "M2 Ventilation")
        for xx in [xf, xf + 18, xf + 36]:
            line(parts, xx, 200, xx, 470)

    if data["has_3way_valve"]:
        draw_power_supply(parts, 900, 240, "PS1")
        draw_valve_actuator(parts, 900, 420, "YV1 Vanne 3 voies")
        line(parts, 900, 258, 900, 404)

    text(parts, 1020, 470, "Actionneur vanne", "ts")
    return svg_footer(parts)


# =========================
# FOLIO COMMANDE
# =========================

def build_control_svg(data: dict) -> str:
    width, height = 1600, 900
    parts = svg_header(width, height)
    draw_page(parts, width, height, "Folio commande")

    xL = 100
    xN = 1500

    line(parts, xL, 90, xL, 780, "rail")
    line(parts, xN, 90, xN, 780, "rail")
    text(parts, xL - 14, 78, "L", "t")
    text(parts, xN - 10, 78, "N", "t")

    # RANG 1 : POMPE
    y1 = 190
    if data["has_pump"]:
        line(parts, xL, y1, 210, y1)
        if data["has_defrost"]:
            draw_contact_nc(parts, 290, y1, "DEG NF")
            line(parts, 322, y1, 390, y1)
        else:
            line(parts, 210, y1, 390, y1)

        draw_contact_no(parts, 470, y1, "REG demande pompe")
        line(parts, 502, y1, 1180, y1)
        draw_coil(parts, 1250, y1, "KM1")
        line(parts, 1250, y1 + 20, 1250, y1 + 50)
        line(parts, 1250, y1 + 50, xN, y1 + 50)
        line(parts, xN, y1 + 50, xN, y1)

    # RANG 2 : VENTILATION PERMANENTE
    y2 = 320
    if data["has_fan"]:
        line(parts, xL, y2, 1180, y2)
        draw_coil(parts, 1250, y2, "KV1")
        line(parts, 1250, y2 + 20, 1250, y2 + 50)
        line(parts, 1250, y2 + 50, xN, y2 + 50)
        line(parts, xN, y2 + 50, xN, y2)
        text(parts, 300, y2 - 12, "Ventilation permanente", "ts")

    # RANG 3 : INFORMATIONS REGULATION
    draw_controller(parts, 820, 520, "A1")

    if data["has_temp_sensor"]:
        draw_sensor(parts, 500, 460, "TT1 Entree")
        draw_sensor(parts, 500, 590, "TT2 Reprise")
        # petits chemins orthogonaux
        line(parts, 500, 486, 500, 520)
        line(parts, 500, 520, 785, 520)
        line(parts, 500, 616, 500, 550)
        line(parts, 500, 550, 785, 550)

    if data["has_3way_valve"]:
        draw_terminal(parts, 1180, 500, "AO+")
        draw_terminal(parts, 1230, 500, "AO-")
        line(parts, 855, 505, 1180, 505)
        line(parts, 855, 535, 1230, 535)
        text(parts, 1280, 505, "0-10V vers YV1", "t")

    # Texte technique
    yy = 680
    if data["setpoint"]:
        text(parts, 760, yy, f"Consigne : {data['setpoint']}", "ts")
        yy += 20
    if data["pump_on"]:
        text(parts, 760, yy, f"Marche pompe : {data['pump_on']}", "ts")
        yy += 20
    if data["pump_off"]:
        text(parts, 760, yy, f"Arret pompe : {data['pump_off']}", "ts")
        yy += 20
    if data["differential"]:
        text(parts, 760, yy, f"Differenciel : {data['differential']}", "ts")

    return svg_footer(parts)


# =========================
# RESUME
# =========================

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
    if data["setpoint"]:
        lines.append(f"Consigne détectée : {data['setpoint']}")
    if data["pump_on"]:
        lines.append(f"Seuil marche pompe : {data['pump_on']}")
    if data["pump_off"]:
        lines.append(f"Seuil arrêt pompe : {data['pump_off']}")
    return "\n".join(lines) if lines else "Aucun équipement reconnu."


# =========================
# UI
# =========================

st.title("Générateur de schéma électrique conventionnel V7")
st.caption("Sortie visée : schéma puissance + commande de style industriel simplifié.")

default_text = """Un contrôleur de boucle, associé à une sonde de température du retour ou de la reprise, permet de moduler l’ouverture d’une vanne 3 voies motorisée en fonction de la température mesurée à l’entrée frigorifère.
La pompe de circulation, à débit fixe, alimente le circuit en eau glycolée froide.
La vanne 3 voies modulante, installée sur le retour du circuit frigorifique, ajuste le mélange entre le retour du fluide et la boucle de dérivation selon le besoin en froid.
La pompe est commandée par la sonde de reprise :
• Marche : température ≥ 12 °C
• Arrêt : température ≤ 10 °C
• Différentiel : 2 K
Ventilation permanente, indépendamment du fonctionnement de la pompe et de la vanne.
Mode dégivrage naturel :
• La pompe de circulation est arrêtée.
• La vanne 3 voies est placée en by-pass 100 %.
• La ventilation continue de fonctionner.
Point de consigne vanne modulante : +4 °C."""

analysis_text = st.text_area("Décris ton installation", value=default_text, height=320)

if st.button("Générer le schéma électrique"):
    data = parse_analysis(analysis_text)
    power_svg = build_power_svg(data)
    control_svg = build_control_svg(data)

    tab1, tab2, tab3 = st.tabs(["Résumé", "Puissance", "Commande"])

    with tab1:
        st.subheader("Éléments détectés")
        st.text(build_summary_text(data))
        st.json(data)

    with tab2:
        st.subheader("Schéma puissance")
        render_svg(power_svg, height=820)

    with tab3:
        st.subheader("Schéma commande")
        render_svg(control_svg, height=820)
