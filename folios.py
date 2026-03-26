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

    # Arrivée et protection générale
    x_cols = [90, 130, 170]
    for idx, xx in enumerate(x_cols, start=1):
        line(parts, xx, 95, xx, 720, "rail")
        text(parts, xx - 10, 82, f"L{idx}", "tiny")

    draw_switch_3p(parts, 90, 150, r["ig1"])
    draw_breaker_3p(parts, 90, 250, r["q1"])
    draw_contactor_y = 360
    draw_breaker_3p(parts, 90, draw_contactor_y, r["dm1"])

    # Départ pompe
    draw_breaker_3p(parts, 90, 470, r["q2"])
    draw_motor(parts, 90, 620, r["m1"])

    for xx in [90, 108, 126]:
        line(parts, xx, 178, xx, 222)
        line(parts, xx, 278, xx, 332)
        line(parts, xx, 388, xx, 442)
        line(parts, xx, 498, xx, 602)

    # Contacteur puissance
    from style import draw_contactor_3p
    draw_contactor_3p(parts, 90, 560, r["km1"])
    for xx in [90, 108, 126]:
        line(parts, xx, 498, xx, 534)
        line(parts, xx, 586, xx, 602)

    # Ventilation mono/mono simplifiée
    if data["has_fan"]:
        xf = 420
        line(parts, xf, 95, xf, 720, "rail")
        line(parts, xf + 40, 95, xf + 40, 720, "rail")
        text(parts, xf - 10, 82, "L", "tiny")
        text(parts, xf + 30, 82, "N", "tiny")
        draw_breaker_3p(parts, xf, 250, "QF Vent")
        draw_motor(parts, xf, 620, r["m2"])
        line(parts, xf, 278, xf, 602)
        line(parts, xf + 18, 278, xf + 18, 602)

    # Transfo / alim commande
    draw_transformer(parts, 760, 250, r["t1"])
    line(parts, 730, 180, 730, 238)
    line(parts, 790, 180, 790, 238)
    text(parts, 710, 165, "230V / 24V", "tiny")

    # Alimentation vanne
    if data["has_3way_valve"]:
        rect(parts, 1050, 230, 40, 36, "box")
        text(parts, 1058, 252, "PS", "text")
        text(parts, 1105, 252, r["ps1"], "text")
        rect(parts, 1054, 420, 32, 32, "box")
        line(parts, 1070, 452, 1070, 480)
        from style import poly
        poly(parts, [(1058, 480), (1082, 480), (1070, 495)], "box")
        text(parts, 1100, 440, r["yv1"], "text")
        line(parts, 1070, 266, 1070, 420)

    return svg_footer(parts)


def build_regulation_svg(data: dict) -> str:
    width, height = 1600, 900
    parts = svg_header(width, height)
    draw_sheet(parts, width, height, data["project_title"], "Folio commande / régulation")

    r = data["refs"]
    xL = 100
    xN = 1490

    line(parts, xL, 95, xL, 780, "rail")
    line(parts, xN, 95, xN, 780, "rail")
    text(parts, xL - 14, 82, "L", "tiny")
    text(parts, xN - 10, 82, "N", "tiny")

    # Rung pompe
    y1 = 180
    line(parts, xL, y1, 200, y1)
    if data["has_defrost"]:
        draw_contact_nc(parts, 280, y1, "DEG NF")
        line(parts, 314, y1, 390, y1)
    else:
        line(parts, 200, y1, 390, y1)

    draw_contact_no(parts, 470, y1, "REG pompe")
    line(parts, 504, y1, 1180, y1)
    draw_coil(parts, 1250, y1, r["km1"])
    line(parts, 1250, y1 + 18, 1250, y1 + 48)
    line(parts, 1250, y1 + 48, xN, y1 + 48)
    line(parts, xN, y1 + 48, xN, y1)

    # Rung ventilation
    if data["has_fan"]:
        y2 = 300
        line(parts, xL, y2, 1180, y2)
        draw_coil(parts, 1250, y2, "KV1")
        line(parts, 1250, y2 + 18, 1250, y2 + 48)
        line(parts, 1250, y2 + 48, xN, y2 + 48)
        line(parts, xN, y2 + 48, xN, y2)
        text(parts, 310, y2 - 12, "Ventilation permanente", "tiny")

    # Bloc régulateur type MPX PRO
    draw_controller(parts, 700, 430, 170, 110, r["a1"])
    rect(parts, 910, 430, 90, 110, "box")
    text(parts, 930, 455, r["dt1"], "bold")
    text(parts, 925, 480, "Détendeur /", "tiny")
    text(parts, 925, 495, "module I/O", "tiny")

    # Sondes
    if data["has_temp_sensor"]:
        draw_sensor(parts, 470, 450, r["tt1"])
        draw_sensor(parts, 470, 540, r["tt2"])

        line(parts, 470, 472, 470, 485)
        line(parts, 470, 485, 700, 485)

        line(parts, 470, 562, 470, 515)
        line(parts, 470, 515, 700, 515)

    # Sorties vers DT1
    line(parts, 870, 455, 910, 455)
    line(parts, 870, 485, 910, 485)
    line(parts, 870, 515, 910, 515)

    text(parts, 760, 418, "DI / AI / relais", "tiny")
    text(parts, 928, 418, "Pilotage vanne", "tiny")

    # Sortie analogique vanne
    if data["has_3way_valve"]:
        draw_terminal(parts, 1140, 470, "AO+")
        draw_terminal(parts, 1195, 470, "AO-")
        line(parts, 1000, 470, 1140, 470)
        line(parts, 1000, 500, 1195, 500)
        text(parts, 1245, 474, "0-10V vers YV1", "text")

    # Infos consigne
    text(parts, 700, 640, f'Consigne : {data["setpoint"]}', "text")
    text(parts, 700, 660, f'Marche pompe : {data["pump_on"]}', "text")
    text(parts, 700, 680, f'Arrêt pompe : {data["pump_off"]}', "text")
    text(parts, 700, 700, f'Différentiel : {data["differential"]}', "text")

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
