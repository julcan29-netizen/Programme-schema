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

        '<text x="70" y="110" font-size="11" fill="#111">L1</text>'
        '<text x="90" y="110" font-size="11" fill="#111">L2</text>'
        '<text x="110" y="110" font-size="11" fill="#111">L3</text>'

        '<line x1="80" y1="130" x2="80" y2="430" stroke="#111" stroke-width="2"/>'
        '<line x1="100" y1="130" x2="100" y2="430" stroke="#111" stroke-width="2"/>'
        '<line x1="120" y1="130" x2="120" y2="430" stroke="#111" stroke-width="2"/>'

        '<line x1="76" y1="145" x2="84" y2="155" stroke="#111" stroke-width="1.4"/>'
        '<line x1="96" y1="145" x2="104" y2="155" stroke="#111" stroke-width="1.4"/>'
        '<line x1="116" y1="145" x2="124" y2="155" stroke="#111" stroke-width="1.4"/>'
        '<text x="135" y="156" font-size="12" fill="#111">IG1</text>'

        '<line x1="76" y1="190" x2="84" y2="200" stroke="#111" stroke-width="1.4"/>'
        '<line x1="96" y1="190" x2="104" y2="200" stroke="#111" stroke-width="1.4"/>'
        '<line x1="116" y1="190" x2="124" y2="200" stroke="#111" stroke-width="1.4"/>'
        '<text x="135" y="201" font-size="12" fill="#111">Q1</text>'

        '<line x1="76" y1="235" x2="84" y2="245" stroke="#111" stroke-width="1.4"/>'
        '<line x1="96" y1="235" x2="104" y2="245" stroke="#111" stroke-width="1.4"/>'
        '<line x1="116" y1="235" x2="124" y2="245" stroke="#111" stroke-width="1.4"/>'
        '<text x="135" y="246" font-size="12" fill="#111">DM1</text>'

        '<line x1="76" y1="280" x2="84" y2="290" stroke="#111" stroke-width="1.4"/>'
        '<line x1="96" y1="280" x2="104" y2="290" stroke="#111" stroke-width="1.4"/>'
        '<line x1="116" y1="280" x2="124" y2="290" stroke="#111" stroke-width="1.4"/>'
        '<text x="135" y="291" font-size="12" fill="#111">KM1</text>'

        '<circle cx="100" cy="390" r="18" fill="none" stroke="#111" stroke-width="1.5"/>'
        '<text x="94" y="395" font-size="12" fill="#111">M</text>'
        '<text x="135" y="395" font-size="12" fill="#111">M1 Pompe</text>'

        '<text x="250" y="110" font-size="11" fill="#111">L1</text>'
        '<text x="270" y="110" font-size="11" fill="#111">L2</text>'
        '<text x="290" y="110" font-size="11" fill="#111">L3</text>'

        '<line x1="260" y1="130" x2="260" y2="430" stroke="#111" stroke-width="2"/>'
        '<line x1="280" y1="130" x2="280" y2="430" stroke="#111" stroke-width="2"/>'
        '<line x1="300" y1="130" x2="300" y2="430" stroke="#111" stroke-width="2"/>'

        '<line x1="256" y1="190" x2="264" y2="200" stroke="#111" stroke-width="1.4"/>'
        '<line x1="276" y1="190" x2="284" y2="200" stroke="#111" stroke-width="1.4"/>'
        '<line x1="296" y1="190" x2="304" y2="200" stroke="#111" stroke-width="1.4"/>'
        '<text x="315" y="201" font-size="12" fill="#111">QF Vent</text>'

        '<circle cx="280" cy="390" r="18" fill="none" stroke="#111" stroke-width="1.5"/>'
        '<text x="274" y="395" font-size="12" fill="#111">M</text>'
        '<text x="315" y="395" font-size="12" fill="#111">M2 Ventilation</text>'

        '<text x="475" y="110" font-size="11" fill="#111">230V / 24V</text>'
        '<line x1="500" y1="130" x2="500" y2="155" stroke="#111" stroke-width="1.5"/>'
        '<circle cx="492" cy="170" r="8" fill="none" stroke="#111" stroke-width="1.5"/>'
        '<circle cx="508" cy="170" r="8" fill="none" stroke="#111" stroke-width="1.5"/>'
        '<text x="522" y="174" font-size="12" fill="#111">T1</text>'

        '<rect x="760" y="155" width="24" height="18" fill="none" stroke="#111" stroke-width="1.3"/>'
        '<text x="745" y="150" font-size="11" fill="#111">PS1</text>'
        '<line x1="772" y1="173" x2="772" y2="250" stroke="#111" stroke-width="1.5"/>'
        '<rect x="764" y="250" width="16" height="22" fill="none" stroke="#111" stroke-width="1.3"/>'
        '<text x="790" y="265" font-size="12" fill="#111">YV1 Vanne 3 voies</text>'
        '<line x1="772" y1="272" x2="772" y2="285" stroke="#111" stroke-width="1.5"/>'
        '<polygon points="766,285 778,285 772,294" fill="none" stroke="#111" stroke-width="1.3"/>'

        '<rect x="20" y="500" width="960" height="30" fill="none" stroke="#222" stroke-width="1.5"/>'
        '<line x1="900" y1="500" x2="900" y2="530" stroke="#222" stroke-width="1.5"/>'
        '<text x="30" y="520" font-size="12" fill="#111">Folio puissance</text>'
        '<text x="915" y="520" font-size="12" fill="#111">10</text>'

        '</svg>'
    )

def svg_command():
    return (
        '<svg width="1000" height="520" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff">'
        '<rect x="20" y="20" width="960" height="480" fill="none" stroke="#222" stroke-width="1.5"/>'
        '<text x="40" y="45" font-size="20" fill="#111">Folio commande</text>'

        '<line x1="80" y1="90" x2="80" y2="430" stroke="#111" stroke-width="2"/>'
        '<line x1="920" y1="90" x2="920" y2="430" stroke="#111" stroke-width="2"/>'
        '<text x="72" y="80" font-size="11" fill="#111">L</text>'
        '<text x="912" y="80" font-size="11" fill="#111">N</text>'

        '<line x1="80" y1="150" x2="760" y2="150" stroke="#111" stroke-width="1.5"/>'
        '<rect x="760" y="140" width="28" height="20" fill="none" stroke="#111"/>'
        '<text x="800" y="154" font-size="12" fill="#111">KM1</text>'
        '<line x1="788" y1="150" x2="920" y2="150" stroke="#111" stroke-width="1.5"/>'
        '<text x="180" y="142" font-size="11" fill="#111">Commande pompe</text>'

        '<line x1="80" y1="220" x2="760" y2="220" stroke="#111" stroke-width="1.5"/>'
        '<rect x="760" y="210" width="28" height="20" fill="none" stroke="#111"/>'
        '<text x="800" y="224" font-size="12" fill="#111">KV1</text>'
        '<line x1="788" y1="220" x2="920" y2="220" stroke="#111" stroke-width="1.5"/>'
        '<text x="150" y="212" font-size="11" fill="#111">Ventilation permanente</text>'

        '<circle cx="260" cy="320" r="4" fill="none" stroke="#111"/>'
        '<circle cx="260" cy="380" r="4" fill="none" stroke="#111"/>'
        '<text x="272" y="324" font-size="11" fill="#111">TT1 Entrée batterie</text>'
        '<text x="272" y="384" font-size="11" fill="#111">TT2 Reprise</text>'

        '<rect x="470" y="290" width="160" height="100" fill="none" stroke="#111"/>'
        '<text x="485" y="315" font-size="12" fill="#111">A1 MPX PRO</text>'
        '<text x="485" y="338" font-size="10" fill="#111">Consigne +4°C</text>'
        '<text x="485" y="356" font-size="10" fill="#111">Marche pompe 12°C</text>'
        '<text x="485" y="374" font-size="10" fill="#111">Arrêt pompe 10°C</text>'

        '<line x1="264" y1="320" x2="470" y2="320" stroke="#111"/>'
        '<line x1="264" y1="380" x2="470" y2="380" stroke="#111"/>'

        '<line x1="630" y1="330" x2="760" y2="330" stroke="#111"/>'
        '<line x1="630" y1="350" x2="760" y2="350" stroke="#111"/>'
        '<text x="770" y="334" font-size="11" fill="#111">AO+</text>'
        '<text x="770" y="354" font-size="11" fill="#111">AO-</text>'
        '<text x="820" y="344" font-size="11" fill="#111">0-10V vers YV1</text>'

        '<rect x="20" y="470" width="960" height="30" fill="none" stroke="#222" stroke-width="1.5"/>'
        '<text x="35" y="490" font-size="12" fill="#111">Folio commande</text>'
        '<text x="920" y="490" font-size="12" fill="#111">11</text>'
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
    components.html(svg_command(), height=760, scrolling=True)

with tabs[3]:
    st.subheader("Folio bornier")
    components.html(svg_bornier(), height=760, scrolling=True)

with tabs[4]:
    st.subheader("Nomenclature simplifiée")
    components.html(svg_nomenclature(), height=760, scrolling=True)
