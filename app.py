import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Générateur de schéma électrique", layout="wide")

st.title("Générateur de schéma électrique")

texte = st.text_area(
    "Analyse fonctionnelle",
    value="Pompe, ventilation, vanne 3 voies, dégivrage naturel, consigne +4°C.",
    height=180,
)


def svg_power():
    return (
        '<svg width="1000" height="560" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff">'
        '<rect x="20" y="20" width="960" height="520" fill="none" stroke="#222" stroke-width="1.5"/>'

        '<text x="40" y="45" font-size="20" fill="#111">Folio puissance</text>'
        '<text x="60" y="85" font-size="12" fill="#111">COFFRET TYPE FROID MONO-VENTIL</text>'
        '<text x="780" y="85" font-size="12" fill="#111">Schéma de puissance</text>'

        '<g stroke="#d0d0d0" stroke-width="1" stroke-dasharray="4 4">'
        '<line x1="80" y1="90" x2="80" y2="480"/>'
        '<line x1="180" y1="90" x2="180" y2="480"/>'
        '<line x1="280" y1="90" x2="280" y2="480"/>'
        '<line x1="380" y1="90" x2="380" y2="480"/>'
        '<line x1="480" y1="90" x2="480" y2="480"/>'
        '<line x1="580" y1="90" x2="580" y2="480"/>'
        '<line x1="680" y1="90" x2="680" y2="480"/>'
        '<line x1="780" y1="90" x2="780" y2="480"/>'
        '<line x1="880" y1="90" x2="880" y2="480"/>'
        '<line x1="40" y1="120" x2="940" y2="120"/>'
        '<line x1="40" y1="220" x2="940" y2="220"/>'
        '<line x1="40" y1="320" x2="940" y2="320"/>'
        '<line x1="40" y1="420" x2="940" y2="420"/>'
        '</g>'

        '<text x="90" y="110" font-size="11" fill="#111">L1</text>'
        '<text x="110" y="110" font-size="11" fill="#111">L2</text>'
        '<text x="130" y="110" font-size="11" fill="#111">L3</text>'

        '<line x1="100" y1="130" x2="100" y2="430" stroke="#111" stroke-width="2"/>'
        '<line x1="120" y1="130" x2="120" y2="430" stroke="#111" stroke-width="2"/>'
        '<line x1="140" y1="130" x2="140" y2="430" stroke="#111" stroke-width="2"/>'

        '<line x1="96" y1="145" x2="104" y2="155" stroke="#111" stroke-width="1.4"/>'
        '<line x1="116" y1="145" x2="124" y2="155" stroke="#111" stroke-width="1.4"/>'
        '<line x1="136" y1="145" x2="144" y2="155" stroke="#111" stroke-width="1.4"/>'
        '<text x="155" y="156" font-size="12" fill="#111">IG1</text>'

        '<line x1="96" y1="190" x2="104" y2="200" stroke="#111" stroke-width="1.4"/>'
        '<line x1="116" y1="190" x2="124" y2="200" stroke="#111" stroke-width="1.4"/>'
        '<line x1="136" y1="190" x2="144" y2="200" stroke="#111" stroke-width="1.4"/>'
        '<text x="155" y="201" font-size="12" fill="#111">Q1</text>'

        '<line x1="96" y1="235" x2="104" y2="245" stroke="#111" stroke-width="1.4"/>'
        '<line x1="116" y1="235" x2="124" y2="245" stroke="#111" stroke-width="1.4"/>'
        '<line x1="136" y1="235" x2="144" y2="245" stroke="#111" stroke-width="1.4"/>'
        '<text x="155" y="246" font-size="12" fill="#111">DM1</text>'

        '<line x1="96" y1="280" x2="104" y2="290" stroke="#111" stroke-width="1.4"/>'
        '<line x1="116" y1="280" x2="124" y2="290" stroke="#111" stroke-width="1.4"/>'
        '<line x1="136" y1="280" x2="144" y2="290" stroke="#111" stroke-width="1.4"/>'
        '<text x="155" y="291" font-size="12" fill="#111">KM1</text>'

        '<circle cx="120" cy="390" r="18" fill="none" stroke="#111" stroke-width="1.5"/>'
        '<text x="114" y="395" font-size="12" fill="#111">M</text>'
        '<text x="155" y="395" font-size="12" fill="#111">M1 Pompe</text>'

        '<text x="270" y="110" font-size="11" fill="#111">L1</text>'
        '<text x="290" y="110" font-size="11" fill="#111">L2</text>'
        '<text x="310" y="110" font-size="11" fill="#111">L3</text>'

        '<line x1="280" y1="130" x2="280" y2="430" stroke="#111" stroke-width="2"/>'
        '<line x1="300" y1="130" x2="300" y2="430" stroke="#111" stroke-width="2"/>'
        '<line x1="320" y1="130" x2="320" y2="430" stroke="#111" stroke-width="2"/>'

        '<line x1="276" y1="190" x2="284" y2="200" stroke="#111" stroke-width="1.4"/>'
        '<line x1="296" y1="190" x2="304" y2="200" stroke="#111" stroke-width="1.4"/>'
        '<line x1="316" y1="190" x2="324" y2="200" stroke="#111" stroke-width="1.4"/>'
        '<text x="335" y="201" font-size="12" fill="#111">Q2</text>'

        '<circle cx="300" cy="390" r="18" fill="none" stroke="#111" stroke-width="1.5"/>'
        '<text x="294" y="395" font-size="12" fill="#111">M</text>'
        '<text x="335" y="395" font-size="12" fill="#111">M2 Ventilation</text>'

        '<text x="495" y="110" font-size="11" fill="#111">230V / 24V</text>'
        '<line x1="520" y1="130" x2="520" y2="155" stroke="#111" stroke-width="1.5"/>'
        '<circle cx="512" cy="170" r="8" fill="none" stroke="#111" stroke-width="1.5"/>'
        '<circle cx="528" cy="170" r="8" fill="none" stroke="#111" stroke-width="1.5"/>'
        '<text x="542" y="174" font-size="12" fill="#111">T1</text>'

        '<text x="760" y="110" font-size="11" fill="#111">L / N</text>'
        '<line x1="780" y1="130" x2="780" y2="155" stroke="#111" stroke-width="1.5"/>'
        '<line x1="800" y1="130" x2="800" y2="155" stroke="#111" stroke-width="1.5"/>'

        '<rect x="778" y="155" width="24" height="18" fill="none" stroke="#111" stroke-width="1.3"/>'
        '<text x="763" y="150" font-size="11" fill="#111">PS1</text>'
        '<line x1="790" y1="173" x2="790" y2="250" stroke="#111" stroke-width="1.5"/>'
        '<rect x="782" y="250" width="16" height="22" fill="none" stroke="#111" stroke-width="1.3"/>'
        '<text x="808" y="265" font-size="12" fill="#111">YV1 Vanne 3 voies</text>'
        '<line x1="790" y1="272" x2="790" y2="285" stroke="#111" stroke-width="1.5"/>'
        '<polygon points="784,285 796,285 790,294" fill="none" stroke="#111" stroke-width="1.3"/>'

        '<rect x="20" y="500" width="960" height="30" fill="none" stroke="#222" stroke-width="1.5"/>'
        '<line x1="900" y1="500" x2="900" y2="530" stroke="#222" stroke-width="1.5"/>'
        '<text x="30" y="520" font-size="12" fill="#111">Folio puissance</text>'
        '<text x="915" y="520" font-size="12" fill="#111">10</text>'

        '</svg>'
    )


def svg_command():
    return (
        '<svg width="1100" height="620" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff">'
        '<rect x="20" y="20" width="1060" height="580" fill="none" stroke="#222" stroke-width="1.5"/>'

        '<text x="40" y="48" font-size="22" fill="#111">Folio commande</text>'
        '<text x="40" y="78" font-size="12" fill="#111">COFFRET TYPE FROID MONO-VENTIL</text>'
        '<text x="900" y="78" font-size="12" fill="#111">Schéma de commande</text>'

        '<g stroke="#d9d9d9" stroke-width="1" stroke-dasharray="4 4">'
        '<line x1="80" y1="95" x2="80" y2="540"/>'
        '<line x1="180" y1="95" x2="180" y2="540"/>'
        '<line x1="280" y1="95" x2="280" y2="540"/>'
        '<line x1="380" y1="95" x2="380" y2="540"/>'
        '<line x1="480" y1="95" x2="480" y2="540"/>'
        '<line x1="580" y1="95" x2="580" y2="540"/>'
        '<line x1="680" y1="95" x2="680" y2="540"/>'
        '<line x1="780" y1="95" x2="780"def svg_power():
    return (
        '<svg width="1100" height="620" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff">'
        '<rect x="20" y="20" width="1060" height="580" fill="none" stroke="#222" stroke-width="1.5"/>'

        '<text x="40" y="48" font-size="22" fill="#111">Folio puissance</text>'
        '<text x="40" y="78" font-size="12" fill="#111">COFFRET TYPE FROID MONO-VENTIL</text>'
        '<text x="915" y="78" font-size="12" fill="#111">Schéma de puissance</text>'

        '<g stroke="#d9d9d9" stroke-width="1" stroke-dasharray="4 4">'
        '<line x1="80" y1="95" x2="80" y2="540"/>'
        '<line x1="180" y1="95" x2="180" y2="540"/>'
        '<line x1="280" y1="95" x2="280" y2="540"/>'
        '<line x1="380" y1="95" x2="380" y2="540"/>'
        '<line x1="480" y1="95" x2="480" y2="540"/>'
        '<line x1="580" y1="95" x2="580" y2="540"/>'
        '<line x1="680" y1="95" x2="680" y2="540"/>'
        '<line x1="780" y1="95" x2="780" y2="540"/>'
        '<line x1="880" y1="95" x2="880" y2="540"/>'
        '<line x1="980" y1="95" x2="980" y2="540"/>'
        '<line x1="40" y1="120" x2="1040" y2="120"/>'
        '<line x1="40" y1="220" x2="1040" y2="220"/>'
        '<line x1="40" y1="320" x2="1040" y2="320"/>'
        '<line x1="40" y1="420" x2="1040" y2="420"/>'
        '</g>'

        '<text x="92" y="108" font-size="11" fill="#111">L1</text>'
        '<text x="114" y="108" font-size="11" fill="#111">L2</text>'
        '<text x="136" y="108" font-size="11" fill="#111">L3</text>'
        '<text x="84" y="128" font-size="12" fill="#111">Pompe circulation</text>'

        '<line x1="100" y1="140" x2="100" y2="372" stroke="#111" stroke-width="2"/>'
        '<line x1="122" y1="140" x2="122" y2="372" stroke="#111" stroke-width="2"/>'
        '<line x1="144" y1="140" x2="144" y2="372" stroke="#111" stroke-width="2"/>'

        '<line x1="96" y1="158" x2="104" y2="168" stroke="#111" stroke-width="1.4"/>'
        '<line x1="118" y1="158" x2="126" y2="168" stroke="#111" stroke-width="1.4"/>'
        '<line x1="140" y1="158" x2="148" y2="168" stroke="#111" stroke-width="1.4"/>'
        '<text x="160" y="170" font-size="12" fill="#111">IG1</text>'

        '<line x1="96" y1="208" x2="104" y2="218" stroke="#111" stroke-width="1.4"/>'
        '<line x1="118" y1="208" x2="126" y2="218" stroke="#111" stroke-width="1.4"/>'
        '<line x1="140" y1="208" x2="148" y2="218" stroke="#111" stroke-width="1.4"/>'
        '<text x="160" y="220" font-size="12" fill="#111">Q1</text>'

        '<line x1="96" y1="258" x2="104" y2="268" stroke="#111" stroke-width="1.4"/>'
        '<line x1="118" y1="258" x2="126" y2="268" stroke="#111" stroke-width="1.4"/>'
        '<line x1="140" y1="258" x2="148" y2="268" stroke="#111" stroke-width="1.4"/>'
        '<text x="160" y="270" font-size="12" fill="#111">DM1</text>'

        '<line x1="100" y1="372" x2="110" y2="372" stroke="#111" stroke-width="1.5"/>'
        '<line x1="144" y1="372" x2="134" y2="372" stroke="#111" stroke-width="1.5"/>'
        '<line x1="100" y1="408" x2="110" y2="408" stroke="#111" stroke-width="1.5"/>'
        '<line x1="144" y1="408" x2="134" y2="408" stroke="#111" stroke-width="1.5"/>'
        '<circle cx="122" cy="390" r="18" fill="none" stroke="#111" stroke-width="1.5"/>'
        '<text x="116" y="395" font-size="12" fill="#111">M</text>'
        '<text x="160" y="395" font-size="12" fill="#111">M1 Pompe</text>'

        '<line x1="100" y1="408" x2="100" y2="470" stroke="#111" stroke-width="2"/>'
        '<line x1="122" y1="408" x2="122" y2="470" stroke="#111" stroke-width="2"/>'
        '<line x1="144" y1="408" x2="144" y2="470" stroke="#111" stroke-width="2"/>'

        '<text x="312" y="108" font-size="11" fill="#111">L1</text>'
        '<text x="334" y="108" font-size="11" fill="#111">L2</text>'
        '<text x="356" y="108" font-size="11" fill="#111">L3</text>'
        '<text x="300" y="128" font-size="12" fill="#111">Ventilation</text>'

        '<line x1="320" y1="140" x2="320" y2="372" stroke="#111" stroke-width="2"/>'
        '<line x1="342" y1="140" x2="342" y2="372" stroke="#111" stroke-width="2"/>'
        '<line x1="364" y1="140" x2="364" y2="372" stroke="#111" stroke-width="2"/>'

        '<line x1="316" y1="208" x2="324" y2="218" stroke="#111" stroke-width="1.4"/>'
        '<line x1="338" y1="208" x2="346" y2="218" stroke="#111" stroke-width="1.4"/>'
        '<line x1="360" y1="208" x2="368" y2="218" stroke="#111" stroke-width="1.4"/>'
        '<text x="382" y="220" font-size="12" fill="#111">Q2</text>'

        '<line x1="320" y1="372" x2="330" y2="372" stroke="#111" stroke-width="1.5"/>'
        '<line x1="364" y1="372" x2="354" y2="372" stroke="#111" stroke-width="1.5"/>'
        '<line x1="320" y1="408" x2="330" y2="408" stroke="#111" stroke-width="1.5"/>'
        '<line x1="364" y1="408" x2="354" y2="408" stroke="#111" stroke-width="1.5"/>'
        '<circle cx="342" cy="390" r="18" fill="none" stroke="#111" stroke-width="1.5"/>'
        '<text x="336" y="395" font-size="12" fill="#111">M</text>'
        '<text x="382" y="395" font-size="12" fill="#111">M2 Ventilation</text>'

        '<line x1="320" y1="408" x2="320" y2="470" stroke="#111" stroke-width="2"/>'
        '<line x1="342" y1="408" x2="342" y2="470" stroke="#111" stroke-width="2"/>'
        '<line x1="364" y1="408" x2="364" y2="470" stroke="#111" stroke-width="2"/>'

        '<text x="540" y="108" font-size="11" fill="#111">Alim commande</text>'
        '<text x="540" y="124" font-size="10" fill="#111">230V / 24V</text>'

        '<line x1="565" y1="140" x2="565" y2="165" stroke="#111" stroke-width="1.5"/>'
        '<line x1="595" y1="140" x2="595" y2="165" stroke="#111" stroke-width="1.5"/>'
        '<circle cx="557" cy="182" r="8" fill="none" stroke="#111" stroke-width="1.5"/>'
        '<circle cx="573" cy="182" r="8" fill="none" stroke="#111" stroke-width="1.5"/>'
        '<circle cx="587" cy="182" r="8" fill="none" stroke="#111" stroke-width="1.5"/>'
        '<circle cx="603" cy="182" r="8" fill="none" stroke="#111" stroke-width="1.5"/>'
        '<text x="620" y="186" font-size="12" fill="#111">T1</text>'
        '<text x="550" y="205" font-size="10" fill="#111">primaire</text>'
        '<text x="588" y="205" font-size="10" fill="#111">secondaire</text>'

        '<line x1="587" y1="190" x2="587" y2="225" stroke="#111" stroke-width="1.3"/>'
        '<line x1="603" y1="190" x2="603" y2="225" stroke="#111" stroke-width="1.3"/>'
        '<text x="610" y="230" font-size="10" fill="#111">24V~ / N</text>'

        '<text x="800" y="108" font-size="11" fill="#111">Actionneur vanne 3 voies</text>'
        '<text x="810" y="124" font-size="10" fill="#111">alimentation 24V~</text>'

        '<line x1="840" y1="140" x2="840" y2="165" stroke="#111" stroke-width="1.5"/>'
        '<line x1="862" y1="140" x2="862" y2="165" stroke="#111" stroke-width="1.5"/>'
        '<text x="834" y="178" font-size="10" fill="#111">L</text>'
        '<text x="858" y="178" font-size="10" fill="#111">N</text>'

        '<rect x="836" y="188" width="30" height="18" fill="none" stroke="#111" stroke-width="1.3"/>'
        '<text x="825" y="184" font-size="11" fill="#111">PS1</text>'
        '<line x1="851" y1="206" x2="851" y2="282" stroke="#111" stroke-width="1.5"/>'

        '<rect x="842" y="282" width="18" height="28" fill="none" stroke="#111" stroke-width="1.3"/>'
        '<text x="875" y="300" font-size="12" fill="#111">YV1</text>'
        '<text x="875" y="316" font-size="11" fill="#111">Vanne 3 voies modulante</text>'

        '<line x1="851" y1="310" x2="851" y2="326" stroke="#111" stroke-width="1.5"/>'
        '<polygon points="845,326 857,326 851,336" fill="none" stroke="#111" stroke-width="1.3"/>'

        '<rect x="20" y="560" width="1060" height="30" fill="none" stroke="#222" stroke-width="1.5"/>'
        '<line x1="985" y1="560" x2="985" y2="590" stroke="#222" stroke-width="1.5"/>'
        '<text x="30" y="580" font-size="12" fill="#111">Folio puissance</text>'
        '<text x="1000" y="580" font-size="12" fill="#111">10</text>'

        '</svg>'
    )


def svg_bornier():
    return (
        '<svg width="1000" height="520" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff">'
        '<rect x="20" y="20" width="960" height="480" fill="none" stroke="#222" stroke-width="1.5"/>'
        '<text x="40" y="45" font-size="20" fill="#111">Folio bornier</text>'
        '<text x="60" y="95" font-size="13" fill="#111">Bornier X1</text>'

        '<rect x="60" y="120" width="860" height="28" fill="none" stroke="#111"/>'
        '<line x1="140" y1="120" x2="140" y2="148" stroke="#111"/>'
        '<line x1="520" y1="120" x2="520" y2="148" stroke="#111"/>'
        '<text x="80" y="138" font-size="12" fill="#111">Repère</text>'
        '<text x="180" y="138" font-size="12" fill="#111">Fonction</text>'
        '<text x="580" y="138" font-size="12" fill="#111">Extérieur</text>'

        '<rect x="60" y="160" width="860" height="24" fill="none" stroke="#111"/><line x1="140" y1="160" x2="140" y2="184" stroke="#111"/><line x1="520" y1="160" x2="520" y2="184" stroke="#111"/><text x="88" y="176" font-size="11" fill="#111">1</text><text x="150" y="176" font-size="11" fill="#111">Sonde TT1 entrée batterie</text><text x="580" y="176" font-size="11" fill="#111">Champ</text>'
        '<rect x="60" y="184" width="860" height="24" fill="none" stroke="#111"/><line x1="140" y1="184" x2="140" y2="208" stroke="#111"/><line x1="520" y1="184" x2="520" y2="208" stroke="#111"/><text x="88" y="200" font-size="11" fill="#111">2</text><text x="150" y="200" font-size="11" fill="#111">Sonde TT2 reprise</text><text x="580" y="200" font-size="11" fill="#111">Champ</text>'
        '<rect x="60" y="208" width="860" height="24" fill="none" stroke="#111"/><line x1="140" y1="208" x2="140" y2="232" stroke="#111"/><line x1="520" y1="208" x2="520" y2="232" stroke="#111"/><text x="88" y="224" font-size="11" fill="#111">3</text><text x="150" y="224" font-size="11" fill="#111">Sortie 0-10V AO+</text><text x="580" y="224" font-size="11" fill="#111">Actionneur YV1</text>'
        '<rect x="60" y="232" width="860" height="24" fill="none" stroke="#111"/><line x1="140" y1="232" x2="140" y2="256" stroke="#111"/><line x1="520" y1="232" x2="520" y2="256" stroke="#111"/><text x="88" y="248" font-size="11" fill="#111">4</text><text x="150" y="248" font-size="11" fill="#111">Sortie 0-10V AO-</text><text x="580" y="248" font-size="11" fill="#111">Actionneur YV1</text>'
        '<rect x="60" y="256" width="860" height="24" fill="none" stroke="#111"/><line x1="140" y1="256" x2="140" y2="280" stroke="#111"/><line x1="520" y1="256" x2="520" y2="280" stroke="#111"/><text x="88" y="272" font-size="11" fill="#111">5</text><text x="150" y="272" font-size="11" fill="#111">Commande pompe</text><text x="580" y="272" font-size="11" fill="#111">KM1</text>'
        '<rect x="60" y="280" width="860" height="24" fill="none" stroke="#111"/><line x1="140" y1="280" x2="140" y2="304" stroke="#111"/><line x1="520" y1="280" x2="520" y2="304" stroke="#111"/><text x="88" y="296" font-size="11" fill="#111">6</text><text x="150" y="296" font-size="11" fill="#111">Retour neutre</text><text x="580" y="296" font-size="11" fill="#111">N</text>'
        '<rect x="60" y="304" width="860" height="24" fill="none" stroke="#111"/><line x1="140" y1="304" x2="140" y2="328" stroke="#111"/><line x1="520" y1="304" x2="520" y2="328" stroke="#111"/><text x="88" y="320" font-size="11" fill="#111">7</text><text x="150" y="320" font-size="11" fill="#111">Commande ventilation</text><text x="580" y="320" font-size="11" fill="#111">KV1</text>'
        '<rect x="60" y="328" width="860" height="24" fill="none" stroke="#111"/><line x1="140" y1="328" x2="140" y2="352" stroke="#111"/><line x1="520" y1="328" x2="520" y2="352" stroke="#111"/><text x="88" y="344" font-size="11" fill="#111">8</text><text x="150" y="344" font-size="11" fill="#111">Info dégivrage</text><text x="580" y="344" font-size="11" fill="#111">Entrée REG</text>'

        '<rect x="20" y="470" width="960" height="30" fill="none" stroke="#222" stroke-width="1.5"/>'
        '<text x="35" y="490" font-size="12" fill="#111">Folio bornier</text>'
        '<text x="920" y="490" font-size="12" fill="#111">12</text>'
        '</svg>'
    )


def svg_nomenclature():
    return (
        '<svg width="1000" height="560" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff">'
        '<rect x="20" y="20" width="960" height="520" fill="none" stroke="#222" stroke-width="1.5"/>'
        '<text x="40" y="45" font-size="20" fill="#111">Nomenclature simplifiée</text>'

        '<rect x="60" y="100" width="860" height="28" fill="none" stroke="#111"/>'
        '<line x1="140" y1="100" x2="140" y2="128" stroke="#111"/>'
        '<line x1="760" y1="100" x2="760" y2="128" stroke="#111"/>'
        '<text x="80" y="118" font-size="12" fill="#111">Repère</text>'
        '<text x="180" y="118" font-size="12" fill="#111">Désignation</text>'
        '<text x="820" y="118" font-size="12" fill="#111">Qté</text>'

        '<rect x="60" y="140" width="860" height="22" fill="none" stroke="#111"/><line x1="140" y1="140" x2="140" y2="162" stroke="#111"/><line x1="760" y1="140" x2="760" y2="162" stroke="#111"/><text x="84" y="155" font-size="11" fill="#111">IG1</text><text x="150" y="155" font-size="11" fill="#111">Interrupteur général</text><text x="835" y="155" font-size="11" fill="#111">1</text>'
        '<rect x="60" y="162" width="860" height="22" fill="none" stroke="#111"/><line x1="140" y1="162" x2="140" y2="184" stroke="#111"/><line x1="760" y1="162" x2="760" y2="184" stroke="#111"/><text x="88" y="177" font-size="11" fill="#111">Q1</text><text x="150" y="177" font-size="11" fill="#111">Protection générale</text><text x="835" y="177" font-size="11" fill="#111">1</text>'
        '<rect x="60" y="184" width="860" height="22" fill="none" stroke="#111"/><line x1="140" y1="184" x2="140" y2="206" stroke="#111"/><line x1="760" y1="184" x2="760" y2="206" stroke="#111"/><text x="84" y="199" font-size="11" fill="#111">DM1</text><text x="150" y="199" font-size="11" fill="#111">Protection moteur pompe</text><text x="835" y="199" font-size="11" fill="#111">1</text>'
        '<rect x="60" y="206" width="860" height="22" fill="none" stroke="#111"/><line x1="140" y1="206" x2="140" y2="228" stroke="#111"/><line x1="760" y1="206" x2="760" y2="228" stroke="#111"/><text x="88" y="221" font-size="11" fill="#111">QF</text><text x="150" y="221" font-size="11" fill="#111">Protection ventilation</text><text x="835" y="221" font-size="11" fill="#111">1</text>'
        '<rect x="60" y="228" width="860" height="22" fill="none" stroke="#111"/><line x1="140" y1="228" x2="140" y2="250" stroke="#111"/><line x1="760" y1="228" x2="760" y2="250" stroke="#111"/><text x="84" y="243" font-size="11" fill="#111">KM1</text><text x="150" y="243" font-size="11" fill="#111">Contacteur pompe</text><text x="835" y="243" font-size="11" fill="#111">1</text>'
        '<rect x="60" y="250" width="860" height="22" fill="none" stroke="#111"/><line x1="140" y1="250" x2="140" y2="272" stroke="#111"/><line x1="760" y1="250" x2="760" y2="272" stroke="#111"/><text x="84" y="265" font-size="11" fill="#111">KV1</text><text x="150" y="265" font-size="11" fill="#111">Relais ventilation</text><text x="835" y="265" font-size="11" fill="#111">1</text>'
        '<rect x="60" y="272" width="860" height="22" fill="none" stroke="#111"/><line x1="140" y1="272" x2="140" y2="294" stroke="#111"/><line x1="760" y1="272" x2="760" y2="294" stroke="#111"/><text x="88" y="287" font-size="11" fill="#111">T1</text><text x="150" y="287" font-size="11" fill="#111">Transformateur alimentation commande</text><text x="835" y="287" font-size="11" fill="#111">1</text>'
        '<rect x="60" y="294" width="860" height="22" fill="none" stroke="#111"/><line x1="140" y1="294" x2="140" y2="316" stroke="#111"/><line x1="760" y1="294" x2="760" y2="316" stroke="#111"/><text x="88" y="309" font-size="11" fill="#111">A1</text><text x="150" y="309" font-size="11" fill="#111">Régulateur MPX PRO</text><text x="835" y="309" font-size="11" fill="#111">1</text>'
        '<rect x="60" y="316" width="860" height="22" fill="none" stroke="#111"/><line x1="140" y1="316" x2="140" y2="338" stroke="#111"/><line x1="760" y1="316" x2="760" y2="338" stroke="#111"/><text x="88" y="331" font-size="11" fill="#111">X1</text><text x="150" y="331" font-size="11" fill="#111">Bornier extérieur</text><text x="835" y="331" font-size="11" fill="#111">1</text>'
        '<rect x="60" y="338" width="860" height="22" fill="none" stroke="#111"/><line x1="140" y1="338" x2="140" y2="360" stroke="#111"/><line x1="760" y1="338" x2="760" y2="360" stroke="#111"/><text x="84" y="353" font-size="11" fill="#111">YV1</text><text x="150" y="353" font-size="11" fill="#111">Actionneur vanne 3 voies 0-10V</text><text x="835" y="353" font-size="11" fill="#111">1</text>'
        '<rect x="60" y="360" width="860" height="22" fill="none" stroke="#111"/><line x1="140" y1="360" x2="140" y2="382" stroke="#111"/><line x1="760" y1="360" x2="760" y2="382" stroke="#111"/><text x="84" y="375" font-size="11" fill="#111">TT1</text><text x="150" y="375" font-size="11" fill="#111">Sonde entrée batterie</text><text x="835" y="375" font-size="11" fill="#111">1</text>'
        '<rect x="60" y="382" width="860" height="22" fill="none" stroke="#111"/><line x1="140" y1="382" x2="140" y2="404" stroke="#111"/><line x1="760" y1="382" x2="760" y2="404" stroke="#111"/><text x="84" y="397" font-size="11" fill="#111">TT2</text><text x="150" y="397" font-size="11" fill="#111">Sonde reprise</text><text x="835" y="397" font-size="11" fill="#111">1</text>'

        '<rect x="20" y="510" width="960" height="30" fill="none" stroke="#222" stroke-width="1.5"/>'
        '<text x="35" y="530" font-size="12" fill="#111">Nomenclature simplifiée</text>'
        '<text x="920" y="530" font-size="12" fill="#111">13</text>'
        '</svg>'
    )


if st.button("Générer le schéma électrique"):
    st.success("Schéma généré")

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
    st.write("Marche pompe : ≥ 12°C")
    st.write("Arrêt pompe : ≤ 10°C")
    st.write("Différentiel : 2 K")

with tabs[1]:
    st.subheader("Folio puissance")
    components.html(svg_power(), height=760, scrolling=True)

with tabs[2]:
    st.subheader("Folio commande")
    components.html(svg_command
