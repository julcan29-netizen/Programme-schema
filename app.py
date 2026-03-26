import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Générateur de schéma électrique", layout="wide")


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


def build_power_svg():
    return """
    <svg width="1200" height="700" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff">
      <rect x="20" y="20" width="1160" height="660" fill="none" stroke="#222" stroke-width="1.5"/>

      <text x="40" y="45" font-size="18" fill="#111">COFFRET TYPE FROID MONO-VENTIL</text>
      <text x="40" y="95" font-size="18" fill="#111">Folio puissance</text>

      <!-- Grille légère -->
      <g stroke="#d0d0d0" stroke-width="1" stroke-dasharray="4 4">
        <line x1="80" y1="80" x2="80" y2="620"/>
        <line x1="200" y1="80" x2="200" y2="620"/>
        <line x1="320" y1="80" x2="320" y2="620"/>
        <line x1="440" y1="80" x2="440" y2="620"/>
        <line x1="560" y1="80" x2="560" y2="620"/>
        <line x1="680" y1="80" x2="680" y2="620"/>
        <line x1="800" y1="80" x2="800" y2="620"/>
        <line x1="920" y1="80" x2="920" y2="620"/>
        <line x1="1040" y1="80" x2="1040" y2="620"/>

        <line x1="40" y1="120" x2="1140" y2="120"/>
        <line x1="40" y1="220" x2="1140" y2="220"/>
        <line x1="40" y1="320" x2="1140" y2="320"/>
        <line x1="40" y1="420" x2="1140" y2="420"/>
        <line x1="40" y1="520" x2="1140" y2="520"/>
      </g>

      <!-- Départ pompe -->
      <text x="120" y="110" font-size="14" fill="#111">Départ pompe</text>
      <line x1="110" y1="140" x2="110" y2="560" stroke="#111" stroke-width="2"/>
      <line x1="130" y1="140" x2="130" y2="560" stroke="#111" stroke-width="2"/>
      <line x1="150" y1="140" x2="150" y2="560" stroke="#111" stroke-width="2"/>

      <text x="100" y="135" font-size="11" fill="#111">L1</text>
      <text x="120" y="135" font-size="11" fill="#111">L2</text>
      <text x="140" y="135" font-size="11" fill="#111">L3</text>

      <line x1="110" y1="165" x2="110" y2="190" stroke="#111" stroke-width="2"/>
      <line x1="130" y1="165" x2="130" y2="190" stroke="#111" stroke-width="2"/>
      <line x1="150" y1="165" x2="150" y2="190" stroke="#111" stroke-width="2"/>
      <line x1="105" y1="165" x2="115" y2="175" stroke="#111" stroke-width="1.5"/>
      <line x1="125" y1="165" x2="135" y2="175" stroke="#111" stroke-width="1.5"/>
      <line x1="145" y1="165" x2="155" y2="175" stroke="#111" stroke-width="1.5"/>
      <text x="170" y="180" font-size="12" fill="#111">IG1</text>

      <line x1="110" y1="220" x2="110" y2="250" stroke="#111" stroke-width="2"/>
      <line x1="130" y1="220" x2="130" y2="250" stroke="#111" stroke-width="2"/>
      <line x1="150" y1="220" x2="150" y2="250" stroke="#111" stroke-width="2"/>
      <line x1="104" y1="220" x2="116" y2="232" stroke="#111" stroke-width="1.5"/>
      <line x1="124" y1="220" x2="136" y2="232" stroke="#111" stroke-width="1.5"/>
      <line x1="144" y1="220" x2="156" y2="232" stroke="#111" stroke-width="1.5"/>
      <text x="170" y="238" font-size="12" fill="#111">Q1</text>

      <line x1="110" y1="280" x2="110" y2="330" stroke="#111" stroke-width="2"/>
      <line x1="130" y1="280" x2="130" y2="330" stroke="#111" stroke-width="2"/>
      <line x1="150" y1="280" x2="150" y2="330" stroke="#111" stroke-width="2"/>
      <line x1="104" y1="300" x2="110" y2="307" stroke="#111" stroke-width="1.5"/>
      <line x1="124" y1="300" x2="130" y2="307" stroke="#111" stroke-width="1.5"/>
      <line x1="144" y1="300" x2="150" y2="307" stroke="#111" stroke-width="1.5"/>
      <text x="170" y="308" font-size="12" fill="#111">DM1</text>

      <line x1="110" y1="360" x2="110" y2="395" stroke="#111" stroke-width="2"/>
      <line x1="130" y1="360" x2="130" y2="395" stroke="#111" stroke-width="2"/>
      <line x1="150" y1="360" x2="150" y2="395" stroke="#111" stroke-width="2"/>
      <line x1="110" y1="395" x2="110" y2="405" stroke="#111" stroke-width="2"/>
      <line x1="130" y1="395" x2="130" y2="405" stroke="#111" stroke-width="2"/>
      <line x1="150" y1="395" x2="150" y2="405" stroke="#111" stroke-width="2"/>
      <text x="170" y="395" font-size="12" fill="#111">KM1</text>

      <circle cx="130" cy="500" r="20" fill="none" stroke="#111" stroke-width="1.5"/>
      <text x="124" y="505" font-size="12" fill="#111">M</text>
      <text x="160" y="505" font-size="12" fill="#111">M1 Pompe</text>

      <!-- Départ ventilation -->
      <text x="360" y="110" font-size="14" fill="#111">Départ ventilation</text>
      <line x1="350" y1="140" x2="350" y2="560" stroke="#111" stroke-width="2"/>
      <line x1="370" y1="140" x2="370" y2="560" stroke="#111" stroke-width="2"/>
      <line x1="390" y1="140" x2="390" y2="560" stroke="#111" stroke-width="2"/>

      <text x="340" y="135" font-size="11" fill="#111">L1</text>
      <text x="360" y="135" font-size="11" fill="#111">L2</text>
      <text x="380" y="135" font-size="11" fill="#111">L3</text>

      <line x1="350" y1="220" x2="350" y2="250" stroke="#111" stroke-width="2"/>
      <line x1="370" y1="220" x2="370" y2="250" stroke="#111" stroke-width="2"/>
      <line x1="390" y1="220" x2="390" y2="250" stroke="#111" stroke-width="2"/>
      <line x1="344" y1="220" x2="356" y2="232" stroke="#111" stroke-width="1.5"/>
      <line x1="364" y1="220" x2="376" y2="232" stroke="#111" stroke-width="1.5"/>
      <line x1="384" y1="220" x2="396" y2="232" stroke="#111" stroke-width="1.5"/>
      <text x="410" y="238" font-size="12" fill="#111">QF Vent</text>

      <circle cx="370" cy="500" r="20" fill="none" stroke="#111" stroke-width="1.5"/>
      <text x="364" y="505" font-size="12" fill="#111">M</text>
      <text x="400" y="505" font-size="12" fill="#111">M2 Ventilation</text>

      <!-- Transfo -->
      <text x="560" y="110" font-size="14" fill="#111">Alim commande</text>
      <line x1="600" y1="180" x2="600" y2="205" stroke="#111" stroke-width="1.5"/>
      <circle cx="590" cy="220" r="10" fill="none" stroke="#111" stroke-width="1.5"/>
      <circle cx="610" cy="220" r="10" fill="none" stroke="#111" stroke-width="1.5"/>
      <text x="625" y="225" font-size="12" fill="#111">T1</text>
      <text x="575" y="170" font-size="10" fill="#111">230/24V</text>

      <!-- Actionneur -->
      <rect x="850" y="210" width="28" height="22" fill="none" stroke="#111" stroke-width="1.5"/>
      <text x="839" y="205" font-size="11" fill="#111">PS</text>
      <text x="885" y="225" font-size="12" fill="#111">PS1</text>

      <line x1="864" y1="232" x2="864" y2="320" stroke="#111" stroke-width="1.5"/>

      <rect x="855" y="320" width="18" height="24" fill="none" stroke="#111" stroke-width="1.5"/>
      <text x="885" y="336" font-size="12" fill="#111">YV1 Vanne 3 voies</text>
      <line x1="864" y1="344" x2="864" y2="360" stroke="#111" stroke-width="1.5"/>
      <polygon points="857,360 871,360 864,370" fill="none" stroke="#111" stroke-width="1.5"/>

      <!-- Cartouche -->
      <rect x="20" y="640" width="1160" height="30" fill="none" stroke="#222" stroke-width="1.5"/>
      <line x1="1000" y1="640" x2="1000" y2="670" stroke="#222" stroke-width="1.5"/>
      <line x1="1090" y1="640" x2="1090" y2="670" stroke="#222" stroke-width="1.5"/>
      <text x="30" y="660" font-size="12" fill="#111">Folio puissance</text>
      <text x="1015" y="660" font-size="12" fill="#111">Folio</text>
      <text x="1115" y="660" font-size="12" fill="#111">10</text>
    </svg>
    """


def build_command_svg():
    return """
    <svg width="1200" height="700" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff">
      <rect x="20" y="20" width="1160" height="660" fill="none" stroke="#222" stroke-width="1.5"/>

      <text x="40" y="45" font-size="18" fill="#111">COFFRET TYPE FROID MONO-VENTIL</text>
      <text x="40" y="95" font-size="18" fill="#111">Folio commande</text>

      <!-- Grille -->
      <g stroke="#d0d0d0" stroke-width="1" stroke-dasharray="4 4">
        <line x1="80" y1="80" x2="80" y2="620"/>
        <line x1="200" y1="80" x2="200" y2="620"/>
        <line x1="320" y1="80" x2="320" y2="620"/>
        <line x1="440" y1="80" x2="440" y2="620"/>
        <line x1="560" y1="80" x2="560" y2="620"/>
        <line x1="680" y1="80" x2="680" y2="620"/>
        <line x1="800" y1="80" x2="800" y2="620"/>
        <line x1="920" y1="80" x2="920" y2="620"/>
        <line x1="1040" y1="80" x2="1040" y2="620"/>

        <line x1="40" y1="120" x2="1140" y2="120"/>
        <line x1="40" y1="220" x2="1140" y2="220"/>
        <line x1="40" y1="320" x2="1140" y2="320"/>
        <line x1="40" y1="420" x2="1140" y2="420"/>
        <line x1="40" y1="520" x2="1140" y2="520"/>
      </g>

      <!-- Rails -->
      <line x1="80" y1="100" x2="80" y2="610" stroke="#111" stroke-width="2"/>
      <line x1="1120" y1="100" x2="1120" y2="610" stroke="#111" stroke-width="2"/>
      <text x="72" y="95" font-size="11" fill="#111">L</text>
      <text x="1112" y="95" font-size="11" fill="#111">N</text>

      <!-- Ligne pompe -->
      <line x1="80" y1="180" x2="200" y2="180" stroke="#111" stroke-width="1.5"/>
      <line x1="220" y1="180" x2="340" y2="180" stroke="#111" stroke-width="1.5"/>
      <line x1="360" y1="180" x2="860" y2="180" stroke="#111" stroke-width="1.5"/>
      <line x1="890" y1="180" x2="1120" y2="180" stroke="#111" stroke-width="1.5"/>

      <line x1="200" y1="172" x2="220" y2="188" stroke="#111" stroke-width="1.5"/>
      <text x="150" y="172" font-size="11" fill="#111">DEG</text>

      <line x1="340" y1="172" x2="360" y2="188" stroke="#111" stroke-width="1.5"/>
      <text x="292" y="172" font-size="11" fill="#111">REG</text>

      <rect x="860" y="170" width="28" height="20" fill="none" stroke="#111" stroke-width="1.5"/>
      <text x="900" y="184" font-size="12" fill="#111">KM1</text>

      <!-- Ligne ventilo -->
      <line x1="80" y1="280" x2="860" y2="280" stroke="#111" stroke-width="1.5"/>
      <line x1="890" y1="280" x2="1120" y2="280" stroke="#111" stroke-width="1.5"/>
      <rect x="860" y="270" width="28" height="20" fill="none" stroke="#111" stroke-width="1.5"/>
      <text x="900" y="284" font-size="12" fill="#111">KV1</text>
      <text x="170" y="272" font-size="11" fill="#111">Ventilation permanente</text>

      <!-- Régulateur -->
      <circle cx="380" cy="420" r="5" fill="none" stroke="#111" stroke-width="1.5"/>
      <line x1="380" y1="425" x2="380" y2="455" stroke="#111" stroke-width="1.5"/>
      <text x="392" y="424" font-size="11" fill="#111">TT1 Entrée batterie</text>

      <circle cx="380" cy="490" r="5" fill="none" stroke="#111" stroke-width="1.5"/>
      <line x1="380" y1="495" x2="380" y2="525" stroke="#111" stroke-width="1.5"/>
      <text x="392" y="494" font-size="11" fill="#111">TT2 Reprise</text>

      <rect x="500" y="400" width="170" height="110" fill="none" stroke="#111" stroke-width="1.5"/>
      <text x="515" y="425" font-size="12" fill="#111">A1 MPX PRO</text>
      <text x="515" y="447" font-size="10" fill="#111">Consigne +4°C</text>
      <text x="515" y="465" font-size="10" fill="#111">Marche pompe 12°C</text>
      <text x="515" y="483" font-size="10" fill="#111">Arrêt pompe 10°C</text>
      <text x="515" y="501" font-size="10" fill="#111">Différentiel 2K</text>

      <line x1="385" y1="420" x2="500" y2="420" stroke="#111" stroke-width="1.5"/>
      <line x1="385" y1="490" x2="500" y2="490" stroke="#111" stroke-width="1.5"/>

      <!-- Sortie analogique -->
      <line x1="670" y1="435" x2="790" y2="435" stroke="#111" stroke-width="1.5"/>
      <line x1="670" y1="455" x2="790" y2="455" stroke="#111" stroke-width="1.5"/>

      <polygon points="790,435 800,430 800,440" fill="none" stroke="#111" stroke-width="1.5"/>
      <polygon points="790,455 800,450 800,460" fill="none" stroke="#111" stroke-width="1.5"/>

      <text x="810" y="439" font-size="11" fill="#111">AO+</text>
      <text x="810" y="459" font-size="11" fill="#111">AO-</text>
      <text x="860" y="447" font-size="11" fill="#111">0-10V vers YV1</text>

      <!-- Cartouche -->
      <rect x="20" y="640" width="1160" height="30" fill="none" stroke="#222" stroke-width="1.5"/>
      <line x1="1000" y1="640" x2="1000" y2="670" stroke="#222" stroke-width="1.5"/>
      <line x1="1090" y1="640" x2="1090" y2="670" stroke="#222" stroke-width="1.5"/>
      <text x="30" y="660" font-size="12" fill="#111">Folio commande</text>
      <text x="1015" y="660" font-size="12" fill="#111">Folio</text>
      <text x="1115" y="660" font-size="12" fill="#111">11</text>
    </svg>
    """


def build_bornier_svg():
    return """
    <svg width="1200" height="700" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff">
      <rect x="20" y="20" width="1160" height="660" fill="none" stroke="#222" stroke-width="1.5"/>

      <text x="40" y="45" font-size="18" fill="#111">COFFRET TYPE FROID MONO-VENTIL</text>
      <text x="40" y="95" font-size="18" fill="#111">Folio bornier</text>

      <g stroke="#d0d0d0" stroke-width="1" stroke-dasharray="4 4">
        <line x1="80" y1="80" x2="80" y2="620"/>
        <line x1="200" y1="80" x2="200" y2="620"/>
        <line x1="320" y1="80" x2="320" y2="620"/>
        <line x1="440" y1="80" x2="440" y2="620"/>
        <line x1="560" y1="80" x2="560" y2="620"/>
        <line x1="680" y1="80" x2="680" y2="620"/>
        <line x1="800" y1="80" x2="800" y2="620"/>
        <line x1="920" y1="80" x2="920" y2="620"/>
        <line x1="1040" y1="80" x2="1040" y2="620"/>
      </g>

      <text x="70" y="135" font-size="13" fill="#111">Bornier X1</text>

      <rect x="80" y="150" width="950" height="30" fill="none" stroke="#111" stroke-width="1.5"/>
      <line x1="180" y1="150" x2="180" y2="180" stroke="#111" stroke-width="1.5"/>
      <line x1="560" y1="150" x2="560" y2="180" stroke="#111" stroke-width="1.5"/>
      <text x="95" y="170" font-size="12" fill="#111">Repère</text>
      <text x="230" y="170" font-size="12" fill="#111">Fonction</text>
      <text x="610" y="170" font-size="12" fill="#111">Extérieur</text>

      <rect x="80" y="190" width="950" height="26" fill="none" stroke="#111"/>
      <line x1="180" y1="190" x2="180" y2="216" stroke="#111"/>
      <line x1="560" y1="190" x2="560" y2="216" stroke="#111"/>
      <text x="100" y="208" font-size="11" fill="#111">1</text>
      <text x="195" y="208" font-size="11" fill="#111">Sonde TT1 entrée batterie</text>
      <text x="610" y="208" font-size="11" fill="#111">Champ</text>

      <rect x="80" y="220" width="950" height="26" fill="none" stroke="#111"/>
      <line x1="180" y1="220" x2="180" y2="246" stroke="#111"/>
      <line x1="560" y1="220" x2="560" y2="246" stroke="#111"/>
      <text x="100" y="238" font-size="11" fill="#111">2</text>
      <text x="195" y="238" font-size="11" fill="#111">Sonde TT2 reprise</text>
      <text x="610" y="238" font-size="11" fill="#111">Champ</text>

      <rect x="80" y="250" width="950" height="26" fill="none" stroke="#111"/>
      <line x1="180" y1="250" x2="180" y2="276" stroke="#111"/>
      <line x1="560" y1="250" x2="560" y2="276" stroke="#111"/>
      <text x="100" y="268" font-size="11" fill="#111">3</text>
      <text x="195" y="268" font-size="11" fill="#111">Sortie 0-10V AO+</text>
      <text x="610" y="268" font-size="11" fill="#111">Actionneur YV1</text>

      <rect x="80" y="280" width="950" height="26" fill="none" stroke="#111"/>
      <line x1="180" y1="280" x2="180" y2="306" stroke="#111"/>
      <line x1="560" y1="280" x2="560" y2="306" stroke="#111"/>
      <text x="100" y="298" font-size="11" fill="#111">4</text>
      <text x="195" y="298" font-size="11" fill="#111">Sortie 0-10V AO-</text>
      <text x="610" y="298" font-size="11" fill="#111">Actionneur YV1</text>

      <rect x="80" y="310" width="950" height="26" fill="none" stroke="#111"/>
      <line x1="180" y1="310" x2="180" y2="336" stroke="#111"/>
      <line x1="560" y1="310" x2="560" y2="336" stroke="#111"/>
      <text x="100" y="328" font-size="11" fill="#111">5</text>
      <text x="195" y="328" font-size="11" fill="#111">Commande pompe</text>
      <text x="610" y="328" font-size="11" fill="#111">KM1</text>

      <rect x="80" y="340" width="950" height="26" fill="none" stroke="#111"/>
      <line x1="180" y1="340" x2="180" y2="366" stroke="#111"/>
      <line x1="560" y1="340" x2="560" y2="366" stroke="#111"/>
      <text x="100" y="358" font-size="11" fill="#111">6</text>
      <text x="195" y="358" font-size="11" fill="#111">Retour neutre</text>
      <text x="610" y="358" font-size="11" fill="#111">N</text>

      <rect x="80" y="370" width="950" height="26" fill="none" stroke="#111"/>
      <line x1="180" y1="370" x2="180" y2="396" stroke="#111"/>
      <line x1="560" y1="370" x2="560" y2="396" stroke="#111"/>
      <text x="100" y="388" font-size="11" fill="#111">7</text>
      <text x="195" y="388" font-size="11" fill="#111">Commande ventilation</text>
      <text x="610" y="388" font-size="11" fill="#111">KV1</text>

      <rect x="80" y="400" width="950" height="26" fill="none" stroke="#111"/>
      <line x1="180" y1="400" x2="180" y2="426" stroke="#111"/>
      <line x1="560" y1="400" x2="560" y2="426" stroke="#111"/>
      <text x="100" y="418" font-size="11" fill="#111">8</text>
      <text x="195" y="418" font-size="11" fill="#111">Info dégivrage</text>
      <text x="610" y="418" font-size="11" fill="#111">Entrée REG</text>

      <rect x="20" y="640" width="1160" height="30" fill="none" stroke="#222" stroke-width="1.5"/>
      <line x1="1000" y1="640" x2="1000" y2="670" stroke="#222" stroke-width="1.5"/>
      <line x1="1090" y1="640" x2="1090" y2="670" stroke="#222" stroke-width="1.5"/>
      <text x="30" y="660" font-size="12" fill="#111">Folio bornier</text>
      <text x="1015" y="660" font-size="12" fill="#111">Folio</text>
      <text x="1115" y="660" font-size="12" fill="#111">12</text>
    </svg>
    """


def build_nomenclature_svg():
    return (
        '<svg width="1200" height="700" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff">'
        '<rect x="20" y="20" width="1160" height="660" fill="none" stroke="#222" stroke-width="1.5"/>'

        '<text x="40" y="45" font-size="18" fill="#111">COFFRET TYPE FROID MONO-VENTIL</text>'
        '<text x="40" y="95" font-size="18" fill="#111">Nomenclature simplifiée</text>'

        '<g stroke="#d0d0d0" stroke-width="1" stroke-dasharray="4 4">'
        '<line x1="80" y1="80" x2="80" y2="620"/>'
        '<line x1="200" y1="80" x2="200" y2="620"/>'
        '<line x1="320" y1="80" x2="320" y2="620"/>'
        '<line x1="440" y1="80" x2="440" y2="620"/>'
        '<line x1="560" y1="80" x2="560" y2="620"/>'
        '<line x1="680" y1="80" x2="680" y2="620"/>'
        '<line x1="800" y1="80" x2="800" y2="620"/>'
        '<line x1="920" y1="80" x2="920" y2="620"/>'
        '<line x1="1040" y1="80" x2="1040" y2="620"/>'
        '</g>'

        '<rect x="80" y="150" width="950" height="30" fill="none" stroke="#111" stroke-width="1.5"/>'
        '<line x1="180" y1="150" x2="180" y2="180" stroke="#111" stroke-width="1.5"/>'
        '<line x1="820" y1="150" x2="820" y2="180" stroke="#111" stroke-width="1.5"/>'
        '<text x="95" y="170" font-size="12" fill="#111">Repère</text>'
        '<text x="230" y="170" font-size="12" fill="#111">Désignation</text>'
        '<text x="875" y="170" font-size="12" fill="#111">Qté</text>'

        '<rect x="80" y="190" width="950" height="24" fill="none" stroke="#111"/>'
        '<line x1="180" y1="190" x2="180" y2="214" stroke="#111"/>'
        '<line x1="820" y1="190" x2="820" y2="214" stroke="#111"/>'
        '<text x="100" y="207" font-size="11" fill="#111">IG1</text>'
        '<text x="200" y="207" font-size="11" fill="#111">Interrupteur général</text>'
        '<text x="885" y="207" font-size="11" fill="#111">1</text>'

        '<rect x="80" y="216" width="950" height="24" fill="none" stroke="#111"/>'
        '<line x1="180" y1="216" x2="180" y2="240" stroke="#111"/>'
        '<line x1="820" y1="216" x2="820" y2="240" stroke="#111"/>'
        '<text x="100" y="233" font-size="11" fill="#111">Q1</text>'
        '<text x="200" y="233" font-size="11" fill="#111">Protection générale</text>'
        '<text x="885" y="233" font-size="11" fill="#111">1</text>'

        '<rect x="80" y="242" width="950" height="24" fill="none" stroke="#111"/>'
        '<line x1="180" y1="242" x2="180" y2="266" stroke="#111"/>'
        '<line x1="820" y1="242" x2="820" y2="266" stroke="#111"/>'
        '<text x="100" y="259" font-size="11" fill="#111">DM1</text>'
        '<text x="200" y="259" font-size="11" fill="#111">Protection moteur pompe</text>'
        '<text x="885" y="259" font-size="11" fill="#111">1</text>'

        '<rect x="80" y="268" width="950" height="24" fill="none" stroke="#111"/>'
        '<line x1="180" y1="268" x2="180" y2="292" stroke="#111"/>'
        '<line x1="820" y1="268" x2="820" y2="292" stroke="#111"/>'
        '<text x="100" y="285" font-size="11" fill="#111">QF</text>'
        '<text x="200" y="285" font-size="11" fill="#111">Protection ventilation</text>'
        '<text x="885" y="285" font-size="11" fill="#111">1</text>'

        '<rect x="80" y="294" width="950" height="24" fill="none" stroke="#111"/>'
        '<line x1="180" y1="294" x2="180" y2="318" stroke="#111"/>'
        '<line x1="820" y1="294" x2="820" y2="318" stroke="#111"/>'
        '<text x="100" y="311" font-size="11" fill="#111">KM1</text>'
        '<text x="200" y="311" font-size="11" fill="#111">Contacteur pompe</text>'
        '<text x="885" y="311" font-size="11" fill="#111">1</text>'

        '<rect x="80" y="320" width="950" height="24" fill="none" stroke="#111"/>'
        '<line x1="180" y1="320" x2="180" y2="344" stroke="#111"/>'
        '<line x1="820" y1="320" x2="820" y2="344" stroke="#111"/>'
        '<text x="100" y="337" font-size="11" fill="#111">KV1</text>'
        '<text x="200" y="337" font-size="11" fill="#111">Relais ventilation</text>'
        '<text x="885" y="337" font-size="11" fill="#111">1</text>'

        '<rect x="80" y="346" width="950" height="24" fill="none" stroke="#111"/>'
        '<line x1="180" y1="346" x2="180" y2="370" stroke="#111"/>'
        '<line x1="820" y1="346" x2="820" y2="370" stroke="#111"/>'
        '<text x="100" y="363" font-size="11" fill="#111">T1</text>'
        '<text x="200" y="363" font-size="11" fill="#111">Transformateur alimentation commande</text>'
        '<text x="885" y="363" font-size="11" fill="#111">1</text>'

        '<rect x="80" y="372" width="950" height="24" fill="none" stroke="#111"/>'
        '<line x1="180" y1="372" x2="180" y2="396" stroke="#111"/>'
        '<line x1="820" y1="372" x2="820" y2="396" stroke="#111"/>'
        '<text x="100" y="389" font-size="11" fill="#111">A1</text>'
        '<text x="200" y="389" font-size="11" fill="#111">Régulateur MPX PRO</text>'
        '<text x="885" y="389" font-size="11" fill="#111">1</text>'

        '<rect x="80" y="398" width="950" height="24" fill="none" stroke="#111"/>'
        '<line x1="180" y1="398" x2="180" y2="422" stroke="#111"/>'
        '<line x1="820" y1="398" x2="820" y2="422" stroke="#111"/>'
        '<text x="100" y="415" font-size="11" fill="#111">X1</text>'
        '<text x="200" y="415" font-size="11" fill="#111">Bornier extérieur</text>'
        '<text x="885" y="415" font-size="11" fill="#111">1</text>'

        '<rect x="80" y="424" width="950" height="24" fill="none" stroke="#111"/>'
        '<line x1="180" y1="424" x2="180" y2="448" stroke="#111"/>'
        '<line x1="820" y1="424" x2="820" y2="448" stroke="#111"/>'
        '<text x="100" y="441" font-size="11" fill="#111">YV1</text>'
        '<text x="200" y="441" font-size="11" fill="#111">Actionneur vanne 3 voies 0-10V</text>'
        '<text x="885" y="441" font-size="11" fill="#111">1</text>'

        '<rect x="80" y="450" width="950" height="24" fill="none" stroke="#111"/>'
        '<line x1="180" y1="450" x2="180" y2="474" stroke="#111"/>'
        '<line x1="820" y1="450" x2="820" y2="474" stroke="#111"/>'
        '<text x="100" y="467" font-size="11" fill="#111">TT1</text>'
        '<text x="200" y="467" font-size="11" fill="#111">Sonde entrée batterie</text>'
        '<text x="885" y="467" font-size="11" fill="#111">1</text>'

        '<rect x="80" y="476" width="950" height="24" fill="none" stroke="#111"/>'
        '<line x1="180" y1="476" x2="180" y2="500" stroke="#111"/>'
        '<line x1="820" y1="476" x2="820" y2="500" stroke="#111"/>'
        '<text x="100" y="493" font-size="11" fill="#111">TT2</text>'
        '<text x="200" y="493" font-size="11" fill="#111">Sonde reprise</text>'
        '<text x="885" y="493" font-size="11" fill="#111">1</text>'

        '<rect x="20" y="640" width="1160" height="30" fill="none" stroke="#222" stroke-width="1.5"/>'
        '<line x1="1000" y1="640" x2="1000" y2="670" stroke="#222" stroke-width="1.5"/>'
        '<line x1="1090" y1="640" x2="1090" y2="670" stroke="#222" stroke-width="1.5"/>'
        '<text x="30" y="660" font-size="12" fill="#111">Nomenclature simplifiée</text>'
        '<text x="1015" y="660" font-size="12" fill="#111">Folio</text>'
        '<text x="1115" y="660" font-size="12" fill="#111">13</text>'

        '</svg>'
    )
