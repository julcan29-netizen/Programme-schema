import html


def esc(value: str) -> str:
    return html.escape(str(value), quote=True)


def svg_header(width: int, height: int) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {width} {height}" style="background:#fff">',
        "<style>",
        ".title{font:700 22px Arial,sans-serif; fill:#111;}",
        ".text{font:13px Arial,sans-serif; fill:#111;}",
        ".small{font:10px Arial,sans-serif; fill:#111;}",
        ".tiny{font:8px Arial,sans-serif; fill:#111;}",
        ".bold{font:700 13px Arial,sans-serif; fill:#111;}",
        ".line{stroke:#111; stroke-width:2; fill:none;}",
        ".rail{stroke:#111; stroke-width:3; fill:none;}",
        ".thin{stroke:#aaa; stroke-width:1; fill:none; stroke-dasharray:4 4;}",
        ".box{stroke:#111; stroke-width:1.8; fill:#fff;}",
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


def draw_sheet(parts: list[str], width: int, height: int, title: str, sheet_name: str) -> None:
    top = 55
    left = 40
    right = width - 40
    bottom = height - 80

    rect(parts, left, top, right - left, bottom - top, "box")
    text(parts, 50, 35, title, "title")

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

    rect(parts, 20, height - 55, width - 40, 35, "box")
    text(parts, 30, height - 33, sheet_name, "text")


def draw_breaker_3p(parts: list[str], x: int, y: int, label: str) -> None:
    for i in range(3):
        xx = x + i * 18
        line(parts, xx, y - 28, xx, y - 8)
        line(parts, xx - 6, y - 8, xx + 6, y + 8)
        line(parts, xx, y + 8, xx, y + 28)
    text(parts, x + 62, y + 4, label, "text")


def draw_switch_3p(parts: list[str], x: int, y: int, label: str) -> None:
    for i in range(3):
        xx = x + i * 18
        line(parts, xx, y - 28, xx, y + 28)
        line(parts, xx - 6, y - 10, xx + 6, y + 10)
    text(parts, x + 62, y + 4, label, "text")


def draw_contactor_3p(parts: list[str], x: int, y: int, label: str) -> None:
    for i in range(3):
        xx = x + i * 18
        line(parts, xx, y - 26, xx, y - 6)
        line(parts, xx - 8, y - 6, xx, y + 8)
        line(parts, xx, y + 8, xx, y + 26)
    text(parts, x + 62, y + 4, label, "text")


def draw_transformer(parts: list[str], x: int, y: int, label: str) -> None:
    circle(parts, x - 10, y, 12)
    circle(parts, x + 10, y, 12)
    text(parts, x + 30, y + 4, label, "text")


def draw_motor(parts: list[str], x: int, y: int, label: str) -> None:
    circle(parts, x, y, 18)
    text(parts, x - 6, y + 5, "M", "text")
    text(parts, x + 28, y + 5, label, "text")


def draw_controller(parts: list[str], x: int, y: int, w: int, h: int, label: str) -> None:
    rect(parts, x, y, w, h, "box")
    text(parts, x + 10, y + 22, label, "bold")


def draw_sensor(parts: list[str], x: int, y: int, label: str) -> None:
    circle(parts, x, y, 7)
    line(parts, x, y + 7, x, y + 22)
    text(parts, x + 14, y + 4, label, "text")


def draw_contact_no(parts: list[str], x: int, y: int, label: str) -> None:
    line(parts, x - 34, y, x - 8, y)
    line(parts, x + 8, y, x + 34, y)
    line(parts, x - 8, y - 12, x + 8, y + 12)
    text(parts, x + 42, y + 4, label, "text")


def draw_contact_nc(parts: list[str], x: int, y: int, label: str) -> None:
    line(parts, x - 34, y, x - 8, y)
    line(parts, x + 8, y, x + 34, y)
    line(parts, x - 8, y - 12, x + 8, y + 12)
    line(parts, x - 8, y + 12, x + 8, y - 12)
    text(parts, x + 42, y + 4, label, "text")


def draw_coil(parts: list[str], x: int, y: int, label: str) -> None:
    line(parts, x, y - 18, x, y - 10)
    rect(parts, x - 16, y - 10, 32, 20, "box")
    line(parts, x, y + 10, x, y + 18)
    text(parts, x + 22, y + 4, label, "text")
    text(parts, x + 2, y - 14, "A1", "tiny")
    text(parts, x + 2, y + 22, "A2", "tiny")


def draw_terminal(parts: list[str], x: int, y: int, label: str) -> None:
    line(parts, x, y - 10, x, y + 10)
    circle(parts, x, y, 4)
    text(parts, x + 10, y + 4, label, "text")
