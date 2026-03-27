# folio_power.py
import svgwrite
import streamlit as st

from model import Folio, split_ref
from reference_case import get_reference_power_folio
from validators import validate_power_folio


PAGE_W = 1700
PAGE_H = 1100

GRID = 20

TOP_BUS_Y_L = 110
TOP_BUS_Y_N = 145
TOP_BUS_Y_PE = 180

SYMBOL_W = 90
SYMBOL_H = 90

COLUMN_X = {
    "power_in": 220,
    "transformer": 520,
    "control_power": 790,
    "motor_power": 1110,
    "field": 1360,
    "field_far": 1520,
}


def snap(v: int) -> int:
    return round(v / GRID) * GRID


def junction(dwg, x, y):
    dwg.add(dwg.circle(center=(x, y), r=4, fill="black"))


def draw_page_frame(dwg: svgwrite.Drawing, folio: Folio):
    dwg.add(dwg.rect(insert=(15, 15), size=(PAGE_W - 30, PAGE_H - 30),
                     fill="white", stroke="black", stroke_width=1.5))

    # Zone intérieure
    dwg.add(dwg.rect(insert=(30, 30), size=(PAGE_W - 60, PAGE_H - 140),
                     fill="none", stroke="black", stroke_width=1))

    # Grille horizontale numérotée
    start_x = 30
    cell_w = (PAGE_W - 60) / 20
    for i in range(21):
        x = start_x + i * cell_w
        dwg.add(dwg.line((x, 30), (x, 50), stroke="black", stroke_width=1))
        if i < 20:
            dwg.add(dwg.text(str(i + 1), insert=(x + cell_w / 2 - 5, 45), font_size="12px"))

    dwg.add(dwg.text(f"{folio.title}", insert=(80, 85), font_size="28px", font_weight="bold"))

    # Cartouche simple
    cart_x = PAGE_W - 520
    cart_y = PAGE_H - 95
    dwg.add(dwg.rect((cart_x, cart_y), (480, 60), fill="none", stroke="black"))
    dwg.add(dwg.line((cart_x + 330, cart_y), (cart_x + 330, cart_y + 60), stroke="black"))
    dwg.add(dwg.text("Cuisine centrale", insert=(cart_x + 20, cart_y + 25), font_size="16px"))
    dwg.add(dwg.text("PUISSANCE", insert=(cart_x + 20, cart_y + 48), font_size="16px", font_weight="bold"))
    dwg.add(dwg.text("FOLIO", insert=(cart_x + 360, cart_y + 22), font_size="12px"))
    dwg.add(dwg.text(str(folio.number), insert=(cart_x + 390, cart_y + 48), font_size="22px", font_weight="bold"))


def draw_buses(dwg: svgwrite.Drawing):
    x1, x2 = 70, PAGE_W - 70
    for y, label in [(TOP_BUS_Y_L, "L"), (TOP_BUS_Y_N, "N"), (TOP_BUS_Y_PE, "PE")]:
        dwg.add(dwg.line((x1, y), (x2, y), stroke="black", stroke_width=2))
        dwg.add(dwg.text(label, insert=(45, y + 5), font_size="18px", font_weight="bold"))


def draw_device_label(dwg, x, y, tag, label, align="left"):
    if align == "center":
        dwg.add(dwg.text(tag, insert=(x + SYMBOL_W / 2, y - 24), text_anchor="middle",
                         font_size="16px", font_weight="bold"))
        dwg.add(dwg.text(label, insert=(x + SYMBOL_W / 2, y - 8), text_anchor="middle",
                         font_size="12px"))
    else:
        dwg.add(dwg.text(tag, insert=(x, y - 22), font_size="16px", font_weight="bold"))
        dwg.add(dwg.text(label, insert=(x, y - 8), font_size="12px"))


def get_terminal_pos(device_kind: str, x: int, y: int, terminal: str):
    if device_kind in {"breaker", "motor_protection", "contactor_power"}:
        if terminal == "1":
            return (x + SYMBOL_W // 2, y)
        if terminal == "2":
            return (x + SYMBOL_W // 2, y + SYMBOL_H)

    if device_kind == "transformer":
        mapping = {
            "P1": (x + 22, y),
            "P2": (x + 68, y),
            "S1": (x + 22, y + SYMBOL_H),
            "S2": (x + 68, y + SYMBOL_H),
        }
        return mapping.get(terminal)

    if device_kind in {"controller_supply", "power_supply"}:
        mapping = {
            "L": (x, y + 25),
            "N": (x, y + 65),
            "+24": (x + SYMBOL_W, y + 28),
            "0V": (x + SYMBOL_W, y + 62),
        }
        return mapping.get(terminal)

    if device_kind == "terminal_block":
        order = {"5": 0, "6": 1, "7": 2, "8": 3}
        idx = order.get(terminal, 0)
        return (x, y + 25 + idx * 35)

    if device_kind == "motor":
        mapping = {
            "L": (x, y + 18),
            "N": (x, y + 42),
            "PE": (x + 45, y + 100),
        }
        return mapping.get(terminal)

    if device_kind == "valve":
        mapping = {
            "24V": (x, y + 30),
            "0V": (x, y + 60),
        }
        return mapping.get(terminal)

    return (x, y)


def draw_breaker(dwg, x, y, tag, label):
    draw_device_label(dwg, x, y, tag, label, align="center")
    cx = x + SYMBOL_W / 2
    dwg.add(dwg.line((cx, y), (cx, y + 15), stroke="black", stroke_width=2))
    dwg.add(dwg.line((cx, y + 15), (cx + 18, y + 38), stroke="black", stroke_width=2))
    dwg.add(dwg.line((cx, y + 38), (cx, y + 38), stroke="black", stroke_width=2))
    dwg.add(dwg.line((cx, y + 38), (cx, y + SYMBOL_H), stroke="black", stroke_width=2))
    dwg.add(dwg.text("Q", insert=(x + 18, y + 54), font_size="18px", font_weight="bold"))


def draw_motor_protection(dwg, x, y, tag, label):
    draw_device_label(dwg, x, y, tag, label, align="center")
    left = x + 20
    top = y + 10
    width = 50
    height = 70
    dwg.add(dwg.rect((left, top), (width, height), fill="none", stroke="black"))
    dwg.add(dwg.line((left + 25, y), (left + 25, top), stroke="black", stroke_width=2))
    dwg.add(dwg.line((left + 25, top + height), (left + 25, y + SYMBOL_H), stroke="black", stroke_width=2))
    dwg.add(dwg.text("DM", insert=(x + 24, y + 58), font_size="18px", font_weight="bold"))


def draw_contactor_power(dwg, x, y, tag, label):
    draw_device_label(dwg, x, y, tag, label, align="center")
    cx = x + SYMBOL_W / 2
    dwg.add(dwg.line((cx, y), (cx, y + 22), stroke="black", stroke_width=2))
    dwg.add(dwg.line((cx - 18, y + 28), (cx - 18, y + 70), stroke="black"))
    dwg.add(dwg.line((cx + 18, y + 28), (cx + 18, y + 70), stroke="black"))
    dwg.add(dwg.line((cx - 18, y + 49), (cx + 18, y + 49), stroke="black", stroke_width=2))
    dwg.add(dwg.line((cx, y + 70), (cx, y + SYMBOL_H), stroke="black", stroke_width=2))


def draw_transformer(dwg, x, y, tag, label):
    draw_device_label(dwg, x, y, tag, label, align="center")
    dwg.add(dwg.line((x + 22, y), (x + 22, y + 18), stroke="black", stroke_width=2))
    dwg.add(dwg.line((x + 68, y), (x + 68, y + 18), stroke="black", stroke_width=2))
    dwg.add(dwg.circle(center=(x + 32, y + 45), r=16, fill="none", stroke="black"))
    dwg.add(dwg.circle(center=(x + 58, y + 45), r=16, fill="none", stroke="black"))
    dwg.add(dwg.line((x + 22, y + 72), (x + 22, y + SYMBOL_H), stroke="black", stroke_width=2))
    dwg.add(dwg.line((x + 68, y + 72), (x + 68, y + SYMBOL_H), stroke="black", stroke_width=2))


def draw_controller_supply(dwg, x, y, tag, label):
    draw_device_label(dwg, x, y, tag, label, align="center")
    dwg.add(dwg.rect((x, y), (SYMBOL_W, SYMBOL_H), fill="none", stroke="black"))
    dwg.add(dwg.text("MXPRO", insert=(x + 45, y + 52), text_anchor="middle",
                     font_size="18px", font_weight="bold"))


def draw_power_supply(dwg, x, y, tag, label):
    draw_device_label(dwg, x, y, tag, label, align="center")
    dwg.add(dwg.rect((x, y), (SYMBOL_W, SYMBOL_H), fill="none", stroke="black"))
    dwg.add(dwg.text("PS", insert=(x + 45, y + 52), text_anchor="middle",
                     font_size="24px", font_weight="bold"))


def draw_terminal_block(dwg, x, y, tag, label, terminals):
    draw_device_label(dwg, x, y, tag, label, align="center")
    h = 20 + len(terminals) * 35
    dwg.add(dwg.rect((x, y), (70, h), fill="none", stroke="black"))
    for i, t in enumerate(terminals):
        ty = y + 20 + i * 35
        dwg.add(dwg.line((x, ty), (x + 70, ty), stroke="black"))
        dwg.add(dwg.text(t, insert=(x + 8, ty - 8), font_size="12px"))


def draw_motor(dwg, x, y, tag, label):
    draw_device_label(dwg, x, y, tag, label, align="center")
    dwg.add(dwg.line((x, y + 18), (x + 18, y + 18), stroke="black", stroke_width=1.5))
    dwg.add(dwg.line((x, y + 42), (x + 18, y + 42), stroke="black", stroke_width=1.5))
    dwg.add(dwg.circle(center=(x + 50, y + 45), r=28, fill="none", stroke="black", stroke_width=1.5))
    dwg.add(dwg.text("M", insert=(x + 42, y + 52), font_size="20px", font_weight="bold"))
    # Terre
    gx = x + 50
    gy = y + 100
    dwg.add(dwg.line((gx, gy - 10), (gx, gy), stroke="black"))
    dwg.add(dwg.line((gx - 12, gy), (gx + 12, gy), stroke="black"))
    dwg.add(dwg.line((gx - 8, gy + 5), (gx + 8, gy + 5), stroke="black"))
    dwg.add(dwg.line((gx - 4, gy + 10), (gx + 4, gy + 10), stroke="black"))


def draw_valve(dwg, x, y, tag, label):
    draw_device_label(dwg, x, y, tag, label, align="center")
    dwg.add(dwg.rect((x, y + 8), (SYMBOL_W - 10, SYMBOL_H - 16), fill="none", stroke="black"))
    dwg.add(dwg.text("YV", insert=(x + 40, y + 55), text_anchor="middle",
                     font_size="20px", font_weight="bold"))


def draw_device(dwg, device, placed):
    x = COLUMN_X[placed.column]
    y = placed.y

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


def get_ref_pos(folio: Folio, ref: str):
    device_map = {d.tag: d for d in folio.devices}

    if ref == "N:0":
        return (70, TOP_BUS_Y_N)
    if ref == "PE:0":
        return (70, TOP_BUS_Y_PE)

    if ref.startswith("FOLIO"):
        return None

    tag, terminal = split_ref(ref)
    dev = device_map[tag]
    placed = folio.layout[tag]
    x = COLUMN_X[placed.column]
    y = placed.y
    return get_terminal_pos(dev.kind, x, y, terminal)


def draw_wire_number(dwg, x, y, wire_id):
    dwg.add(dwg.text(wire_id, insert=(x + 4, y - 6), font_size="11px", font_weight="bold"))


def draw_terminal_ref(dwg, x, y, text):
    dwg.add(dwg.text(text, insert=(x + 6, y + 14), font_size="10px"))


def draw_cross_ref(dwg, x, y, text):
    dwg.add(dwg.rect((x, y - 14), (108, 22), fill="white", stroke="black"))
    dwg.add(dwg.text(text, insert=(x + 4, y + 1), font_size="10px"))


def draw_polyline(dwg, points):
    dwg.add(dwg.polyline(points=points, fill="none", stroke="black", stroke_width=1.6))


def draw_wire_between_points(dwg, p1, p2, wire_id, terminal_block_ref=None):
    x1, y1 = p1
    x2, y2 = p2

    if x1 == x2 or y1 == y2:
        pts = [p1, p2]
        draw_polyline(dwg, pts)
        draw_wire_number(dwg, (x1 + x2) / 2, (y1 + y2) / 2, wire_id)
        if terminal_block_ref:
            draw_terminal_ref(dwg, x2, y2, terminal_block_ref)
        return

    # routage industriel simple : vertical puis horizontal
    mid1 = (x1, y2)
    pts = [p1, mid1, p2]
    draw_polyline(dwg, pts)

    # numéro sur segment horizontal final ou principal
    hx = min(x1, x2) + abs(x2 - x1) / 2
    hy = y2
    draw_wire_number(dwg, hx, hy, wire_id)

    if terminal_block_ref:
        draw_terminal_ref(dwg, x2, y2, terminal_block_ref)


def draw_bus_drop(dwg, x, y_bus, y_target, wire_id=None):
    dwg.add(dwg.line((x, y_bus), (x, y_target), stroke="black", stroke_width=1.6))
    junction(dwg, x, y_bus)
    if wire_id:
        draw_wire_number(dwg, x, y_bus, wire_id)


def draw_wires(dwg, folio: Folio):
    for w in folio.wires:
        p1 = get_ref_pos(folio, w.from_ref)
        p2 = get_ref_pos(folio, w.to_ref)

        # vers autre folio
        if w.to_ref.startswith("FOLIO") and p1:
            x, y = p1
            end = (x + 120, y)
            draw_wire_between_points(dwg, p1, end, w.wire_id, w.terminal_block_ref)
            if w.cross_ref:
                draw_cross_ref(dwg, end[0] + 10, end[1], w.cross_ref)
            continue

        if p1 and p2:
            draw_wire_between_points(dwg, p1, p2, w.wire_id, w.terminal_block_ref)


def draw_supply_drops(dwg, folio: Folio):
    device_map = {d.tag: d for d in folio.devices}

    # Q1 sur L
    q1 = folio.layout["Q1"]
    q1_x = COLUMN_X[q1.column]
    q1_top = get_terminal_pos(device_map["Q1"].kind, q1_x, q1.y, "1")
    draw_bus_drop(dwg, q1_top[0], TOP_BUS_Y_L, q1_top[1], "0")

    # Descentes N directes pour A1/T1/PS1/X1
    n_targets = [
        get_ref_pos(folio, "A1:N"),
        get_ref_pos(folio, "T1:P2"),
        get_ref_pos(folio, "PS1:N"),
        get_ref_pos(folio, "X1:6"),
    ]
    used_x = set()
    for pt in n_targets:
        if pt and pt[0] not in used_x:
            draw_bus_drop(dwg, pt[0], TOP_BUS_Y_N, pt[1])
            used_x.add(pt[0])

    # Descente PE vers moteur
    pe_target = get_ref_pos(folio, "M1:PE")
    if pe_target:
        draw_bus_drop(dwg, pe_target[0], TOP_BUS_Y_PE, pe_target[1])


def render_power_folio_svg() -> str:
    folio = get_reference_power_folio()
    errors = validate_power_folio(folio)
    if errors:
        raise ValueError("\n".join(errors))

    dwg = svgwrite.Drawing(size=(PAGE_W, PAGE_H))
    draw_page_frame(dwg, folio)
    draw_buses(dwg)
    draw_supply_drops(dwg, folio)

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
    st.components.v1.html(svg, height=1120, scrolling=True)
