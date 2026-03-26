import re
import html
import streamlit as st
import streamlit.components.v1 as components


def has_any(text: str, patterns: list[str]) -> bool:
    return any(p in text for p in patterns)


def extract_setpoint(text: str) -> str | None:
    patterns = [
        r"consigne[^0-9+-]*([+-]?\d+)\s*°?\s*c",
        r"point de consigne[^0-9+-]*([+-]?\d+)\s*°?\s*c",
        r"à\s*([+-]?\d+)\s*°?\s*c",
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            return f"{m.group(1)}°C"
    return None


def extract_threshold(text: str, keyword: str) -> str | None:
    patterns = [
        rf"{keyword}[^0-9+-]*([+-]?\d+)\s*°?\s*c",
        rf"{keyword}\s*:\s*température\s*[<>]=?\s*([+-]?\d+)\s*°?\s*c",
        rf"{keyword}\s*:\s*t[^0-9+-]*([+-]?\d+)\s*°?\s*c",
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            return f"{m.group(1)}°C"
    return None


def parse_analysis(text: str) -> dict:
    t = text.lower()

    data = {
        "has_controller": has_any(t, ["contrôleur", "controleur", "régulateur", "regulateur"]),
        "has_temp_sensor": has_any(t, ["sonde", "température", "temperature"]),
        "has_pump": "pompe" in t,
        "has_3way_valve": has_any(t, ["vanne 3 voies", "vanne 3 voies motorisée", "vanne 3 voies modulante"]),
        "has_valve": "vanne" in t,
        "has_fan": has_any(t, ["ventilation", "ventilateur"]),
        "has_defrost": has_any(t, ["dégivrage", "degivrage"]),
        "has_bypass": has_any(t, ["by-pass", "bypass", "boucle de dérivation", "boucle de derivation"]),
        "has_glycol": has_any(t, ["glycol", "glycolée", "glycolee", "eau glycolée", "eau glycolee"]),
        "has_evaporator": has_any(t, ["évaporateur", "evaporateur", "batterie froide"]),
        "is_onoff": has_any(t, ["on/off", "tout ou rien"]),
        "is_pid": has_any(t, ["pid", "modul", "0-10v", "0/10v"]),
        "permanent_fan": "ventilation permanente" in t,
        "local_adjustment": has_any(t, ["ajustés localement", "ajustes localement", "localement si nécessaire", "localement si necessaire"]),
    }

    data["setpoint"] = extract_setpoint(t)
    data["pump_on"] = extract_threshold(t, "marche")
    data["pump_off"] = extract_threshold(t, "arrêt") or extract_threshold(t, "arret")

    if "différentiel" in t or "differentiel" in t:
        m = re.search(r"(différentiel|differentiel)[^0-9]*([0-9]+)\s*k", t)
        data["differential"] = f"{m.group(2)}K" if m else None
    else:
        data["differential"] = None

    return data


def build_overview_mermaid(data: dict) -> str:
    lines = [
        "flowchart TD",
        "A[Analyse fonctionnelle]",
    ]

    if data["has_controller"]:
        lines += ["REG[Contrôleur local]", "A --> REG"]

    if data["has_temp_sensor"]:
        lines += ["TT1[Sonde entrée frigorifère]", "TT2[Sonde reprise]"]
        if data["has_controller"]:
            lines += ["TT1 --> REG", "TT2 --> REG"]

    if data["has_3way_valve"]:
        lines += ["V3V[Vanne 3 voies modulante]"]
        if data["has_controller"]:
            lines += ["REG -->|0-10V| V3V"]
    elif data["has_valve"]:
        lines += ["V1[Vanne]"]
        if data["has_controller"]:
            lines += ["REG --> V1"]

    if data["has_pump"]:
        lines += ["P1[Pompe de circulation]"]
        if data["has_controller"]:
            lines += ["REG -->|Marche / Arrêt| P1"]

    if data["has_glycol"]:
        lines += ["GLYCOL[Boucle eau glycolée]"]
        if data["has_pump"]:
            lines += ["P1 --> GLYCOL"]
        if data["has_3way_valve"]:
            lines += ["V3V --> GLYCOL"]

    if data["has_bypass"]:
        lines += ["BP[By-pass]"]
        if data["has_3way_valve"]:
            lines += ["V3V --> BP"]

    if data["has_evaporator"]:
        lines += ["EVAP[Évaporateur / Batterie froide]"]
        if data["has_pump"]:
            lines += ["P1 --> EVAP"]

    if data["has_fan"]:
        lines += ["FAN[Ventilation]"]
        if data["has_evaporator"]:
            lines += ["FAN --> EVAP"]
        else:
            lines += ["A --> FAN"]

    if data["has_defrost"]:
        lines += ["DEG[Mode dégivrage]"]
        if data["has_controller"]:
            lines += ["REG --> DEG"]
        if data["has_pump"]:
            lines += ["DEG -->|Arrêt| P1"]
        if data["has_3way_valve"]:
            lines += ["DEG -->|100% by-pass| V3V"]
        if data["has_fan"]:
            lines += ["DEG -->|Maintien marche| FAN"]

    if data["setpoint"]:
        lines += [f"SP[Consigne {data['setpoint']}]", "SP --> REG"]

    return "\n".join(lines)


def build_function_mermaid(data: dict) -> str:
    lines = [
        "flowchart TD",
        "START[Température mesurée]",
    ]

    if data["has_temp_sensor"]:
        lines += ["TT2[Sonde reprise]", "TT1[Sonde entrée frigorifère]", "TT2 --> START", "TT1 --> START"]

    if data["pump_on"] or data["pump_off"]:
        on_txt = data["pump_on"] or "seuil marche"
        off_txt = data["pump_off"] or "seuil arrêt"
        lines += [
            f"D1{{T reprise >= {on_txt} ?}}",
            "START --> D1",
            "PON[Pompe ON]",
            f"D2{{T reprise <= {off_txt} ?}}",
            "D1 -->|Oui| PON",
            "D1 -->|Non| D2",
            "POFF[Pompe OFF]",
            "D2 -->|Oui| POFF",
        ]

    if data["has_3way_valve"]:
        reg_type = "PID / modulation 0-10V" if data["is_pid"] else "Régulation"
        sp = data["setpoint"] or "consigne"
        lines += [
            f"REG[{reg_type}]",
            f"SP[Consigne {sp}]",
            "START --> REG",
            "SP --> REG",
            "V3V[Vanne 3 voies modulante]",
            "REG --> V3V",
        ]

    if data["has_defrost"]:
        lines += [
            "DEG[Dégivrage naturel]",
            "BYP[By-pass 100%]",
            "DEG --> BYP",
        ]
        if data["has_pump"]:
            lines += ["DEG --> POFF"]
        if data["has_fan"]:
            lines += ["FANON[Ventilation maintenue]", "DEG --> FANON"]

    return "\n".join(lines)


def build_power_mermaid(data: dict) -> str:
    lines = [
        "flowchart LR",
        "ALIM[Alimentation]",
    ]

    if data["has_pump"]:
        lines += ["QF1[Protection pompe]", "KM1[Commande pompe]", "M1[Moteur pompe]", "ALIM --> QF1 --> KM1 --> M1"]

    if data["has_fan"]:
        lines += ["QF2[Protection ventilation]", "MV1[Moteur ventilation]", "ALIM --> QF2 --> MV1"]

    if data["has_3way_valve"]:
        lines += ["PS1[Alim régulation]", "YV1[Actionneur vanne 3 voies]", "ALIM --> PS1 --> YV1"]

    return "\n".join(lines)


def build_control_mermaid(data: dict) -> str:
    lines = [
        "flowchart LR",
    ]

    if data["has_controller"]:
        lines += ["REG[Contrôleur local]"]

    if data["has_temp_sensor"]:
        lines += ["TT1[Sonde entrée]", "TT2[Sonde reprise]", "TT1 --> REG", "TT2 --> REG"]

    if data["has_pump"]:
        lines += ["KM1[Relais / contacteur pompe]", "REG -->|Marche / Arrêt| KM1"]

    if data["has_3way_valve"]:
        lines += ["YV1[Actionneur vanne 0-10V]", "REG -->|0-10V| YV1"]

    if data["has_defrost"]:
        lines += ["DEG[Horloge / cycle dégivrage]", "DEG --> REG"]

    if data["has_fan"] and data["permanent_fan"]:
        lines += ["FANP[Ventilation permanente]"]

    return "\n".join(lines)


def render_mermaid(mermaid_code: str, height: int = 700) -> None:
    safe_code = html.escape(mermaid_code)
    html_code = f"""
    <html>
    <head>
      <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ startOnLoad: true, theme: 'dark' }});
      </script>
      <style>
        body {{
          margin: 0;
          background: transparent;
          color: white;
          font-family: Arial, sans-serif;
        }}
        .wrap {{
          padding: 8px;
          overflow: auto;
        }}
      </style>
    </head>
    <body>
      <div class="wrap">
        <pre class="mermaid">{safe_code}</pre>
      </div>
    </body>
    </html>
    """
    components.html(html_code, height=height, scrolling=True)


st.set_page_config(page_title="Générateur de schéma métier", layout="wide")
st.title("Générateur de schéma métier")
st.caption("Analyse fonctionnelle → vue globale, logique, puissance, commande.")

default_text = """Un contrôleur de boucle, associé à une sonde de température du retour ou de la reprise, permet de moduler l’ouverture d’une vanne 3 voies motorisée en fonction de la température mesurée à l’entrée frigorifère.
La pompe de circulation, à débit fixe, alimente le circuit en eau glycolée froide.
La vanne 3 voies modulante, installée sur le retour du circuit frigorifique, ajuste le mélange entre le retour du fluide et la boucle de dérivation selon le besoin en froid.
La pompe est commandée par la sonde de reprise :
• Marche : température ≥ 12 °C
• Arrêt : température ≤ 10 °C
• Différentiel : 2 K
Ventilation permanente.
Mode dégivrage naturel :
• La pompe de circulation est arrêtée.
• La vanne 3 voies est placée en by-pass 100 %.
• La ventilation continue de fonctionner.
Point de consigne vanne modulante : +4 °C."""

analysis_text = st.text_area("Décris ton installation", value=default_text, height=320)

if st.button("Générer"):
    data = parse_analysis(analysis_text)

    overview = build_overview_mermaid(data)
    function = build_function_mermaid(data)
    power = build_power_mermaid(data)
    control = build_control_mermaid(data)

    st.subheader("Résumé détecté")
    st.json(data)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Vue globale", "Logique de fonctionnement", "Puissance", "Commande", "Code Mermaid"]
    )

    with tab1:
        st.subheader("Vue globale")
        render_mermaid(overview, 720)

    with tab2:
        st.subheader("Logique de fonctionnement")
        render_mermaid(function, 760)

    with tab3:
        st.subheader("Puissance")
        render_mermaid(power, 520)

    with tab4:
        st.subheader("Commande")
        render_mermaid(control, 520)

    with tab5:
        st.subheader("Code Mermaid")
        st.markdown("### Vue globale")
        st.code(overview, language="text")
        st.markdown("### Logique de fonctionnement")
        st.code(function, language="text")
        st.markdown("### Puissance")
        st.code(power, language="text")
        st.markdown("### Commande")
        st.code(control, language="text")
