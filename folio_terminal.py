from style import draw_page, line, rect, svg_footer, svg_header, text


def build_terminal_svg(data: dict) -> str:
    width, height = 1400, 900
    parts = svg_header(width, height)
    draw_page(parts, width, height, "Folio bornier")

    refs = data["refs"]

    x0 = 120
    y0 = 180
    row_h = 55

    headers = ["Repère", "Fonction", "Extérieur"]
    col_x = [120, 320, 820]
    for i, header in enumerate(headers):
        text(parts, col_x[i], y0 - 25, header, "tb")

    rows = [
        ("1", "Sonde TT1 entrée", "Champ"),
        ("2", "Sonde TT2 reprise", "Champ"),
        ("3", "Sortie 0-10V AO+", "Actionneur YV1"),
        ("4", "Sortie 0-10V AO-", "Actionneur YV1"),
        ("5", "Commande pompe", "KM1"),
        ("6", "Commun / neutre", "N"),
    ]

    text(parts, 120, 110, f'Bornier {refs["terminal_strip"]}', "tb")

    for i, row in enumerate(rows):
        y = y0 + i * row_h
        rect(parts, 90, y - 22, 1180, 36)
        line(parts, 260, y - 22, 260, y + 14)
        line(parts, 760, y - 22, 760, y + 14)
        text(parts, 120, y, row[0], "t")
        text(parts, 320, y, row[1], "t")
        text(parts, 820, y, row[2], "t")

    return svg_footer(parts)
