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
    <svg width="800" height="400" xmlns="http://www.w3.org/2000/svg">

    <!-- Alimentation -->
    <line x1="50" y1="50" x2="50" y2="300" stroke="white" stroke-width="2"/>
    <text x="40" y="40" fill="white">L</text>

    <line x1="100" y1="50" x2="100" y2="300" stroke="white" stroke-width="2"/>
    <text x="90" y="40" fill="white">N</text>

    <!-- Disjoncteur -->
    <rect x="50" y="100" width="50" height="40" stroke="white" fill="none"/>
    <text x="60" y="125" fill="white">Q1</text>

    <!-- Moteur pompe -->
    <circle cx="75" cy="220" r="25" stroke="white" fill="none"/>
    <text x="65" y="225" fill="white">M</text>

    <!-- Liaison -->
    <line x1="75" y1="140" x2="75" y2="195" stroke="white" stroke-width="2"/>

    </svg>
    """

    st.components.v1.html(svg, height=420)
