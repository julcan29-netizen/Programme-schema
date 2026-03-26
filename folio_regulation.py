from style import (
    draw_coil,
    draw_contact_nc,
    draw_contact_no,
    draw_controller,
    draw_page,
    draw_sensor,
    draw_terminal,
    line,
    svg_footer,
    svg_header,
    text,
)


def build_regulation_svg(data: dict) -> str:
    width, height = 1600, 900
    parts = svg_header(width, height)
    draw_page(parts, width, height, "Folio commande")

    refs = data["refs"]

    xL = 100
    xN = 1500

    line(parts, xL, 90, xL, 780, "rail")
    line(parts, xN, 90, xN, 780, "rail")
    text(parts, xL - 14, 78, "L", "t")
    text(parts, xN - 10, 78, "N", "t")

    # RANG 1 : pompe avec NF dégivrage + NO régulation + bobine KM1
    if data["has_pump"]:
        y1 = 190
        line(parts, xL, y1, 210, y1)

        if data["has_defrost"]:
            draw_contact_nc(parts, 290, y1, "DEG NF")
            line(parts, 322, y1, 390, y1)
        else:
            line(parts, 210, y1, 390, y1)

        draw_contact_no(parts, 470, y1, "REG demande pompe")
        line(parts, 502, y1, 1180, y1)
        draw_coil(parts, 1250, y1, refs["pump_contactor"])
        line(parts, 1250, y1 + 20, 1250, y1 + 50)
        line(parts, 1250, y1 + 50, xN, y1 + 50)
        line(parts, xN, y1 + 50, xN, y1)

    # RANG 2 : ventilation permanente
    if data["has_fan"]:
        y2 = 320
        line(parts, xL, y2, 1180, y2)
        draw_coil(parts, 1250, y2, "KV1")
        line(parts, 1250, y2 + 20, 1250, y2 + 50)
        line(parts, 1250, y2 + 50, xN, y2 + 50)
        line(parts, xN, y2 + 50, xN, y2)
        text(parts, 300, y2 - 12, "Ventilation permanente", "ts")

    # Régulateur
    draw_controller(parts, 820, 520, refs["controller"])

    # Sondes
    if data["has_temp_sensor"]:
        draw_sensor(parts, 500, 460, f'{refs["temp_in"]} Entrée')
        draw_sensor(parts, 500, 590, f'{refs["temp_return"]} Reprise')

        # câblage orthogonal
        line(parts, 500, 486, 500, 520)
        line(parts, 500, 520, 778, 520)

        line(parts, 500, 616, 500, 550)
        line(parts, 500, 550, 778, 550)

    # Sortie analogique vers vanne
    if data["has_3way_valve"]:
        draw_terminal(parts, 1180, 500, "AO+")
        draw_terminal(parts, 1230, 500, "AO-")
        line(parts, 862, 505, 1180, 505)
        line(parts, 862, 535, 1230, 535)
        text(parts, 1280, 505, "0-10V vers YV1", "t")

    # infos
    yy = 680
    if data["setpoint"]:
        text(parts, 760, yy, f'Consigne : {data["setpoint"]}', "ts")
        yy += 20
    if data["pump_on"]:
        text(parts, 760, yy, f'Marche pompe : {data["pump_on"]}', "ts")
        yy += 20
    if data["pump_off"]:
        text(parts, 760, yy, f'Arrêt pompe : {data["pump_off"]}', "ts")
        yy += 20
    if data["differential"]:
        text(parts, 760, yy, f'Différentiel : {data["differential"]}', "ts")

    return svg_footer(parts)
