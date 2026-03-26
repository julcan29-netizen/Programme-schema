import streamlit as st

st.set_page_config(layout="wide")

st.title("Générateur de schéma électrique")

# =========================
# ANALYSE
# =========================

st.subheader("Analyse fonctionnelle")

analyse = st.text_area(
    "",
    "Pompe, ventilation, vanne 3 voies, dégivrage naturel, consigne +4°C."
)

# =========================
# BOUTON GENERATION
# =========================

if st.button("Générer le schéma électrique"):
    st.session_state["generated"] = True

# =========================
# TABS
# =========================

tabs = st.tabs(["Résumé", "Puissance", "Commande", "Bornier", "Nomenclature"])

# =========================
# RESUME
# =========================

with tabs[0]:
    st.subheader("Résumé de fonctionnement")

    st.write("Contrôleur local détecté")
    st.write("Sondes de température détectées")
    st.write("Pompe détectée")
    st.write("Vanne 3 voies modulante détectée")
    st.write("Ventilation détectée")
    st.write("Mode dégivrage détecté")
    st.write("Consigne : +4°C")
    st.write("Marche pompe : permanente")
    st.write("Différentiel : 2 K")

# =========================
# PUISSANCE V3 PROPRE
# =========================

def svg_power():
    return """
<svg width="1100" height="620" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff">

<!-- CADRE -->
<rect x="20" y="20" width="1060" height="580" fill="none" stroke="#222" stroke-width="1.5"/>

<text x="40" y="48" font-size="22">Folio puissance</text>
<text x="40" y="75" font-size="14">COFFRET TYPE FROID MONO-VENTIL</text>

<!-- ===== POMPE ===== -->

<!-- Barres -->
<line x1="120" y1="120" x2="120" y2="520" stroke="black" stroke-width="2"/>
<line x1="140" y1="120" x2="140" y2="520" stroke="black" stroke-width="2"/>
<line x1="160" y1="120" x2="160" y2="520" stroke="black" stroke-width="2"/>

<text x="110" y="100">L1</text>
<text x="135" y="100">L2</text>
<text x="155" y="100">L3</text>

<text x="110" y="540">Pompe</text>

<!-- Q1 -->
<rect x="110" y="140" width="60" height="25" fill="none" stroke="black"/>
<text x="120" y="158">Q1</text>

<!-- DM1 -->
<rect x="110" y="180" width="60" height="25" fill="none" stroke="black"/>
<text x="115" y="198">DM1</text>

<!-- KM1 -->
<rect x="110" y="220" width="60" height="25" fill="none" stroke="black"/>
<text x="115" y="238">KM1</text>

<!-- Connexion moteur -->
<line x1="130" y1="245" x2="130" y2="290" stroke="black"/>

<!-- Moteur -->
<circle cx="140" cy="320" r="25" stroke="black" fill="none"/>
<text x="132" y="325">M</text>

<text x="115" y="360">M1 Pompe</text>

<!-- ===== VENTILATION ===== -->

<line x1="300" y1="120" x2="300" y2="520" stroke="black" stroke-width="2"/>
<line x1="320" y1="120" x2="320" y2="520" stroke="black" stroke-width="2"/>
<line x1="340" y1="120" x2="340" y2="520" stroke="black" stroke-width="2"/>

<text x="290" y="100">L1</text>
<text x="315" y="100">L2</text>
<text x="335" y="100">L3</text>

<text x="290" y="540">Ventilation</text>

<!-- QF Vent -->
<rect x="290" y="160" width="60" height="25" fill="none" stroke="black"/>
<text x="300" y="178">QF</text>

<!-- KM2 -->
<rect x="290" y="200" width="60" height="25" fill="none" stroke="black"/>
<text x="300" y="218">KM2</text>

<!-- Connexion moteur -->
<line x1="310" y1="225" x2="310" y2="290" stroke="black"/>

<!-- Moteur -->
<circle cx="320" cy="320" r="25" stroke="black" fill="none"/>
<text x="312" y="325">M</text>

<text x="290" y="360">M2 Ventil</text>

<!-- ===== TRANSFO ===== -->

<text x="520" y="100">230V / 24V</text>

<circle cx="540" cy="160" r="10" stroke="black" fill="none"/>
<circle cx="570" cy="160" r="10" stroke="black" fill="none"/>

<text x="540" y="185">T1</text>

<!-- ===== VANNE 3 VOIES ===== -->

<text x="760" y="100">Vanne 3 voies</text>

<rect x="780" y="140" width="30" height="30" fill="none" stroke="black"/>
<text x="785" y="160">PS1</text>

<line x1="795" y1="170" x2="795" y2="260" stroke="black"/>

<rect x="770" y="260" width="50" height="30" fill="none" stroke="black"/>
<text x="775" y="280">YV1</text>

<line x1="795" y1="290" x2="795" y2="330" stroke="black"/>

<!-- Terre -->
<line x1="785" y1="330" x2="805" y2="330" stroke="black"/>
<line x1="788" y1="335" x2="802" y2="335" stroke="black"/>
<line x1="792" y1="340" x2="798" y2="340" stroke="black"/>

</svg>
"""

with tabs[1]:
    st.subheader("Folio puissance")

    if "generated" in st.session_state:
        st.components.v1.html(svg_power(), height=650)

# =========================
# COMMANDE (placeholder)
# =========================

with tabs[2]:
    st.subheader("Folio commande")
    st.info("Commande V2 à venir")

# =========================
# BORNIER
# =========================

with tabs[3]:
    st.subheader("Folio bornier")

    st.table({
        "Repère": ["1", "2", "3", "4", "5", "6", "7", "8"],
        "Fonction": [
            "Sonde entrée batterie",
            "Sonde reprise",
            "Sortie 0-10V",
            "Sortie 0-10V",
            "Commande pompe",
            "Neutre",
            "Commande ventil",
            "Info dégivrage"
        ],
        "Extérieur": [
            "Champ",
            "Champ",
            "YV1",
            "YV1",
            "KM1",
            "N",
            "KM2",
            "Régulateur"
        ]
    })

# =========================
# NOMENCLATURE
# =========================

with tabs[4]:
    st.subheader("Nomenclature simplifiée")

    st.table({
        "Repère": ["Q1", "DM1", "KM1", "QF", "KM2", "T1", "YV1"],
        "Désignation": [
            "Disjoncteur pompe",
            "Relais thermique pompe",
            "Contacteur pompe",
            "Protection ventilation",
            "Contacteur ventilation",
            "Transformateur",
            "Vanne 3 voies"
        ],
        "Qté": [1,1,1,1,1,1,1]
    })
