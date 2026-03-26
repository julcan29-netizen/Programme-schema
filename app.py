import re
import html
import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(page_title="Generateur de schema electrique V6.1", layout="wide")


def has_any(text: str, patterns: list[str]) -> bool:
    return any(p in text for p in patterns)


def extract_setpoint(text: str) -> str | None:
    patterns = [
        r"consigne[^0-9+-]*([+-]?\d+)\s*°?\s*c",
        r"point de consigne[^0-9+-]*([+-]?\d+)\s*°?\s*c",
        r"à\s*([+-]?\d+)\s*°?\s*c",
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            return f"{m.group(1)}°C"
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
        "has_3way_valve": has_any(t, ["vanne 3 voies", "vanne 3 voies motorisée", "vanne 3 voies modulante"]),
        "has_valve": "vanne" in t,
        "has_fan": has_any(t, ["ventilation", "ventilateur"]),
        "has_defrost": has_any(t, ["dégivrage", "degivrage"]),
        "has_bypass": has_any(t, ["by-pass", "bypass", "boucle de dérivation", "boucle de derivation"]),
        "has_glycol": has_any(t, ["glycol", "glycolée", "glycolee", "eau glycolée", "eau glycolee"]),
        "has_evaporator": has_any(t, ["évaporateur", "evaporateur", "batterie froide", "aerotherme", "aérotherme"]),
        "is_pid": has_any(t, ["pid", "modul", "0-10v", "0/10v"]),
        "permanent_fan": "ventilation permanente" in t,
    }

    data["setpoint"] = extract_setpoint(t)
    data["pump_on"] = extract_threshold(t, "marche")
    data["pump_off"] = extract_threshold(t, "arrêt") or extract_threshold(t, "arret")

    m = re.search(r"(différentiel|differentiel)[^0-9]*([0-9]+)\s*k", t)
    data["differential"] = f"{m.group(2)}K" if m else None

    return data


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def svg_header(width: int, height: int) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {width} {height}" style="background:#ffffff">',
        "<style>",
        ".t{font:14px Arial, sans-serif; fill:#111;}",
        ".ts{font:12px Arial, sans-serif; fill:#111;}",
        ".tb{font:700 18px Arial, sans-serif; fill:#111;}",
        ".line{stroke:#111; stroke-width:2; fill:none;}",
        ".thin{stroke:#111; stroke-width:1.2; fill:none;}",
        ".box{stroke:#111; stroke-width:2; fill:#fff;}",
        ".rail{stroke:#111; stroke-width:3;}",
        ".guide{stroke:#aaa; stroke-width:1; stroke-dasharray:4 4; fill:none;}",
        "</style>",
    ]


def svg_footer(parts: list[str]) -> str:
    parts.append("</svg>")
    return "\n".join(parts)


def draw_title_block(parts: list[str], width: int, height: int, title: str) -> None:
    y = height - 55
    parts += [
        f'<rect x="20" y="{y}" width="{width-40}" height="35" class="box"/>',
        f'<text x="30" y="{y+22}" class="tb">{esc(title)}</text>',
    ]


def draw_page_grid(parts: list[str], width: int, height: int) -> None:
    top = 50
    bottom = height - 80
    left = 40
    right = width - 40

    parts += [
        f'<rect x="{left}" y="{top}" width="{right-left}" height="{bottom-top}" class="thin"/>'
    ]

    col_w = (right - left) / 10
    for i in range(1, 10):
        x = left + i * col_w
        parts.append(f'<line x1="{x}" y1="{top}" x2="{x}" y2="{bottom}" class="guide"/>')
        parts.append(f'<text x="{x-col_w/2:.0f}" y="{top-10}" class="ts">{i-1}</text>')

    row_h = (bottom - top) / 8
    letters = list("ABCDEFGH")
    for i in range(1, 8):
        y = top + i * row_h
        parts.append(f'<line x1="{left}" y1="{y}" x2="{right}" y2="{y}" class="guide"/>')
    for i, letter in enumerate(letters):
        yy = top + i * row_h + 20
        parts.append(f'<text x="18" y="{yy}" class="ts">{letter}</text>')


def draw_motor(parts: list[str], x: int, y: int, label: str) -> None:
    r = 20
    parts += [
        f'<circle cx="{x}" cy="{y}" r="{r}" class="box"/>',
        f'<text x="{x-6}" y="{y+5}" class="t">M</text>',
        f'<text x="{x+28}" y="{y+5}" class="t">{esc(label)}</text>',
    ]


def draw_breaker_3p(parts: list[str], x: int, y: int, label: str) -> None:
    spacing = 22
    for i in range(3):
        xx = x + i * spacing
        parts += [
            f'<line x1="{xx}" y1="{y-35}" x2="{xx}" y2="{y-10}" class="line"/>',
            f'<line x1="{xx}" y1="{y+10}" x2="{xx}" y2="{y+35}" class="line"/>',
            f'<line x1="{xx-7}" y1="{y-10}" x2="{xx+7}" y2="{y+10}" class="line"/>',
        ]
    parts.append(f'<text x="{x+80}" y="{y+5}" class="t">{esc(label)}</text>')


def draw_contactor_power_3p(parts: list[str], x: int, y: int, label: str) -> None:
    spacing = 22
    for i in range(3):
        xx = x + i * spacing
        parts += [
            f'<line x1="{xx}" y1="{y-35}" x2="{xx}" y2="{y-8}" class="line"/>',
            f'<line x1="{xx}" y1="{y+8}" x2="{xx}" y2="{y+35}" class="line"/>',
            f'<line x1="{xx-8}" y1="{y-8}" x2="{xx}" y2="{y+8}" class="line"/>',
        ]
    parts.append(f'<text x="{x+80}" y="{y+5}" class="t">{esc(label)}</text>')


def draw_power_supply(parts: list[str], x: int, y: int, label: str) -> None:
    parts += [
        f'<rect x="{x-20}" y="{y-20}" width="40" height="40" class="box"/>',
        f'<text x="{x-13}" y="{y+5}" class="t">PS</text>',
        f'<text x="{x+30}" y="{y+5}" class="t">{esc(label)}</text>',
    ]


def draw_valve_actuator(parts: list[str], x: int, y: int, label: str) -> None:
    parts += [
        f'<rect x="{x-18}" y="{y-18}" width="36" height="36" class="box"/>',
        f'<line x1="{x}" y1="{y+18}" x2="{x}" y2="{y+45}" class="line"/>',
        f'<polygon points="{x-15},{y+45} {x+15},{y+45} {x},{y+62}" class="box"/>',
        f'<text x="{x+28}" y="{y+5}" class="t">{esc(label)}</text>',
    ]


def draw_controller(parts: list[str], x: int, y: int, label: str) -> None:
    parts += [
        f'<rect x="{x-40}" y="{y-25}" width="80" height="50" class="box"/>',
        f'<text x="{x-18}" y="{y+5}" class="t">REG</text>',
        f'<text x="{x+50}" y="{y+5}" class="t">{esc(label)}</text>',
    ]


def draw_sensor(parts: list[str], x: int, y: int, label: str) -> None:
    parts += [
        f'<circle cx="{x}" cy="{y}" r="10" class="box"/>',
        f'<line x1="{x}" y1="{y+10}" x2="{x}" y2="{y+30}" class="line"/>',
        f'<text x="{x+18}" y="{y+5}" class="t">{esc(label)}</text>',
    ]


def draw_coil(parts: list[str], x: int, y: int, label: str) -> None:
    parts += [
        f'<line x1="{x}" y1="{y-25}" x2="{x}" y2="{y-10}" class="line"/>',
        f'<rect x="{x-16}" y="{y-10}" width="32" height="20" class="box"/>',
        f'<line x1="{x}" y1="{y+10}" x2="{x}" y2="{y+25}" class="line"/>',
        f'<text x="{x+25}" y="{y+5}" class="t">{esc(label)}</text>',
        f'<text x="{x+2}" y="{y-15}" class="ts">A1</text>',
        f'<text x="{x+2}" y="{y+22}" class="ts">A2</text>',
    ]


def draw_no_contact(parts: list[str], x: int, y: int, label: str) -> None:
    parts += [
        f'<line x1="{x-35}" y1="{y}" x2="{x-10}" y2="{y}" class="line"/>',
        f'<line x1="{x+10}" y1="{y}" x2="{x+35}" y2="{y}" class="line"/>',
        f'<line x1="{x-10}" y1="{y-14}" x2="{x+10}" y2="{y+14}" class="line"/>',
        f'<text x="{x+45}" y="{y+5}" class="t">{esc(label)}</text>',
    ]


def draw_terminal(parts: list[str], x: int, y: int, label: str) -> None:
    parts += [
        f'<line x1="{x}" y1="{y-15}" x2="{x}" y2="{y+15}" class="line"/>',
        f'<circle cx="{x}" cy="{y}" r="4" class="box"/>',
        f'<text x="{x+10}" y="{y+5}" class="t">{esc(label)}</text>',
    ]


def line(parts: list[str], x1: int, y1: int, x2: int, y2: int) -> None:
    parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="line"/>')


def text(parts: list[str], x: int, y: int, value: str, klass: str = "t") -> None:
    parts.append(f'<text x="{x}" y="{y}" class="{klass}">{esc(value)}</text>')


def render_svg(svg_code: str, height: int = 900) -> None:
    components.html(svg_code, height=height, scrolling=True)


def build_power_svg(data: dict) -> str:
    width, height = 1400, 900
    parts = svg_header(width, height)

    draw_page_grid(parts, width, height)
    text(parts, 50, 35, "Folio puissance", "tb")

    # Rails puissance
    line(parts, 90, 90, 90, 700)
    line(parts, 220, 90, 220, 700)
    line(parts, 350, 90, 350, 700)
    text(parts, 78, 82, "L1", "t")
    text(parts, 208, 82, "L2", "t")
    text(parts, 338, 82, "L3", "t")

    y_breaker = 170
    y_contactor = 310
    y_load = 500

    if data["has_pump"] or data["has_fan"] or data["has_3way_valve"]:
        draw_breaker_3p(parts, 90, y_breaker, "QF1")

    if data["has_pump"]:
        draw_contactor_power_3p(parts, 90, y_contactor, "KM1")
        draw_motor(parts, 90, y_load, "M1 Pompe")
        line(parts, 90, y_breaker + 35, 90, y_contactor - 35)
        line(parts, 112, y_breaker + 35, 112, y_contactor - 35)
        line(parts, 134, y_breaker + 35, 134, y_contactor - 35)
        line(parts, 90, y_contactor + 35, 90, y_load - 20)
        line(parts, 112, y_contactor + 35, 112, y_load - 20)
        line(parts, 134, y_contactor + 35, 134, y_load - 20)

    if data["has_fan"]:
        xoff = 420
        draw_breaker_3p(parts, xoff, y_breaker, "QF2")
        draw_motor(parts, xoff, y_load, "M2 Ventilation")
        line(parts, xoff, y_breaker + 35, xoff, y_load - 20)
        line(parts, xoff + 22, y_breaker + 35, xoff + 22, y_load - 20)
        line(parts, xoff + 44, y_breaker + 35, xoff + 44, y_load - 20)

    if data["has_3way_valve"]:
        draw_power_supply(parts, 820, 250, "PS1")
        draw_valve_actuator(parts, 820, 420, "YV1 Vanne 3 voies")
        line(parts, 820, 270, 820, 402)

    if data["has_evaporator"]:
        text(parts, 1040, 500, "Charge hydraulique / batterie / aérotherme", "t")
        parts.append('<rect x="1000" y="460" width="300" height="60" class="box"/>')

    draw_title_block(parts, width, height, "Puissance")
    return svg_footer(parts)


def build_control_svg(data: dict) -> str:
    width, height = 1600, 900
    parts = svg_header(width, height)

    draw_page_grid(parts, width, height)
    text(parts, 50, 35, "Folio commande", "tb")

    # Rails commande
    x_phase = 100
    x_neutral = 1500
    line(parts, x_phase, 80, x_phase, 800)
    line(parts, x_neutral, 80, x_neutral, 800)
    text(parts, x_phase - 20, 70, "L", "t")
    text(parts, x_neutral - 10, 70, "N", "t")

    # Ligne 1 : commande pompe
    y = 200
    if data["has_pump"]:
        line(parts, x_phase, y, 200, y)
        draw_no_contact(parts, 300, y, "Regulation pompe")
        line(parts, 335, y, 1100, y)
        draw_coil(parts, 1200, y, "KM1")
        line(parts, 1200, y + 25, 1200, y + 60)
        line(parts, 1200, y + 60, x_neutral, y + 60)
        line(parts, x_neutral, y + 60, x_neutral, y)

    # Ligne 2 : dégivrage
    if data["has_defrost"]:
        y = 350
        line(parts, x_phase, y, 200, y)
        draw_no_contact(parts, 300, y, "Arret degivrage")
        line(parts, 335, y, 1100, y)
        draw_coil(parts, 1200, y, "KM1")
        line(parts, 1200, y + 25, 1200, y + 60)
        line(parts, 1200, y + 60, x_neutral, y + 60)
        line(parts, x_neutral, y + 60, x_neutral, y)

    # Régulateur au milieu
    if data["has_controller"]:
        draw_controller(parts, 800, 550, "A1 Regulateur")

    # Sondes
    if data["has_temp_sensor"]:
        draw_sensor(parts, 500, 480, "TT1 Entree")
        draw_sensor(parts, 500, 620, "TT2 Reprise")
        line(parts, 510, 510, 760, 550)
        line(parts, 510, 650, 760, 550)

    # Sortie 0-10V vers vanne
    if data["has_3way_valve"]:
        draw_terminal(parts, 1200, 500, "AO+")
        draw_terminal(parts, 1250, 500, "AO-")
        text(parts, 1300, 505, "0-10V vers YV1", "t")
        if data["has_controller"]:
            line(parts, 840, 540, 1200, 500)
            line(parts, 840, 560, 1250, 500)

    # Infos
    if data["setpoint"]:
        text(parts, 750, 520, f"Consigne : {data['setpoint']}", "ts")
    if data["pump_on"]:
        text(parts, 750, 680, f"Marche : {data['pump_on']}", "ts")
    if data["pump_off"]:
        text(parts, 750, 700, f"Arret : {data['pump_off']}", "ts")
    if data["differential"]:
        text(parts, 750, 720, f"Diff : {data['differential']}", "ts")

    draw_title_block(parts, width, height, "Commande")
    return svg_footer(parts)


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


st.title("Générateur de schéma électrique conventionnel V6.1")
st.caption("Analyse fonctionnelle vers folio puissance et folio commande.")

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
        render_svg(control_svg, height=920)
