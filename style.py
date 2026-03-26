import html


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def svg_header(width: int, height: int) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {width} {height}" style="background:#fff">',
        "<style>",
        ".t{font:14px Arial,sans-serif; fill:#111;}",
        ".ts{font:11px Arial,sans-serif; fill:#111;}",
        ".tb{font:700 20px Arial,sans-serif; fill:#111;}",
        ".line{stroke:#111; stroke-width:2; fill:none;}",
        ".rail{stroke:#111; stroke-width:3; fill:none;}",
        ".thin{stroke:#bbb; stroke-width:1; fill:none; stroke-dasharray:4 4;}",
        ".box{stroke:#111; stroke-width:2; fill:#fff;}",
        ".node{stroke:#111; stroke-width:1.5; fill:#fff;}",
        "</style>",
    ]


def svg_footer(parts: list[str]) -> str:
    parts.append("</svg>")
    return "\n".join(parts)


def line(parts: list[str], x1: int, y1: int, x2: int, y2: int, klass: str = "line") -> None:
    parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{klass}"/>')


def rect(parts: list[str], x: int, y: int, w: int, h: int, klass: str = "box") -> None:
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="{klass}"/>')


def circle(parts: list[str], x: int, y: int, r: int, klass: str = "node") -> None:
    parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" class="{klass}"/>')


def text(parts: list[str], x: int, y: int, value: str, klass: str = "t") -> None:
    parts.append(f'<text x="{x}" y="{y}" class="{klass}">{esc(value)}</text>')


def draw_page(parts: list[str], width: int, height: int, title: str) -> None:
    top = 55
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

    rect(parts, 20, height - 55, width - 40, 35, "box")
    text(parts, 30, height - 32, title, "t")


def draw_breaker_3p(parts: list[str], x: int, y: int, label: str) -> None:
    for i in range(3):
        xx = x + i * 18
        line(parts, xx, y - 30, xx, y - 8)
        line(parts, xx - 6, y - 8, xx + 6, y + 8)
        line(parts, xx, y + 8, xx, y + 30)
    text(parts, x + 65, y + 5, label, "t")


def draw_contactor_3p(parts: list[str], x: int, y: int, label: str) -> None:
    for i in range(3):
        xx = x + i * 18
        line(parts, xx, y - 28, xx, y - 6)
        line(parts, xx - 7, y - 6, xx, y + 8)
        line(parts, xx, y + 8, xx, y + 28)
    text(parts, x + 65, y + 5, label, "t")


def draw_motor(parts: list[str], x: int, y: int, label: str) -> None:
    circle(parts, x, y, 18)
    text(parts, x - 6, y + 5, "M", "t")
    text(parts, x + 28, y + 5, label, "t")


def draw_psu(parts: list[str], x: int, y: int, label: str) -> None:
    rect(parts, x - 18, y - 18, 36, 36)
    text(parts, x - 12, y + 5, "PS", "t")
    text(parts, x + 28, y + 5, label, "t")


def draw_valve_actuator(parts: list[str], x: int, y: int, label: str) -> None:
    rect(parts, x - 16, y - 16, 32, 32)
    line(parts, x, y + 16, x, y + 38)
    parts.append(f'<polygon points="{x-12},{y+38} {x+12},{y+38} {x},{y+52}" class="box"/>')
    text(parts, x + 26, y + 5, label, "t")


def draw_controller(parts: list[str], x: int, y: int, label: str) -> None:
    rect(parts, x - 42, y - 22, 84, 44)
    text(parts, x - 18, y + 5, "REG", "t")
    text(parts, x + 50, y + 5, label, "t")


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
