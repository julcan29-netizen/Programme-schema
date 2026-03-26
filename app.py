import streamlit as st

# =========================
# SVG PUISSANCE
# =========================
def build_power_svg():
    parts = []

    parts.append('<svg width="900" height="500" style="background-color:black">')

    # Titre
    parts.append('<text x="20" y="30" fill="white" font-size="20">FOLIO PUISSANCE</text>')

    # ===== BARRE ALIMENTATION =====
    parts.append('<line x1="180" y1="80" x2="580" y2="80" stroke="white" stroke-width="3"/>')

    # ===== POMPE =====
    # Descente
    parts.append('<line x1="200" y1="80" x2="200" y2="120" stroke="white"/>')
    parts.append('<line x1="260" y1="80" x2="260" y2="120" stroke="white"/>')

    # Colonnes
    parts.append('<line x1="200" y1="120" x2="200" y2="400" stroke="white" stroke-width="3"/>')
    parts.append('<line x1="260" y1="120" x2="260" y2="400" stroke="white" stroke-width="3"/>')

    # Labels
    parts.append('<text x="195" y="115" fill="white">L</text>')
    parts.append('<text x="255" y="115" fill="white">N</text>')
    parts.append('<text x="205" y="100" fill="white">Pompe</text>')

    # Q1
    parts.append('<rect x="200" y="140" width="60" height="30" stroke="white" fill="none"/>')
    parts.append('<text x="220" y="160" fill="white">Q1</text>')

    # DM1
    parts.append('<rect x="200" y="190" width="60" height="30" stroke="white" fill="none"/>')
    parts.append('<text x="215" y="210" fill="white">DM1</text>')

    # KM1
    parts.append('<rect x="200" y="240" width="60" height="30" stroke="white" fill="none"/>')
    parts.append('<text x="215" y="260" fill="white">KM1</text>')

    # Liaison moteur
    parts.append('<line x1="230" y1="270" x2="230" y2="310" stroke="white"/>')

    # Moteur
    parts.append('<circle cx="230" cy="350" r="30" stroke="white" fill="none"/>')
    parts.append('<text x="222" y="355" fill="white">M</text>')

    # ===== VENTILATION =====
    # Descente
    parts.append('<line x1="500" y1="80" x2="500" y2="120" stroke="white"/>')
    parts.append('<line x1="560" y1="80" x2="560" y2="120" stroke="white"/>')

    # Colonnes
    parts.append('<line x1="500" y1="120" x2="500" y2="400" stroke="white" stroke-width="3"/>')
    parts.append('<line x1="560" y1="120" x2="560" y2="400" stroke="white" stroke-width="3"/>')

    # Labels
    parts.append('<text x="495" y="115" fill="white">L</text>')
    parts.append('<text x="555" y="115" fill="white">N</text>')
    parts.append('<text x="505" y="100" fill="white">Ventilation</text>')

    # Q2
    parts.append('<rect x="500" y="140" width="60" height="30" stroke="white" fill="none"/>')
    parts.append('<text x="520" y="160" fill="white">Q2</text>')

    # KM2
    parts.append('<rect x="500" y="200" width="60" height="30" stroke="white" fill="none"/>')
    parts.append('<text x="515" y="220" fill="white">KM2</text>')

    # Liaison ventilo
    parts.append('<line x1="530" y1="230" x2="530" y2="300" stroke="white"/>')

    # Ventilateur
    parts.append('<circle cx="530" cy="340" r="30" stroke="white" fill="none"/>')
    parts.append('<text x="522" y="345" fill="white">V</text>')

    parts.append('</svg>')

    return "".join(parts)


# =========================
# UI STREAMLIT
# =========================

st.title("Générateur de schéma électrique")

st.subheader("Résumé de fonctionnement")

st.write("Contrôleur local détecté")
st.write("Sondes de température détectées")
st.write("Pompe détectée")
st.write("Vanne 3 voies modulante détectée")
st.write("Ventilation détectée")
st.write("Mode dégivrage détecté")

st.write("Consigne : +4°C")
st.write("Marche pompe : ≥ 12°C")
st.write("Arrêt pompe : ≤ 10°C")
st.write("Différentiel : 2 K")

if st.button("Générer le schéma électrique"):
    st.success("Schéma généré (simulation OK)")

# ===== FOLIO PUISSANCE =====
st.subheader("Folio puissance")

if st.button("Afficher folio puissance"):
    svg = build_power_svg()
    st.components.v1.html(svg, height=500)
