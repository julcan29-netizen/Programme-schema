import html

def esc(value: str) -> str:
    return html.escape(str(value), quote=True)

def svg_header(width: int, height: int) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {width} {height}" style="background:#fff">',
        "<style>",
        ".title{font:700 22px Arial;}",
        ".text{font:13px Arial;}",
        ".tiny{font:9px Arial;}",
        ".bold{font:700 13px Arial;}",
        ".line{stroke:#111; stroke-width:2;}",
        ".rail{stroke:#111; stroke-width:3;}",
        ".thin{stroke:#aaa; stroke-width:1; stroke-dasharray:4 4;}",
        ".box{stroke:#111; fill:none;}",
        "</style>",
    ]

def svg_footer(parts):
    parts.append("</svg>")
    return "\n".join(parts)

def line(p,x1,y1,x2,y2,c="line"):
    p.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{c}"/>')

def rect(p,x,y,w,h,c="box"):
    p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="{c}"/>')

def circle(p,x,y,r,c="box"):
    p.append(f'<circle cx="{x}" cy="{y}" r="{r}" class="{c}"/>')

def text(p,x,y,t,c="text"):
    p.append(f'<text x="{x}" y="{y}" class="{c}">{esc(t)}</text>')

# ===== SYMBOLS =====

def draw_breaker_3p(p,x,y,label):
    for i in range(3):
        xx=x+i*18
        line(p,xx,y-20,xx,y+20)
    text(p,x+60,y,label)

def draw_switch_3p(p,x,y,label):
    for i in range(3):
        xx=x+i*18
        line(p,xx,y-20,xx,y+20)
    text(p,x+60,y,label)

def draw_contactor_3p(p,x,y,label):
    for i in range(3):
        xx=x+i*18
        line(p,xx,y-20,xx,y+20)
    text(p,x+60,y,label)

def draw_motor(p,x,y,label):
    circle(p,x,y,15)
    text(p,x+25,y,label)

def draw_transformer(p,x,y,label):
    rect(p,x,y,30,30)
    text(p,x+40,y+15,label)

def draw_controller(p,x,y,w,h,label):
    rect(p,x,y,w,h)
    text(p,x+10,y+20,label)

def draw_sensor(p,x,y,label):
    circle(p,x,y,6)
    text(p,x+10,y,label)

def draw_contact_no(p,x,y,label):
    line(p,x-20,y,x-5,y)
    line(p,x+5,y,x+20,y)
    text(p,x+25,y,label)

def draw_contact_nc(p,x,y,label):
    line(p,x-20,y,x-5,y)
    line(p,x+5,y,x+20,y)
    line(p,x-5,y+5,x+5,y-5)
    text(p,x+25,y,label)

def draw_coil(p,x,y,label):
    rect(p,x-10,y-10,20,20)
    text(p,x+15,y,label)

def draw_terminal(p,x,y,label):
    circle(p,x,y,3)
    text(p,x+10,y,label)
