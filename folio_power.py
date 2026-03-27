# folio_power.py
import svgwrite
import streamlit as st

from model import Folio, split_ref
from reference_case import get_reference_power_folio
from validators import validate_power_folio


PAGE_W = 1400
PAGE_H = 900

GRID = 20
TOP_BUS_Y_L = 60
TOP_BUS_Y_N = 80
TOP_BUS_Y_PE = 100

SYMBOL_W = 90
SYMBOL_H = 60


def snap(v: int) -> int:
    return round(v / GRID) * GRID


def draw_page_frame(dwg: svgwrite.Drawing, folio: Folio):
    dwg.add(dwg.rect(insert=(10, 10), size=(PAGE_W - 20, PAGE_H - 20),
                     fill="white", stroke="black", stroke_width=1))

    dwg.add(dwg.text(f"FOLIO {folio.number}", insert=(1150, 40), font_size="20px", font_weight="bold"))
    dwg.add(dwg.text(f"{folio.title}", insert=(80, 40), font_size="22px", font_weight="bold"))

    # Cartouche simple
    dwg.add(dwg.rect(insert=(1000, 780), size=(350, 90), fill="none", stroke="black"))
    dwg.add(dwg.text("Projet : Cas de référence CVC", insert=(1010, 810), font_size="14px"))
    dwg.add(dwg.text("Folio : 10 - Puissance", insert=(1010, 835), font_size="14px"))
    dwg.add(dwg.text("Standard : type industriel", insert=(1010, 860), font_size="14px"))


def draw_buses(dwg: svgwrite.Drawing):
    dwg.add(dwg.line((60, TOP_BUS_Y_L), (1320, TOP_BUS_Y_L), stroke="black", stroke_width=2))
    dwg.add(dwg.text("L", insert=(30, TOP_BUS_Y_L + 5), font_size="16px", font_weight="bold"))

    dwg.add(dwg.line((60, TOP_BUS_Y_N), (1320, TOP_BUS_Y_N), stroke="black", stroke_width=2))
    dwg.add(dwg.text("N", insert=(30, TOP_BUS_Y_N + 5), font_size="16px", font_weight="bold"))

    dwg.add(dwg.line((60, TOP_BUS_Y_PE), (1320, TOP_BUS_Y_PE), stroke="black", stroke_width=2))
    dwg.add(dwg.text("PE", insert=(20, TOP_BUS_Y_PE + 5), font_size="16px", font_weight="bold"))


def get_terminal_pos(device_kind: str, x: int, y: int, terminal: str):
    """
    Coordonnées standardisées des bornes.
    """
    # bornes haut / bas pour appareils verticaux
    if device_kind in {"breaker", "motor_protection", "contactor_power"}:
        if terminal == "1":
            return (x + SYMBOL_W // 2, y)
        if terminal == "2":
            return (x + SYMBOL_W // 2, y + SYMBOL_H)

    if device_kind == "transformer":
        mapping = {
            "P1": (x + 20, y),
            "P2": (x + 70, y),
            "S1": (x + 20, y + SYMBOL_H),
            "S2": (x + 70, y + SYMBOL_H),
        }
        return mapping.get(terminal)

    if device_kind in {"controller_supply", "power_supply"}:
        mapping = {
            "L": (x, y + 15),
            "N": (x, y + 45),
            "+24": (x + SYMBOL_W, y + 20),
            "0V": (x + SYMBOL_W, y + 45),
        }
        return mapping.get(terminal)

    if device_kind == "terminal_block":
        try:
            idx = int(terminal)
        except ValueError:
            idx = 1
        return (x, y + idx * 20)

    if device_kind in {"motor", "valve"}:
        mapping = {
            "L": (x, y + 15),
            "N": (x, y + 35),
            "PE": (x, y + 55),
            "24V": (x, y + 20),
            "0V": (x, y + 45),
        }
        return mapping.get(terminal)

    return (x, y)


def draw_device_label(dwg, x, y, tag, label):
    dwg.add(dwg.text(tag, insert=(x, y - 12), font_size="14px", font_weight="bold"))
    dwg.add(dwg.text(label, insert=(x, y - 2), font_size="11px"))


def draw_breaker(dwg, x, y, tag, label):
    draw_device_label(dwg, x, y, tag, label)
    dwg.add(dwg.rect((x, y), (SYMBOL_W, SYMBOL_H), fill="none", stroke="black"))
    dwg.add(dwg.line((x + SYMBOL_W // 2, y + 8), (x + SYMBOL_W // 2, y + SYMBOL_H - 8), stroke="black", stroke_width=2))


def draw_motor_protection(dwg, x, y, tag, label):
    draw_device_label(dwg, x, y, tag, label)
    dwg.add(dwg.rect((x, y), (SYMBOL_W, SYMBOL_H), fill="none", stroke="black"))
    dwg.add(dwg.text("DM", insert=(x + 28, y + 35), font_size="18px", font_weight="bold"))


def draw_contactor_power(dwg, x, y, tag, label):
    draw_device_label(dwg, x, y, tag, label)
    dwg.add(dwg.rect((x, y), (SYMBOL_W, SYMBOL_H), fill="none", stroke="black"))
    dwg.add(dwg.line((x + 25, y + 15), (x + 25, y + 45), stroke="black"))
    dwg.add(dwg.line((x + 65, y + 15), (x + 65, y + 45), stroke="black"))
    dwg.add(dwg.line((x + 25, y + 30), (x + 65, y + 30), stroke="black", stroke_width=2))


def draw_transformer(dwg, x, y, tag, label):
    draw_device_label(dwg, x, y, tag, label)
    dwg.add(dwg.rect((x, y), (SYMBOL_W, SYMBOL_H), fill="none", stroke="black"))
    dwg.add(dwg.circle(center=(x + 30, y + 30), r=12, fill="none", stroke="black"))
    dwg.add(dwg.circle(center=(x + 60, y + 30), r=12, fill="none", stroke="black"))


def draw_controller_supply(dwg, x, y, tag, label):
    draw_device_label(dwg, x, y, tag, label)
    dwg.add(dwg.rect((x, y), (SYMBOL_W, SYMBOL_H), fill="none", stroke="black"))
    dwg.add(dwg.text("MXPRO", insert=(x + 12, y + 35), font_size="14px", font_weight="bold"))


def draw_power_supply(dwg, x, y, tag, label):
    draw_device_label(dwg, x, y, tag, label)
    dwg.add(dwg.rect((x, y), (SYMBOL_W, SYMBOL_H), fill="none", stroke="black"))
    dwg.add(dwg.text("PS", insert=(x + 32, y + 35), font_size="18px", font_weight="bold"))


def draw_terminal_block(dwg, x, y, tag, label, terminals):
    draw_device_label(dwg, x, y, tag, label)
    height = max(100, len(terminals) * 20 + 10)
    dwg.add(dwg.rect((x, y), (70, height), fill="none", stroke="black"))
    for i, t in enumerate(terminals):
        ty = y + 20 + i * 20
        dwg.add(dwg.line((x, ty), (x + 70, ty), stroke="black"))
        dwg.add(dwg.text(t, insert=(x + 8, ty - 5), font_size="11px"))


def draw_motor(dwg, x, y, tag, label):
    draw_device_label(dwg, x, y, tag, label)
    dwg.add(dwg.circle(center=(x + 40, y + 35), r=30, fill="none", stroke="black"))
    dwg.add(dwg.text("M", insert=(x + 30, y + 42), font_size="18px", font_weight="bold"))


def draw_valve(dwg, x, y, tag, label):
    draw_device_label(dwg, x, y, tag, label)
    dwg.add(dwg.rect((x, y), (SYMBOL_W, SYMBOL_H), fill="none", stroke="black"))
    dwg.add(dwg.text("YV", insert=(x + 28, y + 35), font_size="18px", font_weight="bold"))


def draw_device(dwg, device, placed):
    x, y = placed.x, placed.y

    if device.kind == "breaker":
        draw_breaker(dwg, x, y, device.tag, device.label)
    elif device.kind == "motor_protection":
        draw_motor_protection(dwg, x, y, device.tag, device.label)
    elif device.kind == "contactor_power":
        draw_contactor_power(dwg, x, y, device.tag, device.label)
    elif device.kind == "transformer":
        draw_transformer(dwg, x, y, device.tag, device.label)
    elif device.kind == "controller_supply":
        draw_controller_supply(dwg, x, y, device.tag, device.label)
    elif device.kind == "power_supply":
        draw_power_supply(dwg, x, y, device.tag, device.label)
    elif device.kind == "terminal_block":
        draw_terminal_block(dwg, x, y, device.tag, device.label, device.terminals)
    elif device.kind == "motor":
        draw_motor(dwg, x, y, device.tag, device.label)
    elif device.kind == "valve":
        draw_valve(dwg, x, y, device.tag, device.label)
    else:
        dwg.add(dwg.rect((x, y), (SYMBOL_W, SYMBOL_H), fill="none", stroke="black"))
        draw_device_label(dwg, x, y, device.tag, device.label)


def get_ref_pos(folio: Folio, ref: str):
    device_map = {d.tag: d for d in folio.devices}

    if ref == "N:0":
        return (80, TOP_BUS_Y_N)
    if ref == "PE:0":
        return (80, TOP_BUS_Y_PE)

    if ref.startswith("FOLIO"):
        return None

    tag, terminal = split_ref(ref)
    dev = device_map[tag]
    placed = folio.layout[tag]
    return get_terminal_pos(dev.kind, placed.x, placed.y, terminal)


def draw_wire_number(dwg, x, y, wire_id):
    dwg.add(dwg.text(
        wire_id,
        insert=(x + 5, y - 5),
        font_size="11px",
        font_weight="bold"
    ))


def draw_cross_ref(dwg, x, y, text):
    dwg.add(dwg.rect((x, y - 14), (90, 20), fill="white", stroke="black"))
    dwg.add(dwg.text(text, insert=(x + 4, y), font_size="10px"))


def draw_terminal_ref(dwg, x, y, text):
    dwg.add(dwg.text(text, insert=(x + 6, y + 12), font_size="10px"))


def draw_polyline_wire(dwg, p1, p2, wire_id, terminal_block_ref=None):
    """
    Liaison orthogonale simple.
    """
    x1, y1 = p1
    x2, y2 = p2
    mx = snap((x1 + x2) // 2)

    points = [(x1, y1), (mx, y1), (mx, y2), (x2, y2)]
    dwg.add(dwg.polyline(points=points, fill="none", stroke="black", stroke_width=1.5))

    draw_wire_number(dwg, mx, y1, wire_id)

    if terminal_block_ref:
        draw_terminal_ref(dwg, mx, y2, terminal_block_ref)


def draw_wires(dwg, folio: Folio):
    for w in folio.wires:
        p1 = get_ref_pos(folio, w.from_ref)
        p2 = get_ref_pos(folio, w.to_ref)

        if w.to_ref.startswith("FOLIO") and p1:
            x, y = p1
            end = (x + 120, y)
            draw_polyline_wire(dwg, p1, end, w.wire_id, w.terminal_block_ref)
            if w.cross_ref:
                draw_cross_ref(dwg, end[0] + 10, end[1], w.cross_ref)
            continue

        if p1 and p2:
            draw_polyline_wire(dwg, p1, p2, w.wire_id, w.terminal_block_ref)
            if w.cross_ref:
                mx = snap((p1[0] + p2[0]) // 2)
                my = p2[1]
                draw_cross_ref(dwg, mx + 10, my, w.cross_ref)


def draw_bus_drops(dwg, folio: Folio):
    """
    Liaisons verticales depuis les barres L/N vers certains appareils.
    """
    device_map = {d.tag: d for d in folio.devices}

    # Q1 alimenté depuis L
    q1 = folio.layout["Q1"]
    q1_top = get_terminal_pos(device_map["Q1"].kind, q1.x, q1.y, "1")
    dwg.add(dwg.line((q1_top[0], TOP_BUS_Y_L), q1_top, stroke="black", stroke_width=1.5))
    draw_wire_number(dwg, q1_top[0], TOP_BUS_Y_L, "0")

    # Petite barre N/PE repère côté gauche déjà gérée par refs N:0 et PE:0


def render_power_folio_svg() -> str:
    folio = get_reference_power_folio()
    errors = validate_power_folio(folio)
    if errors:
        raise ValueError("\n".join(errors))

    dwg = svgwrite.Drawing(size=(PAGE_W, PAGE_H))
    draw_page_frame(dwg, folio)
    draw_buses(dwg)
    draw_bus_drops(dwg, folio)

    for d in folio.devices:
        draw_device(dwg, d, folio.layout[d.tag])

    draw_wires(dwg, folio)

    return dwg.tostring()


def render_power_folio_streamlit():
    st.subheader("Folio 10 - Puissance")
    folio = get_reference_power_folio()
    errors = validate_power_folio(folio)

    if errors:
        st.error("Erreurs de validation")
        for err in errors:
            st.write(f"- {err}")
        return

    svg = render_power_folio_svg()
    st.components.v1.html(svg, height=920, scrolling=True)
