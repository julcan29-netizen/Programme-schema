import streamlit as st
import streamlit.components.v1 as components

from parser import parse_analysis
from folios import (
    build_bom_svg,
    build_power_svg,
    build_regulation_svg,
    build_terminal_svg,
)


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
    lines.append(f'Consigne : {data["setpoint"]}')
    lines.append(f'Marche pompe : {data["pump_on"]}')
    lines.append(f'Arrêt pompe : {data["pump_off"]}')
    lines.append(f'Différentiel : {data["differential"]}')
    return "\n".join(lines)


st.set_page_config(page_title="Générateur de schéma électrique conventionnel V10", layout="wide")

st.title("Générateur de schéma électrique conventionnel V10")
st.caption("Template métier mono ventil / pompe / vanne 3 voies / régulateur.")

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

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Résumé", "Puissance", "Commande", "Bornier", "Nomenclature"]
    )

    with tab1:
        st.subheader("Éléments détectés")
        st.text(build_summary_text(data))
        st.json(data)

    with tab2:
        st.subheader("Folio puissance")
        render_svg(build_power_svg(data), 830)

    with tab3:
        st.subheader("Folio commande / régulation")
        render_svg(build_regulation_svg(data), 830)

    with tab4:
        st.subheader("Folio bornier")
        render_svg(build_terminal_svg(data), 760)

    with tab5:
        st.subheader("Nomenclature simplifiée")
        render_svg(build_bom_svg(data), 760)
