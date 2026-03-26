import streamlit as st
import streamlit.components.v1 as components

from parser import parse_analysis
from folio_power import build_power_svg
from folio_regulation import build_regulation_svg
from folio_terminal import build_terminal_svg


def render_svg(svg_code: str, height: int) -> None:
    components.html(svg_code, height=height, scrolling=True)


def build_summary_text(data: dict) -> str:
    lines = []
    if data["has_controller"]:
        lines.append("Contrôleur local détecté")
    if data["has_temp_sensor"]:
        lines.append("Sondes de température détectées")
    if data["has_pump"]:
        lines.append("Pompe détectée")
    if data["has_3way_valve"]:
        lines.append("Vanne 3 voies modulante détectée")
    if data["has_fan"]:
        lines.append("Ventilation détectée")
    if data["has_defrost"]:
        lines.append("Mode dégivrage détecté")
    if data["setpoint"]:
        lines.append(f'Consigne détectée : {data["setpoint"]}')
    if data["pump_on"]:
        lines.append(f'Seuil marche pompe : {data["pump_on"]}')
    if data["pump_off"]:
        lines.append(f'Seuil arrêt pompe : {data["pump_off"]}')
    return "\n".join(lines) if lines else "Aucun équipement reconnu."


st.set_page_config(page_title="Générateur de schéma électrique conventionnel V8", layout="wide")

st.title("Générateur de schéma électrique conventionnel V8")
st.caption("Analyse fonctionnelle → puissance + commande + bornier, style industriel simplifié.")

default_text = """Un contrôleur de boucle, associé à une sonde de température du retour ou de la reprise, permet de moduler l’ouverture d’une vanne 3 voies motorisée en fonction de la température mesurée à l’entrée frigorifère.
La pompe de circulation, à débit fixe, alimente le circuit en eau glycolée froide.
La vanne 3 voies modulante, installée sur le retour du circuit frigorifique, ajuste le mélange entre le retour du fluide et la boucle de dérivation selon le besoin en froid.
La pompe est commandée par la sonde de reprise :
• Marche : température ≥ 12 °C
• Arrêt : température ≤ 10 °C
• Différentiel : 2 K
Ventilation permanente, indépendamment du fonctionnement de la pompe et de la vanne.
Mode dégivrage naturel :
• La pompe de circulation est arrêtée.
• La vanne 3 voies est placée en by-pass 100 %.
• La ventilation continue de fonctionner.
Point de consigne vanne modulante : +4 °C."""

analysis_text = st.text_area("Décris ton installation", value=default_text, height=320)

if st.button("Générer le schéma électrique"):
    data = parse_analysis(analysis_text)

    power_svg = build_power_svg(data)
    regulation_svg = build_regulation_svg(data)
    terminal_svg = build_terminal_svg(data)

    tab1, tab2, tab3, tab4 = st.tabs(["Résumé", "Puissance", "Commande", "Bornier"])

    with tab1:
        st.subheader("Éléments détectés")
        st.text(build_summary_text(data))
        st.json(data)

    with tab2:
        st.subheader("Folio puissance")
        render_svg(power_svg, 820)

    with tab3:
        st.subheader("Folio commande")
        render_svg(regulation_svg, 820)

    with tab4:
        st.subheader("Folio bornier")
        render_svg(terminal_svg, 720)
