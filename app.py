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
<svg width="900" height="600" xmlns="http://www.w3.org/2000/svg">

<!-- ===== CADRE ===== -->
<rect x="10" y="10" width="880" height="580" stroke="white" fill="none"/>

<!-- ===== TITRE ===== -->
<text x="30" y="40" fill="white" font-size="20">FOLIO PUISSANCE</text>

<!-- ===== BARRES L / N ===== -->
<line x1="120" y1="80" x2="120" y2="500" stroke="white" stroke-width="4"/>
<text x="110" y="70" fill="white">L</text>

<line x1="220" y1="80" x2="220" y2="500" stroke="white" stroke-width="4"/>
<text x="210" y="70" fill="white">N</text>

<!-- ===== Q1 ===== -->
<rect x="120" y="120" width="100" height="50" stroke="white" fill="none"/>
<text x="155" y="150" fill="white">Q1</text>

<!-- ===== DM1 ===== -->
<rect x="120" y="190" width="100" height="50" stroke="white" fill="none"/>
<text x="145" y="220" fill="white">DM1</text>

<!-- ===== KM1 ===== -->
<rect x="120" y="260" width="100" height="50" stroke="white" fill="none"/>
<text x="140" y="290" fill="white">KM1</text>

<!-- ===== LIAISON ===== -->
<line x1="170" y1="310" x2="170" y2="360" stroke="white" stroke-width="3"/>

<!-- ===== MOTEUR ===== -->
<circle cx="170" cy="420" r="35" stroke="white" fill="none"/>
<text x="160" y="425" fill="white">M</text>

<!-- ===== CARTOUCHE BAS ===== -->
<rect x="10" y="520" width="880" height="70" stroke="white" fill="none"/>
<text x="30" y="550" fill="white">Coffret type froid mono-ventil</text>
<text x="700" y="550" fill="white">Folio : 10</text>

</svg>
"""

    st.components.v1.html(svg, height=520)
