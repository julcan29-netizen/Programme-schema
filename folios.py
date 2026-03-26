from style import (
    draw_breaker_3p,
    draw_coil,
    draw_contact_nc,
    draw_contact_no,
    draw_controller,
    draw_motor,
    draw_sensor,
    draw_sheet,
    draw_switch_3p,
    draw_terminal,
    draw_transformer,
    line,
    poly,
    rect,
    svg_footer,
    svg_header,
    text,
)


def build_power_svg(data: dict) -> str:
    width, height = 1500, 900
    parts = svg_header(width, height)
    draw_sheet(parts, width, height, data["project_title"], "Folio puissance")

    r = data["refs"]

    x_cols = [90, 130, 170]
    for idx, xx in enumerate(x_cols, start=1):
        line(parts, xx, 95, xx, 720, "rail")
        text(parts, xx - 10, 82, f"L{idx}", "tiny")

    draw_switch_3p(parts, 90, 150, r["ig1"])
    draw_breaker_3p(parts, 90, 250, r["q1"])
    draw_breaker_3p(parts, 90, 360, r["dm1"])

    draw_breaker_3p(parts, 90, 470, r["q2"])

    from style import draw_contactor_3p
    draw_contactor_3p(parts, 90, 560, r["km1"])
    draw_motor(parts, 90, 650, r["m1"])

    for xx in [90, 108, 126]:
        line(parts, xx, 178, xx, 222)
        line(parts, xx, 278, xx, 332)
        line(parts, xx, 388, xx, 442)
        line(parts, xx, 498, xx, 534)
        line(parts, xx, 586, xx, 632)

    if data["has_fan"]:
        xf = 420
        line(parts, xf, 95, xf, 720, "rail")
        line(parts, xf + 40, 95, xf + 40, 720, "rail")
        text(parts, xf - 10, 82, "L", "tiny")
        text(parts, xf + 30, 82, "N", "tiny")
        draw_breaker_3p(parts, xf, 250, "QF Vent")
        draw_motor(parts, xf, 650, r["m2"])
        line(parts, xf, 278, xf, 632)
        line(parts, xf + 18, 278, xf + 18, 632)

    draw_transformer(parts, 760, 250, r["t1"])
    line(parts, 730, 180, 730, 238)
    line(parts, 790, 180, 790, 238)
    text(parts, 710, 165, "230V / 24V", "tiny")

    if data["has_3way_valve"]:
        rect(parts, 1050, 230, 40, 36, "box")
        text(parts, 1058, 252, "PS", "text")
        text(parts, 1105, 252, r["ps1"], "text")
        rect(parts, 1054, 420, 32, 32, "box")
        line(parts, 1070, 452, 1070, 480)
        poly(parts, [(1058, 480), (1082, 480), (1070, 495)], "box")
        text(parts, 1100, 440, r["yv1"], "text")
        line(parts, 1070, 266, 1070, 420)

    return svg_footer(parts)


def build_regulation_svg(data: dict) -> str:
    width, height = 1600, 900
    parts = svg_header(width, height)
    draw_sheet(parts, width, height, data["project_title"], "Folio commande")

    r = data["refs"]
    xL = 100
    xN = 1500

    line(parts, xL, 80, xL, 800, "rail")
    line(parts, xN, 80, xN, 800, "rail")

    text(parts, xL - 15, 70, "L", "bold")
    text(parts, xN - 10, 70, "N", "bold")

    # RANG 1 : COMMANDE POMPE
    y = 200
    line(parts, xL, y, xN, y)

    if data["has_defrost"]:
        draw_contact_nc(parts, 250, y, "DEG")
    draw_contact_no(parts, 420, y, "REG")

    draw_coil(parts, 1350, y, r["km1"])

    # RANG 2 : VENTILATION
    if data["has_fan"]:
        y2 = 300
        line(parts, xL, y2, xN, y2)
        draw_coil(parts, 1350, y2, "KV1")
        text(parts, 320, y2 - 10, "Ventilation permanente", "tiny")

    # RANG 3 : REGULATEUR
    y3 = 500
    draw_controller(parts, 700, y3 - 50, 150, 100, r["a1"])

    if data["has_temp_sensor"]:
        draw_sensor(parts, 500, y3 - 30, r["tt1"])
        draw_sensor(parts, 500, y3 + 40, r["tt2"])

        line(parts, 520, y3 - 30, 700, y3 - 30)
        line(parts, 520, y3 + 40, 700, y3 + 40)

    if data["has_3way_valve"]:
        draw_terminal(parts, 1000, y3, "AO+")
        draw_terminal(parts, 1100, y3, "AO-")
        line(parts, 850, y3, 1000, y3)
        line(parts, 850, y3 + 30, 1100, y3 + 30)
        text(parts, 1150, y3 + 5, "0-10V YV1", "text")

    text(parts, 700, 700, f'Consigne : {data["setpoint"]}', "text")
    text(parts, 700, 720, f'Marche : {data["pump_on"]}', "text")
    text(parts, 700, 740, f'Arrêt : {data["pump_off"]}', "text")
    text(parts, 700, 760, f'Différentiel : {data["differential"]}', "text")

    return svg_footer(parts)


def build_terminal_svg(data: dict) -> str:
    width, height = 1450, 900
    parts = svg_header(width, height)
    draw_sheet(parts, width, height, data["project_title"], "Folio bornier")

    r = data["refs"]

    text(parts, 90, 130, f'Bornier {r["x1"]}', "bold")

    x = 90
    y = 170
    row_h = 48

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
        ("7", "Ventilation", "KV1"),
        ("8", "Dégivrage", "Entrée REG"),
    ]

    for i, row in enumerate(rows):
        yy = y + 48 + i * row_h
        rect(parts, x, yy, 1180, 30, "box")
        line(parts, x + 140, yy, x + 140, yy + 30)
        line(parts, x + 620, yy, x + 620, yy + 30)
        text(parts, x + 25, yy + 20, row[0], "text")
        text(parts, x + 170, yy + 20, row[1], "text")
        text(parts, x + 670, yy + 20, row[2], "text")

    return svg_footer(parts)


def build_bom_svg(data: dict) -> str:
    width, height = 1450, 900
    parts = svg_header(width, height)
    draw_sheet(parts, width, height, data["project_title"], "Nomenclature simplifiée")

    items = [
        ("IG1", "Interrupteur général", "1"),
        ("Q1", "Protection générale", "1"),
        ("DM1", "Protection moteur pompe", "1"),
        ("Q2", "Protection départ pompe", "1"),
        ("KM1", "Contacteur pompe", "1"),
        ("T1", "Transformateur alimentation commande", "1"),
        ("A1", "Régulateur MPX PRO", "1"),
        ("DT1", "Module détente / sortie vanne", "1"),
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
        yy = y + 44 + i * 36
        rect(parts, x, yy, 1180, 28, "box")
        line(parts, x + 180, yy, x + 180, yy + 28)
        line(parts, x + 930, yy, x + 930, yy + 28)
        text(parts, x + 20, yy + 18, item[0], "text")
        text(parts, x + 210, yy + 18, item[1], "text")
        text(parts, x + 990, yy + 18, item[2], "text")

    return svg_footer(parts)
