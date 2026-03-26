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
<svg width="1100" height="650" xmlns="http://www.w3.org/2000/svg">

<!-- CADRE -->
<rect x="10" y="10" width="1080" height="630" stroke="white" fill="none"/>

<!-- TITRE -->
<text x="30" y="40" fill="white" font-size="20">FOLIO PUISSANCE</text>

<!-- BARRE HORIZONTALE ALIM -->
<line x1="100" y1="80" x2="1000" y2="80" stroke="white" stroke-width="3"/>

<!-- ===== DÉPART POMPE ===== -->
<text x="180" y="110" fill="white">Pompe</text>

<!-- L N -->
<line x1="180" y1="120" x2="180" y2="520" stroke="white" stroke-width="4"/>
<line x1="260" y1="120" x2="260" y2="520" stroke="white" stroke-width="4"/>

<text x="170" y="110" fill="white">L</text>
<text x="250" y="110" fill="white">N</text>

<!-- Liaison haut -->
<line x1="180" y1="80" x2="180" y2="120" stroke="white"/>
<line x1="260" y1="80" x2="260" y2="120" stroke="white"/>

<!-- Q1 -->
<rect x="180" y="150" width="80" height="40" stroke="white" fill="none"/>
<text x="205" y="175" fill="white">Q1</text>

<!-- DM1 -->
<rect x="180" y="210" width="80" height="40" stroke="white" fill="none"/>
<text x="195" y="235" fill="white">DM1</text>

<!-- KM1 -->
<rect x="180" y="270" width="80" height="40" stroke="white" fill="none"/>
<text x="195" y="295" fill="white">KM1</text>

<!-- descente -->
<line x1="220" y1="310" x2="220" y2="360" stroke="white" stroke-width="3"/>

<!-- moteur -->
<circle cx="220" cy="420" r="35" stroke="white" fill="none"/>
<text x="210" y="425" fill="white">M</text>


<!-- ===== DÉPART VENTIL ===== -->
<text x="500" y="110" fill="white">Ventilation</text>

<!-- L N -->
<line x1="500" y1="120" x2="500" y2="520" stroke="white" stroke-width="4"/>
<line x1="580" y1="120" x2="580" y2="520" stroke="white" stroke-width="4"/>

<text x="490" y="110" fill="white">L</text>
<text x="570" y="110" fill="white">N</text>

<!-- Liaison haut -->
<line x1="500" y1="80" x2="500" y2="120" stroke="white"/>
<line x1="580" y1="80" x2="580" y2="120" stroke="white"/>

<!-- Q2 -->
<rect x="500" y="150" width="80" height="40" stroke="white" fill="none"/>
<text x="525" y="175" fill="white">Q2</text>

<!-- KM2 -->
<rect x="500" y="230" width="80" height="40" stroke="white" fill="none"/>
<text x="520" y="255" fill="white">KM2</text>

<!-- descente -->
<line x1="540" y1="270" x2="540" y2="320" stroke="white" stroke-width="3"/>

<!-- ventil -->
<circle cx="540" cy="370" r="30" stroke="white" fill="none"/>
<text x="530" y="375" fill="white">V</text>


<!-- ===== CARTOUCHE ===== -->
<rect x="10" y="560" width="1080" height="70" stroke="white" fill="none"/>
<text x="30" y="600" fill="white">Coffret froid mono-ventil</text>
<text x="900" y="600" fill="white">Folio : 10</text>

</svg>
"""

    st.components.v1.html(svg, height=520)
