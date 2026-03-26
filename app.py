import re
import html
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Dossier électrique type froid",
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
        "has_3way_valve": _has_any(
            t,
            ["vanne 3 voies", "vanne 3 voies modulante", "vanne 3 voies motorisée"],
        ),
        "has_defrost": _has_any(t, ["dégivrage", "degivrage"]),
        "setpoint": setpoint or "+4°C",
        "pump_on": pump_on or "+12°C",
        "pump_off": pump_off or "+10°C",
        "differential": differential,
        "refs": {
            "ig1": "IG1",
            "q1": "Q1",
            "q2": "Q2",
            "dm1": "DM1",
            "km1": "KM1",
            "kv1": "KV1",
            "t1": "T1",
            "a1": "A1",
            "dt1": "DT1",
            "x1": "X1",
            "m1": "M1 Pompe",
            "m2": "M2 Ventilation",
            "yv1": "YV1",
            "tt1": "TT1",
            "tt2": "TT2",
            "ps1": "PS1",
            "fr1": "FR1",
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
        ".thin{stroke:#c7c7c7; stroke-width:1; fill:none; stroke-dasharray:4 4;}",
        ".box{stroke:#111; stroke-width:1.5; fill:#fff;}",
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
# PETITS SYMBOLES
# =========================================================

def draw_switch_3p(parts: list[str], x: int, y: int, label: str) -> None:
    for i in range(3):
        xx = x + i * 18
        line(parts, xx, y - 24, xx, y + 24)
        line(parts, xx - 6, y - 8, xx + 6, y + 8)
    text(parts, x + 58, y + 4, label, "text")


def draw_breaker_3p(parts: list[str], x: int, y: int, label: str) -> None:
    for i in range(3):
        xx = x + i * 18
        line(parts, xx, y - 24, xx, y - 6)
        line(parts, xx - 6, y - 6, xx + 6, y + 6)
        line(parts, xx, y + 6, xx, y + 24)
    text(parts, x + 58, y + 4, label, "text")


def draw_contactor_3p(parts: list[str], x: int, y: int, label: str) -> None:
    for i in range(3):
        xx = x + i * 18
        line(parts, xx, y - 24, xx, y - 5)
        line(parts, xx - 8, y - 5, xx, y + 8)
        line(parts, xx, y + 8, xx, y + 24)
    text(parts, x + 58, y + 4, label, "text")


def draw_motor(parts: list[str], x: int, y: int, label: str) -> None:
    circle(parts, x, y, 18)
    text(parts, x - 6, y + 5, "M", "text")
    text(parts, x + 28, y + 5, label, "text")


def draw_transformer(parts: list[str], x: int, y: int, label: str) -> None:
    circle(parts, x - 10, y, 12)
    circle(parts, x + 10, y, 12)
    text(parts, x + 30, y + 4, label, "text")


def draw_contact_no(parts: list[str], x: int, y: int, label: str) -> None:
    line(parts, x - 30, y, x - 8, y)
    line(parts, x + 8, y, x + 30, y)
    line(parts, x - 8, y - 10, x + 8, y + 10)
    text(parts, x + 40, y + 4, label, "text")


def draw_contact_nc(parts: list[str], x: int, y: int, label: str) -> None:
    line(parts, x - 30, y, x - 8, y)
    line(parts, x + 8, y, x + 30, y)
    line(parts, x - 8, y - 10, x + 8, y + 10)
    line(parts, x - 8, y + 10, x + 8, y - 10)
    text(parts, x + 40, y + 4, label, "text")


def draw_coil(parts: list[str], x: int, y: int, label: str) -> None:
    rect(parts, x - 16, y - 10, 32, 20, "box")
    text(parts, x + 24, y + 4, label, "text")
    text(parts, x + 1, y - 14, "A1", "tiny")
    text(parts, x + 1, y + 22, "A2", "tiny")


def draw_sensor(parts: list[str], x: int, y: int, label: str) -> None:
    circle(parts, x, y, 7)
    line(parts, x, y + 7, x, y + 22)
    text(parts, x + 14, y + 4, label, "text")


def draw_terminal(parts: list[str], x: int, y: int, label: str) -> None:
    circle(parts, x, y, 4)
    line(parts, x, y - 10, x, y + 10)
    text(parts, x + 10, y + 4, label, "text")


# =========================================================
# FOLIO 10 - PUISSANCE
# =========================================================

def build_power_svg(data: dict) -> str:
    width, height = 1500, 900
    parts = svg_header(width, height)
    draw_sheet(parts, width, height, data["project_title"], "10 - Puissance", "10")

    r = data["refs"]

    # Départ pompe à gauche, plus compact et plus proche d'un folio réel
    x = 85
    cols = [x, x + 30, x + 60]
    for idx, xx in enumerate(cols, start=1):
        line(parts, xx, 95, xx, 705, "rail")
        text(parts, xx - 8, 82, f"L{idx}", "tiny")

    draw_switch_3p(parts, x, 145, r["ig1"])
    draw_breaker_3p(parts, x, 225, r["q1"])
    draw_breaker_3p(parts, x, 310, r["dm1"])
    draw_breaker_3p(parts, x, 395, r["q2"])
    draw_contactor_3p(parts, x, 500, r["km1"])
    draw_motor(parts, x, 625, r["m1"])

    for xx in [x, x + 18, x + 36]:
        line(parts, xx, 169, xx, 201)
        line(parts, xx, 249, xx, 286)
        line(parts, xx, 334, xx, 371)
        line(parts, xx, 419, xx, 476)
        line(parts, xx, 524, xx, 607)

    # Départ ventilation
    if data["has_fan"]:
        xf = 360
        line(parts, xf, 95, xf, 705, "rail")
        line(parts, xf + 30, 95, xf + 30, 705, "rail")
        text(parts, xf - 6, 82, "L", "tiny")
        text(parts, xf + 22, 82, "N", "tiny")
        draw_breaker_3p(parts, xf, 225, "QF Vent")
        draw_motor(parts, xf, 625, r["m2"])
        line(parts, xf, 249, xf, 607)
        line(parts, xf + 18, 249, xf + 18, 607)

    # Transformateur
    draw_transformer(parts, 690, 245, r["t1"])
    line(parts, 660, 195, 660, 233)
    line(parts, 720, 195, 720, 233)
    text(parts, 642, 182, "230V/24V", "tiny")

    # Alimentation actionneur
    if data["has_3way_valve"]:
        rect(parts, 1030, 225, 42, 34, "box")
        text(parts, 1038, 247, "PS", "text")
        text(parts, 1088, 247, r["ps1"], "text")

        rect(parts, 1035, 395, 32, 32, "box")
        line(parts, 1051, 427, 1051, 454)
        poly(parts, [(1039, 454), (1063, 454), (1051, 468)], "box")
        text(parts, 1085, 414, f'{r["yv1"]} Vanne 3 voies', "text")
        line(parts, 1051, 259, 1051, 395)

    # Petit bloc repérage
    text(parts, 1205, 150, "Départs principaux", "small")
    text(parts, 1205, 170, "Pompe / ventilation / actionneur", "small")

    return svg_footer(parts)


# =========================================================
# FOLIO 11 - COMMANDE MPX / DT1
# =========================================================

def build_command_svg(data: dict) -> str:
    width, height = 1600, 900
    parts = svg_header(width, height)
    draw_sheet(parts, width, height, data["project_title"], "11 - MPX PRO / Détente électrique / Dégivrage naturel", "11")

    r = data["refs"]

    xL = 95
    xN = 1510
    line(parts, xL, 90, xL, 790, "rail")
    line(parts, xN, 90, xN, 790, "rail")
    text(parts, xL - 14, 80, "L", "bold")
    text(parts, xN - 10, 80, "N", "bold")

    # Rang 1 pompe
    y1 = 175
    line(parts, xL, y1, 210, y1)
    if data["has_defrost"]:
        draw_contact_nc(parts, 260, y1, "DEG")
        line(parts, 290, y1, 365, y1)
    else:
        line(parts, 210, y1, 365, y1)

    draw_contact_no(parts, 415, y1, "REG")
    line(parts, 445, y1, 1210, y1)
    draw_coil(parts, 1330, y1, r["km1"])
    line(parts, 1210, y1, 1314, y1)
    line(parts, 1346, y1, xN, y1)

    # Auto-maintien KM1
    line(parts, 365, y1 - 40, 365, y1)
    line(parts, 1210, y1 - 40, 1210, y1)
    line(parts, 365, y1 - 40, 510, y1 - 40)
    draw_contact_no(parts, 560, y1 - 40, "KM1 13-14")
    line(parts, 590, y1 - 40, 1210, y1 - 40)

    # Rang 2 ventilation
    if data["has_fan"]:
        y2 = 275
        line(parts, xL, y2, 1210, y2)
        draw_coil(parts, 1330, y2, r["kv1"])
        line(parts, 1210, y2, 1314, y2)
        line(parts, 1346, y2, xN, y2)
        text(parts, 300, y2 - 10, "Ventilation permanente", "tiny")

    # Bloc MPX et DT1
    rect(parts, 620, 430, 210, 130, "box")
    text(parts, 635, 452, "A1 MPX PRO", "bold")
    text(parts, 635, 474, "Entrées sondes", "small")
    text(parts, 635, 492, "Sorties relais / AO", "small")
    text(parts, 635, 510, "Commande pompe / vanne", "small")

    rect(parts, 890, 448, 95, 70, "box")
    text(parts, 910, 472, "DT1", "bold")
    text(parts, 902, 492, "Interface", "small")
    text(parts, 900, 510, "0-10V", "small")

    # Sondes
    if data["has_temp_sensor"]:
        draw_sensor(parts, 480, 465, r["tt1"])
        draw_sensor(parts, 480, 525, r["tt2"])
        line(parts, 500, 465, 620, 465)
        line(parts, 500, 525, 620, 525)
        text(parts, 510, 457, "Entrée batterie", "tiny")
        text(parts, 510, 517, "Reprise", "tiny")

    # Sorties vanne
    if data["has_3way_valve"]:
        line(parts, 830, 470, 890, 470)
        line(parts, 985, 470, 1070, 470)
        draw_terminal(parts, 1070, 470, "AO+")
        draw_terminal(parts, 1145, 470, "AO-")
        text(parts, 1190, 474, "0-10V vers YV1", "text")

    # Paramètres
    text(parts, 635, 610, f'Consigne : {data["setpoint"]}', "text")
    text(parts, 635, 632, f'Marche pompe : {data["pump_on"]}', "text")
    text(parts, 635, 654, f'Arrêt pompe : {data["pump_off"]}', "text")
    text(parts, 635, 676, f'Différentiel : {data["differential"]}', "text")
    text(parts, 635, 698, "Mode : dégivrage naturel", "text")

    return svg_footer(parts)


# =========================================================
# FOLIO 15/16 - BORNIER X1
# =========================================================

def build_terminal_svg(data: dict) -> str:
    width, height = 1450, 900
    parts = svg_header(width, height)
    draw_sheet(parts, width, height, data["project_title"], "15-16 - Bornier X1", "12")

    r = data["refs"]
    text(parts, 90, 130, f'Bornier {r["x1"]}', "bold")

    x = 85
    y = 165

    rect(parts, x, y, 1185, 34, "box")
    line(parts, x + 130, y, x + 130, y + 34)
    line(parts, x + 605, y, x + 605, y + 34)
    text(parts, x + 18, y + 22, "Repère", "bold")
    text(parts, x + 160, y + 22, "Fonction", "bold")
    text(parts, x + 655, y + 22, "Extérieur", "bold")

    rows = [
        ("1", "Sonde TT1 entrée batterie", "Champ"),
        ("2", "Sonde TT2 reprise", "Champ"),
        ("3", "Sortie 0-10V AO+", "Actionneur YV1"),
        ("4", "Sortie 0-10V AO-", "Actionneur YV1"),
        ("5", "Commande pompe", "KM1"),
        ("6", "Retour neutre", "N"),
        ("7", "Commande ventilation", "KV1"),
        ("8", "Info dégivrage", "Entrée REG"),
        ("9", "Alim actionneur", "PS1"),
        ("10", "Commun régulation", "A1"),
    ]

    for i, row in enumerate(rows):
        yy = y + 42 + i * 31
        rect(parts, x, yy, 1185, 25, "box")
        line(parts, x + 130, yy, x + 130, yy + 25)
        line(parts, x + 605, yy, x + 605, yy + 25)
        text(parts, x + 18, yy + 17, row[0], "text")
        text(parts, x + 160, yy + 17, row[1], "text")
        text(parts, x + 655, yy + 17, row[2], "text")

    return svg_footer(parts)


# =========================================================
# FOLIO 20 - NOMENCLATURE
# =========================================================

def build_bom_svg(data: dict) -> str:
    width, height = 1450, 900
    parts = svg_header(width, height)
    draw_sheet(parts, width, height, data["project_title"], "20 - Nomenclature matériel", "13")

    items = [
        ("IG1", "Interrupteur général", "1"),
        ("Q1", "Protection générale", "1"),
        ("DM1", "Protection moteur pompe", "1"),
        ("Q2", "Protection départ pompe", "1"),
        ("KM1", "Contacteur pompe", "1"),
        ("KV1", "Relais ventilation", "1"),
        ("T1", "Transformateur alimentation commande", "1"),
        ("A1", "Régulateur MPX PRO", "1"),
        ("DT1", "Module interface 0-10V", "1"),
        ("PS1", "Alimentation actionneur", "1"),
        ("X1", "Bornier extérieur", "1"),
        ("YV1", "Actionneur vanne 3 voies 0-10V", "1"),
        ("TT1", "Sonde entrée batterie", "1"),
        ("TT2", "Sonde reprise", "1"),
    ]

    x = 85
    y = 150
    rect(parts, x, y, 1185, 34, "box")
    line(parts, x + 180, y, x + 180, y + 34)
    line(parts, x + 950, y, x + 950, y + 34)
    text(parts, x + 18, y + 22, "Repère", "bold")
    text(parts, x + 210, y + 22, "Désignation", "bold")
    text(parts, x + 995, y + 22, "Qté", "bold")

    for i, item in enumerate(items):
        yy = y + 42 + i * 29
        rect(parts, x, yy, 1185, 24, "box")
        line(parts, x + 180, yy, x + 180, yy + 24)
        line(parts, x + 950, yy, x + 950, yy + 24)
        text(parts, x + 18, yy + 16, item[0], "text")
        text(parts, x + 210, yy + 16, item[1], "text")
        text(parts, x + 995, yy + 16, item[2], "text")

    return svg_footer(parts)


# =========================================================
# FOLIO 25 - LISTE MATÉRIEL
# =========================================================

def build_material_svg(data: dict) -> str:
    width, height = 1450, 900
    parts = svg_header(width, height)
    draw_sheet(parts, width, height, data["project_title"], "25 - Liste du matériel", "14")

    rows = [
        ("IG1", "Interrupteur-sectionneur", "1", "Schneider / équiv."),
        ("Q1", "Disjoncteur général", "1", "Courbe C"),
        ("DM1", "Disjoncteur moteur pompe", "1", "Réglable"),
        ("Q2", "Protection départ pompe", "1", "Magnétothermique"),
        ("KM1", "Contacteur puissance pompe", "1", "Bobine commande"),
        ("KV1", "Relais ventilation", "1", "Commande ventilo"),
        ("T1", "Transformateur 230/24V", "1", "Commande"),
        ("A1", "Régulateur MPX PRO", "1", "CAREL / équiv."),
        ("DT1", "Module analogique 0-10V", "1", "Interface vanne"),
        ("PS1", "Alimentation actionneur", "1", "Selon tension vanne"),
        ("YV1", "Vanne 3 voies + actionneur", "1", "Modulante"),
        ("TT1", "Sonde entrée batterie", "1", "NTC/PTC selon régul."),
        ("TT2", "Sonde reprise", "1", "NTC/PTC selon régul."),
        ("X1", "Bornier de raccordement", "1", "Extérieur coffret"),
    ]

    x = 65
    y = 145
    rect(parts, x, y, 1220, 34, "box")
    line(parts, x + 140, y, x + 140, y + 34)
    line(parts, x + 710, y, x + 710, y + 34)
    line(parts, x + 820, y, x + 820, y + 34)
    text(parts, x + 18, y + 22, "Repère", "bold")
    text(parts, x + 165, y + 22, "Description", "bold")
    text(parts, x + 742, y + 22, "Qté", "bold")
    text(parts, x + 850, y + 22, "Observation", "bold")

    for i, row in enumerate(rows):
        yy = y + 40 + i * 28
        rect(parts, x, yy, 1220, 23, "box")
        line(parts, x + 140, yy, x + 140, yy + 23)
        line(parts, x + 710, yy, x + 710, yy + 23)
        line(parts, x + 820, yy, x + 820, yy + 23)
        text(parts, x + 18, yy + 15, row[0], "text")
        text(parts, x + 165, yy + 15, row[1], "text")
        text(parts, x + 742, yy + 15, row[2], "text")
        text(parts, x + 850, yy + 15, row[3], "text")

    return svg_footer(parts)


# =========================================================
# FOLIO 30 - IMPLANTATION
# =========================================================

def build_implantation_svg(data: dict) -> str:
    width, height = 1450, 900
    parts = svg_header(width, height)
    draw_sheet(parts, width, height, data["project_title"], "30 - Implantation", "15")

    # contour coffret
    rect(parts, 140, 120, 1080, 620, "box")
    text(parts, 160, 145, "Vue avant coffret", "bold")

    # rangée haute
    rect(parts, 220, 200, 95, 55, "box")
    text(parts,
