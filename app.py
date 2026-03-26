import streamlit as st

st.set_page_config(page_title="Schéma coffret", layout="wide")

st.title("Générateur de schéma électrique")

# -----------------------
# Données par défaut
# -----------------------
data = {
    "has_controller": True,
    "has_temp_sensor": True,
    "has_pump": True,
    "has_3way_valve": True,
    "has_fan": True,
    "has_defrost": True,
    "setpoint": "+4°C",
    "pump_on": "≥ 12°C",
    "pump_off": "≤ 10°C",
    "differential": "2 K",
}

# -----------------------
# Résumé
# -----------------------
def build_summary_text(data):
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

    lines.append("Consigne : " + data["setpoint"])
    lines.append("Marche pompe : " + data["pump_on"])
    lines.append("Arrêt pompe : " + data["pump_off"])
    lines.append("Différentiel : " + data["differential"])

    return "\n".join(lines)

# -----------------------
# Affichage
# -----------------------
st.subheader("Résumé de fonctionnement")
st.text(build_summary_text(data))

# -----------------------
# Bouton test
# -----------------------
if st.button("Générer le schéma électrique"):
    st.success("Schéma généré (simulation OK)")

st.subheader("Folio puissance")

if st.button("Afficher folio puissance"):

    svg = """
    <svg width="800" height="500" xmlns="http://www.w3.org/2000/svg">

    <line x1="80" y1="50" x2="80" y2="420" stroke="white" stroke-width="3"/>
    <text x="70" y="40" fill="white">L</text>

    <line x1="160" y1="50" x2="160" y2="420" stroke="white" stroke-width="3"/>
    <text x="150" y="40" fill="white">N</text>

    <rect x="80" y="120" width="80" height="50" stroke="white" fill="none"/>
    <text x="105" y="150" fill="white">Q1</text>

    <rect x="80" y="190" width="80" height="50" stroke="white" fill="none"/>
    <text x="90" y="220" fill="white">DM1</text>

    <rect x="80" y="260" width="80" height="50" stroke="white" fill="none"/>
    <text x="95" y="290" fill="white">KM1</text>

    <line x1="120" y1="310" x2="120" y2="350" stroke="white" stroke-width="3"/>

    <circle cx="120" cy="390" r="30" stroke="white" fill="none"/>
    <text x="110" y="395" fill="white">M</text>

    </svg>
    """

    st.components.v1.html(svg, height=520)
