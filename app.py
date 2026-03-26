import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Générateur de schéma électrique", layout="wide")

st.title("Génateur de schéma électrique")

st.subheader("Analyse fonctionnelle")
analyse = st.text_area(
    "",
    "Pompe, ventilation, vanne 3 voies, dégivrage naturel, consigne +4°C.",
    height=140,
)

st.button("Générer le schéma électrique")


def svg_power():
    return """
<svg width="1100" height="620" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff">

<rect x="20" y="20" width="1060" height="580" fill="none" stroke="#222" stroke-width="1.5"/>

<text x="40" y="48" font-size="22">Folio puissance</text>
<text x="40" y="78" font-size="12">COFFRET TYPE FROID MONO-VENTIL</text>
<text x="915" y="78" font-size="12">Schéma de puissance</text>

<g stroke="#d9d9d9" stroke-width="1" stroke-dasharray="4 4">
    <line x1="80" y1="95" x2="80" y2="540"/>
    <line x1="180" y1="95" x2="180" y2="540"/>
    <line x1="280" y1="95" x2="280" y2="540"/>
    <line x1="380" y1="95" x2="380" y2="540"/>
    <line x1="480" y1="95" x2="480" y2="540"/>
    <line x1="580" y1="95" x2="580" y2="540"/>
    <line x1="680" y1="95" x2="680" y2="540"/>
    <line x1="780" y1="95" x2="780" y2="540"/>
    <line x1="880" y1="95" x2="880" y2="540"/>
    <line x1="980" y1="95" x2="980" y2="540"/>

    <line x1="40" y1="120" x2="1040" y2="120"/>
    <line x1="40" y1="220" x2="1040" y2="220"/>
    <line x1="40" y1="320" x2="1040" y2="320"/>
    <line x1="40" y1="420" x2="1040" y2="420"/>
</g>

<!-- POMPE -->
<text x="92" y="108" font-size="11">L1</text>
<text x="114" y="108" font-size="11">L2</text>
<text x="136" y="108" font-size="11">L3</text>
<text x="84" y="128" font-size="12">Pompe circulation</text>

<line x1="100" y1="140" x2="100" y2="372" stroke="black" stroke-width="2"/>
<line x1="122" y1="140" x2="122" y2="372" stroke="black" stroke-width="2"/>
<line x1="144" y1="140" x2="144" y2="372" stroke="black" stroke-width="2"/>

<line x1="96" y1="158" x2="104" y2="168" stroke="black" stroke-width="1.4"/>
<line x1="118" y1="158" x2="126" y2="168" stroke="black" stroke-width="1.4"/>
<line x1="140" y1="158" x2="148" y2="168" stroke="black" stroke-width="1.4"/>
<text x="160" y="170" font-size="12">IG1</text>

<line x1="96" y1="208" x2="104" y2="218" stroke="black" stroke-width="1.4"/>
<line x1="118" y1="208" x2="126" y2="218" stroke="black" stroke-width="1.4"/>
<line x1="140" y1="208" x2="148" y2="218" stroke="black" stroke-width="1.4"/>
<text x="160" y="220" font-size="12">Q1</text>

<line x1="96" y1="258" x2="104" y2="268" stroke="black" stroke-width="1.4"/>
<line x1="118" y1="258" x2="126" y2="268" stroke="black" stroke-width="1.4"/>
<line x1="140" y1="258" x2="148" y2="268" stroke="black" stroke-width="1.4"/>
<text x="160" y="270" font-size="12">DM1</text>

<line x1="100" y1="372" x2="110" y2="372" stroke="black" stroke-width="1.5"/>
<line x1="144" y1="372" x2="134" y2="372" stroke="black" stroke-width="1.5"/>
<line x1="100" y1="408" x2="110" y2="408" stroke="black" stroke-width="1.5"/>
<line x1="144" y1="408" x2="134" y2="408" stroke="black" stroke-width="1.5"/>

<circle cx="122" cy="390" r="18" fill="none" stroke="black" stroke-width="1.5"/>
<text x="116" y="395" font-size="12">M</text>
<text x="160" y="395" font-size="12">M1 Pompe</text>

<line x1="100" y1="408" x2="100" y2="470" stroke="black" stroke-width="2"/>
<line x1="122" y1="408" x2="122" y2="470" stroke="black" stroke-width="2"/>
<line x1="144" y1="408" x2="144" y2="470" stroke="black" stroke-width="2"/>

<!-- VENTILATION -->
<text x="312" y="108" font-size="11">L1</text>
<text x="334" y="108" font-size="11">L2</text>
<text x="356" y="108" font-size="11">L3</text>
<text x="300" y="128" font-size="12">Ventilation</text>

<line x1="320" y1="140" x2="320" y2="372" stroke="black" stroke-width="2"/>
<line x1="342" y1="140" x2="342" y2="372" stroke="black" stroke-width="2"/>
<line x1="364" y1="140" x2="364" y2="372" stroke="black" stroke-width="2"/>

<line x1="316" y1="208" x2="324" y2="218" stroke="black" stroke-width="1.4"/>
<line x1="338" y1="208" x2="346" y2="218" stroke="black" stroke-width="1.4"/>
<line x1="360" y1="208" x2="368" y2="218" stroke="black" stroke-width="1.4"/>
<text x="382" y="220" font-size="12">Q2</text>

<line x1="320" y1="372" x2="330" y2="372" stroke="black" stroke-width="1.5"/>
<line x1="364" y1="372" x2="354" y2="372" stroke="black" stroke-width="1.5"/>
<line x1="320" y1="408" x2="330" y2="408" stroke="black" stroke-width="1.5"/>
<line x1="364" y1="408" x2="354" y2="408" stroke="black" stroke-width="1.5"/>

<circle cx="342" cy="390" r="18" fill="none" stroke="black" stroke-width="1.5"/>
<text x="336" y="395" font-size="12">M</text>
<text x="382" y="395" font-size="12">M2 Ventilation</text>

<line x1="320" y1="408" x2="320" y2="470" stroke="black" stroke-width="2"/>
<line x1="342" y1="408" x2="342" y2="470" stroke="black" stroke-width="2"/>
<line x1="364" y1="408" x2="364" y2="470" stroke="black" stroke-width="2"/>

<!-- TRANSFO -->
<text x="540" y="108" font-size="11">Alim commande</text>
<text x="540" y="124" font-size="10">230V / 24V</text>

<line x1="565" y1="140" x2="565" y2="165" stroke="black" stroke-width="1.5"/>
<line x1="595" y1="140" x2="595" y2="165" stroke="black" stroke-width="1.5"/>
<circle cx="557" cy="182" r="8" fill="none" stroke="black" stroke-width="1.5"/>
<circle cx="573" cy="182" r="8" fill="none" stroke="black" stroke-width="1.5"/>
<circle cx="587" cy="182" r="8" fill="none" stroke="black" stroke-width="1.5"/>
<circle cx="603" cy="182" r="8" fill="none" stroke="black" stroke-width="1.5"/>
<text x="620" y="186" font-size="12">T1</text>
<text x="550" y="205" font-size="10">primaire</text>
<text x="588" y="205" font-size="10">secondaire</text>

<line x1="587" y1="190" x2="587" y2="225" stroke="black" stroke-width="1.3"/>
<line x1="603" y1="190" x2="603" y2="225" stroke="black" stroke-width="1.3"/>
<text x="610" y="230" font-size="10">24V~ / N</text>

<!-- VANNE -->
<text x="800" y="108" font-size="11">Actionneur vanne 3 voies</text>
<text x="810" y="124" font-size="10">alimentation 24V~</text>

<line x1="840" y1="140" x2="840" y2="165" stroke="black" stroke-width="1.5"/>
<line x1="862" y1="140" x2="862" y2="165" stroke="black" stroke-width="1.5"/>
<text x="834" y="178" font-size="10">L</text>
<text x="858" y="178" font-size="10">N</text>

<rect x="836" y="188" width="30" height="18" fill="none" stroke="black" stroke-width="1.3"/>
<text x="825" y="184" font-size="11">PS1</text>

<line x1="851" y1="206" x2="851" y2="282" stroke="black" stroke-width="1.5"/>

<rect x="842" y="282" width="18" height="28" fill="none" stroke="black" stroke-width="1.3"/>
<text x="875" y="300" font-size="12">YV1</text>
<text x="875" y="316" font-size="11">Vanne 3 voies modulante</text>

<line x1="851" y1="310" x2="851" y2="326" stroke="black" stroke-width="1.5"/>
<polygon points="845,326 857,326 851,336" fill="none" stroke="black" stroke-width="1.3"/>

<!-- CARTOUCHE -->
<rect x="20" y="560" width="1060" height="30" fill="none" stroke="#222" stroke-width="1.5"/>
<line x1="985" y1="560" x2="985" y2="590" stroke="#222" stroke-width="1.5"/>
<text x="30" y="580" font-size="12">Folio puissance</text>
<text x="1000" y="580" font-size="12">10</text>

</svg>
"""


def svg_command():
    return """
<svg width="1100" height="620" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff">
<rect x="20" y="20" width="1060" height="580" fill="none" stroke="#222" stroke-width="1.5"/>
<text x="40" y="48" font-size="22">Folio commande</text>
<text x="40" y="78" font-size="12">COFFRET TYPE FROID MONO-VENTIL</text>
<text x="900" y="78" font-size="12">Schéma de commande</text>

<line x1="90" y1="120" x2="90" y2="520" stroke="black" stroke-width="2"/>
<line x1="1010" y1="120" x2="1010" y2="520" stroke="black" stroke-width="2"/>
<text x="82" y="112" font-size="11">L</text>
<text x="1002" y="112" font-size="11">N</text>

<rect x="360" y="190" width="260" height="150" fill="none" stroke="black" stroke-width="1.5"/>
<text x="380" y="220" font-size="14">A1 MPX PRO</text>
<text x="380" y="245" font-size="11">Régulation température</text>
<text x="380" y="265" font-size="11">TT1 + TT2</text>
<text x="380" y="285" font-size="11">Sortie analogique vanne</text>

<circle cx="220" cy="235" r="5" fill="none" stroke="black"/>
<text x="235" y="240" font-size="11">TT1 Entrée batterie</text>
<line x1="225" y1="235" x2="360" y2="235" stroke="black"/>

<circle cx="220" cy="295" r="5" fill="none" stroke="black"/>
<text x="235" y="300" font-size="11">TT2 Reprise</text>
<line x1="225" y1="295" x2="360" y2="295" stroke="black"/>

<line x1="620" y1="245" x2="770" y2="245" stroke="black"/>
<line x1="620" y1="275" x2="770" y2="275" stroke="black"/>
<text x="780" y="250" font-size="11">AO+</text>
<text x="780" y="280" font-size="11">AO-</text>
<text x="840" y="265" font-size="11">Vers YV1</text>

<text x="120" y="400" font-size="12">Fonctionnement</text>
<text x="140" y="430" font-size="11">• Pompe permanente</text>
<text x="140" y="450" font-size="11">• Ventilation permanente</text>
<text x="140" y="470" font-size="11">• Dégivrage naturel</text>
<text x="140" y="490" font-size="11">• Régulation sur vanne 3 voies</text>

<rect x="20" y="560" width="1060" height="30" fill="none" stroke="#222" stroke-width="1.5"/>
<line x1="985" y1="560" x2="985" y2="590" stroke="#222" stroke-width="1.5"/>
<text x="30" y="580" font-size="12">Folio commande</text>
<text x="1000" y="580" font-size="12">11</text>
</svg>
"""


def svg_bornier():
    return """
<svg width="1100" height="620" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff">
<rect x="20" y="20" width="1060" height="580" fill="none" stroke="#222" stroke-width="1.5"/>
<text x="40" y="48" font-size="22">Folio bornier</text>
<text x="70" y="110" font-size="14">Bornier X1</text>

<rect x="70" y="140" width="960" height="34" fill="none" stroke="black"/>
<line x1="150" y1="140" x2="150" y2="174" stroke="black"/>
<line x1="620" y1="140" x2="620" y2="174" stroke="black"/>
<text x="90" y="162" font-size="12">Repère</text>
<text x="190" y="162" font-size="12">Fonction</text>
<text x="700" y="162" font-size="12">Extérieur</text>

<rect x="70" y="174" width="960" height="32" fill="none" stroke="black"/><line x1="150" y1="174" x2="150" y2="206" stroke="black"/><line x1="620" y1="174" x2="620" y2="206" stroke="black"/><text x="98" y="195" font-size="11">1</text><text x="165" y="195" font-size="11">Sonde TT1 entrée batterie</text><text x="700" y="195" font-size="11">Champ</text>
<rect x="70" y="206" width="960" height="32" fill="none" stroke="black"/><line x1="150" y1="206" x2="150" y2="238" stroke="black"/><line x1="620" y1="206" x2="620" y2="238" stroke="black"/><text x="98" y="227" font-size="11">2</text><text x="165" y="227" font-size="11">Sonde TT2 reprise</text><text x="700" y="227" font-size="11">Champ</text>
<rect x="70" y="238" width="960" height="32" fill="none" stroke="black"/><line x1="150" y1="238" x2="150" y2="270" stroke="black"/><line x1="620" y1="238" x2="620" y2="270" stroke="black"/><text x="98" y="259" font-size="11">3</text><text x="165" y="259" font-size="11">Sortie AO+</text><text x="700" y="259" font-size="11">Actionneur YV1</text>
<rect x="70" y="270" width="960" height="32" fill="none" stroke="black"/><line x1="150" y1="270" x2="150" y2="302" stroke="black"/><line x1="620" y1="270" x2="620" y2="302" stroke="black"/><text x="98" y="291" font-size="11">4</text><text x="165" y="291" font-size="11">Sortie AO-</text><text x="700" y="291" font-size="11">Actionneur YV1</text>
<rect x="70" y="302" width="960" height="32" fill="none" stroke="black"/><line x1="150" y1="302" x2="150" y2="334" stroke="black"/><line x1="620" y1="302" x2="620" y2="334" stroke="black"/><text x="98" y="323" font-size="11">5</text><text x="165" y="323" font-size="11">Alimentation actionneur</text><text x="700" y="323" font-size="11">PS1 / YV1</text>
<rect x="70" y="334" width="960" height="32" fill="none" stroke="black"/><line x1="150" y1="334" x2="150" y2="366" stroke="black"/><line x1="620" y1="334" x2="620" y2="366" stroke="black"/><text x="98" y="355" font-size="11">6</text><text x="165" y="355" font-size="11">Neutre commande</text><text x="700" y="355" font-size="11">N</text>
<rect x="70" y="366" width="960" height="32" fill="none" stroke="black"/><line x1="150" y1="366" x2="150" y2="398" stroke="black"/><line x1="620" y1="366" x2="620" y2="398" stroke="black"/><text x="98" y="387" font-size="11">7</text><text x="165" y="387" font-size="11">Ventilation permanente</text><text x="700" y="387" font-size="11">Alim ventil</text>
<rect x="70" y="398" width="960" height="32" fill="none" stroke="black"/><line x1="150" y1="398" x2="150" y2="430" stroke="black"/><line x1="620" y1="398" x2="620" y2="430" stroke="black"/><text x="98" y="419" font-size="11">8</text><text x="165" y="419" font-size="11">Information dégivrage</text><text x="700" y="419" font-size="11">Entrée régulation</text>

<rect x="20" y="560" width="1060" height="30" fill="none" stroke="#222" stroke-width="1.5"/>
<line x1="985" y1="560" x2="985" y2="590" stroke="#222" stroke-width="1.5"/>
<text x="30" y="580" font-size="12">Folio bornier</text>
<text x="1000" y="580" font-size="12">12</text>
</svg>
"""


def svg_nomenclature():
    return """
<svg width="1100" height="620" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff">
<rect x="20" y="20" width="1060" height="580" fill="none" stroke="#222" stroke-width="1.5"/>
<text x="40" y="48" font-size="22">Nomenclature simplifiée</text>

<rect x="70" y="110" width="960" height="34" fill="none" stroke="black"/>
<line x1="170" y1="110" x2="170" y2="144" stroke="black"/>
<line x1="900" y1="110" x2="900" y2="144" stroke="black"/>
<text x="95" y="132" font-size="12">Repère</text>
<text x="210" y="132" font-size="12">Désignation</text>
<text x="950" y="132" font-size="12">Qté</text>

<rect x="70" y="144" width="960" height="28" fill="none" stroke="black"/><line x1="170" y1="144" x2="170" y2="172" stroke="black"/><line x1="900" y1="144" x2="900" y2="172" stroke="black"/><text x="105" y="162" font-size="11">IG1</text><text x="185" y="162" font-size="11">Interrupteur général</text><text x="965" y="162" font-size="11">1</text>
<rect x="70" y="172" width="960" height="28" fill="none" stroke="black"/><line x1="170" y1="172" x2="170" y2="200" stroke="black"/><line x1="900" y1="172" x2="900" y2="200" stroke="black"/><text x="110" y="190" font-size="11">Q1</text><text x="185" y="190" font-size="11">Protection pompe</text><text x="965" y="190" font-size="11">1</text>
<rect x="70" y="200" width="960" height="28" fill="none" stroke="black"/><line x1="170" y1="200" x2="170" y2="228" stroke="black"/><line x1="900" y1="200" x2="900" y2="228" stroke="black"/><text x="103" y="218" font-size="11">DM1</text><text x="185" y="218" font-size="11">Protection moteur pompe</text><text x="965" y="218" font-size="11">1</text>
<rect x="70" y="228" width="960" height="28" fill="none" stroke="black"/><line x1="170" y1="228" x2="170" y2="256" stroke="black"/><line x1="900" y1="228" x2="900" y2="256" stroke="black"/><text x="110" y="246" font-size="11">Q2</text><text x="185" y="246" font-size="11">Protection ventilation</text><text x="965" y="246" font-size="11">1</text>
<rect x="70" y="256" width="960" height="28" fill="none" stroke="black"/><line x1="170" y1="256" x2="170" y2="284" stroke="black"/><line x1="900" y1="256" x2="900" y2="284" stroke="black"/><text x="110" y="274" font-size="11">T1</text><text x="185" y="274" font-size="11">Transformateur 230/24V</text><text x="965" y="274" font-size="11">1</text>
<rect x="70" y="284" width="960" height="28" fill="none" stroke="black"/><line x1="170" y1="284" x2="170" y2="312" stroke="black"/><line x1="900" y1="284" x2="900" y2="312" stroke="black"/><text x="110" y="302" font-size="11">PS1</text><text x="185" y="302" font-size="11">Protection actionneur</text><text x="965" y="302" font-size="11">1</text>
<rect x="70" y="312" width="960" height="28" fill="none" stroke="black"/><line x1="170" y1="312" x2="170" y2="340" stroke="black"/><line x1="900" y1="312" x2="900" y2="340" stroke="black"/><text x="108" y="330" font-size="11">YV1</text><text x="185" y="330" font-size="11">Actionneur vanne 3 voies modulante</text><text x="965" y="330" font-size="11">1</text>
<rect x="70" y="340" width="960" height="28" fill="none" stroke="black"/><line x1="170" y1="340" x2="170" y2="368" stroke="black"/><line x1="900" y1="340" x2="900" y2="368" stroke="black"/><text x="108" y="358" font-size="11">TT1</text><text x="185" y="358" font-size="11">Sonde entrée batterie</text><text x="965" y="358" font-size="11">1</text>
<rect x="70" y="368" width="960" height="28" fill="none" stroke="black"/><line x1="170" y1="368" x2="170" y2="396" stroke="black"/><line x1="900" y1="368" x2="900" y2="396" stroke="black"/><text x="108" y="386" font-size="11">TT2</text><text x="185" y="386" font-size="11">Sonde reprise</text><text x="965" y="386" font-size="11">1</text>

<rect x="20" y="560" width="1060" height="30" fill="none" stroke="#222" stroke-width="1.5"/>
<line x1="985" y1="560" x2="985" y2="590" stroke="#222" stroke-width="1.5"/>
<text x="30" y="580" font-size="12">Nomenclature simplifiée</text>
<text x="1000" y="580" font-size="12">13</text>
</svg>
"""


tabs = st.tabs(["Résumé", "Puissance", "Commande", "Bornier", "Nomenclature"])

with tabs[0]:
    st.subheader("Résumé de fonctionnement")
    st.write("Contrôleur local détecté")
    st.write("Sondes de température détectées")
    st.write("Pompe détectée")
    st.write("Vanne 3 voies modulante détectée")
    st.write("Ventilation détectée")
    st.write("Mode dégivrage détecté")
    st.write("Consigne : +4°C")
    st.write("Pompe : fonctionnement permanent")
    st.write("Régulation : vanne modulante")
    st.write("Différentiel : 2 K")

with tabs[1]:
    st.subheader("Folio puissance")
    components.html(svg_power(), height=680, scrolling=True)

with tabs[2]:
    st.subheader("Folio commande")
    components.html(svg_command(), height=680, scrolling=True)

with tabs[3]:
    st.subheader("Folio bornier")
    components.html(svg_bornier(), height=680, scrolling=True)

with tabs[4]:
    st.subheader("Nomenclature simplifiée")
    components.html(svg_nomenclature(), height=680, scrolling=True)
