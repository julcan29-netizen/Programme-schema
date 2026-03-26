import re
import streamlit as st


def parse_analysis(text: str) -> dict:
    t = text.lower()

    data = {
        "has_pump": "pompe" in t,
        "has_3way_valve": "vanne 3 voies" in t or "vanne 3 voies motorisée" in t or "vanne 3 voies modulante" in t,
        "has_valve": "vanne" in t,
        "has_fan": "ventilation" in t or "ventilateur" in t,
        "has_controller": "contrôleur" in t or "controleur" in t or "régulateur" in t or "regulateur" in t,
        "has_temp_sensor": "sonde" in t or "température" in t or "temperature" in t,
        "has_defrost": "dégivrage" in t or "degivrage" in t,
        "has_bypass": "by-pass" in t or "bypass" in t,
        "has_glycol": "glycol" in t or "glycolée" in t or "glycolee" in t,
        "has_evaporator": "évaporateur" in t or "evaporateur" in t or "batterie froide" in t,
    }

    setpoint_match = re.search(r"\+?\s*(\d+)\s*°?\s*c", t)
    data["setpoint"] = f"{setpoint_match.group(1)}°C" if setpoint_match else None

    return data


def build_mermaid(data: dict) -> str:
    lines = [
        "flowchart TD",
        "    A[Analyse fonctionnelle]",
    ]

    if data["has_controller"]:
        lines.append("    REG[Contrôleur local]")
        lines.append("    A --> REG")

    if data["has_temp_sensor"]:
        lines.append("    TT1[Sonde entrée frigorifère]")
        lines.append("    TT2[Sonde reprise]")
        if data["has_controller"]:
            lines.append("    TT1 --> REG")
            lines.append("    TT2 --> REG")

    if data["has_3way_valve"]:
        lines.append("    V3V[Vanne 3 voies modulante]")
        if data["has_controller"]:
            lines.append("    REG -->|0-10V| V3V")
    elif data["has_valve"]:
        lines.append("    V1[Vanne]")
        if data["has_controller"]:
            lines.append("    REG --> V1")

    if data["has_pump"]:
        lines.append("    P1[Pompe de circulation]")
        if data["has_controller"]:
            lines.append("    REG -->|Marche / Arrêt| P1")

    if data["has_evaporator"]:
        lines.append("    EVAP[Évaporateur / Batterie froide]")
        if data["has_pump"]:
            lines.append("    P1 --> EVAP")

    if data["has_glycol"]:
        lines.append("    GLYCOL[Boucle eau glycolée]")
        if data["has_pump"]:
            lines.append("    P1 --> GLYCOL")
        if data["has_3way_valve"]:
            lines.append("    V3V --> GLYCOL")

    if data["has_bypass"]:
        lines.append("    BP[By-pass]")
        if data["has_3way_valve"]:
            lines.append("    V3V --> BP")

    if data["has_fan"]:
        lines.append("    FAN[Ventilation permanente]")
        if data["has_evaporator"]:
            lines.append("    FAN --> EVAP")
        else:
            lines.append("    A --> FAN")

    if data["has_defrost"]:
        lines.append("    DEG[Mode dégivrage naturel]")
        if data["has_controller"]:
            lines.append("    REG --> DEG")
        if data["has_pump"]:
            lines.append("    DEG -->|Arrêt| P1")
        if data["has_3way_valve"]:
            lines.append("    DEG -->|100% by-pass| V3V")
        if data["has_fan"]:
            lines.append("    DEG -->|Maintien marche| FAN")

    if data["setpoint"]:
        lines.append(f"    SP[Consigne {data['setpoint']}]")
        if data["has_controller"]:
            lines.append("    SP --> REG")

    return "\n".join(lines)


st.set_page_config(page_title="Analyse → Schéma", layout="wide")
st.title("Générateur de schéma métier")
st.caption("Colle une analyse fonctionnelle pour générer un schéma Mermaid.")

default_text = """Un contrôleur de boucle, associé à une sonde de température du retour ou de la reprise, permet de moduler l’ouverture d’une vanne 3 voies motorisée en fonction de la température mesurée à l’entrée frigorifère.
La pompe de circulation, à débit fixe, alimente le circuit en eau glycolée froide.
La vanne 3 voies modulante est installée sur le retour.
La pompe est commandée par la sonde de reprise.
Ventilation permanente.
Mode dégivrage naturel avec pompe arrêtée et vanne en by-pass 100 %.
Point de consigne : +4 °C."""

analysis_text = st.text_area("Décris ton installation", value=default_text, height=280)

if st.button("Générer"):
    data = parse_analysis(analysis_text)
    mermaid_code = build_mermaid(data)

    st.subheader("Code Mermaid")
    st.code(mermaid_code, language="text")

    st.subheader("Schéma")
    st.markdown(f"```mermaid\n{mermaid_code}\n```")
