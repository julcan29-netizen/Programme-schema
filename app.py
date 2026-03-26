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
<svg width="1000" height="600" xmlns="http://www.w3.org/2000/svg">

<!-- CADRE -->
<rect x="10" y="10" width="980" height="580" stroke="white" fill="none"/>

<!-- TITRE -->
<text x="30" y="40" fill="white" font-size="20">FOLIO PUISSANCE</text>

<!-- ===== DÉPART POMPE ===== -->

<!-- Barres -->
<line x1="150" y1="80" x2="150" y2="500" stroke="white" stroke-width="4"/>
<text x="140" y="70" fill="white">L</text>

<line x1="250" y1="80" x2="250" y2="500" stroke="white" stroke-width="4"/>
<text x="240" y="70" fill="white">N</text>

<!-- Titre départ -->
<text x="160" y="100" fill="white">Pompe</text>

<!-- Q1 -->
<rect x="150" y="120" width="100" height="50" stroke="white" fill="none"/>
<text x="185" y="150" fill="white">Q1</text>

<!-- DM1 -->
<rect x="150" y="190" width="100" height="50" stroke="white" fill="none"/>
<text x="175" y="220" fill="white">DM1</text>

<!-- KM1 -->
<rect x="150" y="260" width="100" height="50" stroke="white" fill="none"/>
<text x="170" y="290" fill="white">KM1</text>

<!-- Liaison -->
<line x1="200" y1="310" x2="200" y2="360" stroke="white" stroke-width="3"/>

<!-- Moteur -->
<circle cx="200" cy="420" r="35" stroke="white" fill="none"/>
<text x="190" y="425" fill="white">M</text>

<!-- ===== DÉPART VENTILATION ===== -->

<!-- Barres -->
<line x1="450" y1="80" x2="450" y2="500" stroke="white" stroke-width="4"/>
<text x="440" y="70" fill="white">L</text>

<line x1="550" y1="80" x2="550" y2="500" stroke="white" stroke-width="4"/>
<text x="540" y="70" fill="white">N</text>

<!-- Titre -->
<text x="450" y="100" fill="white">Ventilation</text>

<!-- Q2 -->
<rect x="450" y="120" width="100" height="50" stroke="white" fill="none"/>
<text x="485" y="150" fill="white">Q2</text>

<!-- KM2 -->
<rect x="450" y="200" width="100" height="50" stroke="white" fill="none"/>
<text x="480" y="230" fill="white">KM2</text>

<!-- Liaison -->
<line x1="500" y1="250" x2="500" y2="300" stroke="white" stroke-width="3"/>

<!-- Moteur ventil -->
<circle cx="500" cy="350" r="30" stroke="white" fill="none"/>
<text x="490" y="355" fill="white">V</text>

<!-- ===== CARTOUCHE ===== -->
<rect x="10" y="520" width="980" height="70" stroke="white" fill="none"/>
<text x="30" y="550" fill="white">Coffret type froid mono-ventil</text>
<text x="780" y="550" fill="white">Folio : 10</text>

</svg>
"""

    st.components.v1.html(svg, height=520)
