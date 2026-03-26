from style import (
    draw_breaker_3p,
    draw_contactor_3p,
    draw_motor,
    draw_page,
    draw_psu,
    draw_valve_actuator,
    line,
    svg_footer,
    svg_header,
    text,
)


def build_power_svg(data: dict) -> str:
    width, height = 1400, 900
    parts = svg_header(width, height)
    draw_page(parts, width, height, "Folio puissance")

    refs = data["refs"]

    # Départ pompe
    x1, x2, x3 = 90, 150, 210
    for xx, name in [(x1, "L1"), (x2, "L2"), (x3, "L3")]:
        line(parts, xx, 90, xx, 700, "rail")
        text(parts, xx - 10, 80, name, "ts")

    if data["has_pump"]:
        draw_breaker_3p(parts, 90, 170, refs["main_breaker"])
        draw_contactor_3p(parts, 90, 305, refs["pump_contactor"])
        draw_motor(parts, 90, 510, f'{refs["pump_motor"]} Pompe')
        for xx in [90, 108, 126]:
            line(parts, xx, 200, xx, 277)
            line(parts, xx, 333, xx, 492)

    # Départ ventilation
    if data["has_fan"]:
        xf = 430
        for i, name in enumerate(["L1", "L2", "L3"]):
            xx = xf + i * 60
            line(parts, xx, 90, xx, 700, "rail")
            if i == 0:
                text(parts, xx - 10, 80, "L1", "ts")
        draw_breaker_3p(parts, xf, 170, refs["fan_breaker"])
        draw_motor(parts, xf, 510, f'{refs["fan_motor"]} Ventilation')
        for xx in [xf, xf + 18, xf + 36]:
            line(parts, xx, 200, xx, 492)

    # Actionneur vanne
    if data["has_3way_valve"]:
        draw_psu(parts, 930, 250, refs["valve_psu"])
        draw_valve_actuator(parts, 930, 430, f'{refs["valve_actuator"]} Vanne 3 voies')
        line(parts, 930, 268, 930, 414)

    return svg_footer(parts)
