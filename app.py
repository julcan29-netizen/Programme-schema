import streamlit as st

st.set_page_config(layout="wide")

st.title("Générateur de schéma intelligent")

# -------------------------
# INPUT UTILISATEUR
# -------------------------
text = st.text_area("Décris ton installation")

# -------------------------
# ANALYSE TEXTE
# -------------------------
def analyze_text(text: str) -> dict:
    text = text.lower()

    return {
        "has_temp_sensor": "sonde" in text or "temp" in text,
        "has_3way_valve": "vanne" in text or "3 voies" in text,
        "has_pump": "pompe" in text,
        "has_fan": "ventil" in text,
        "has_defrost": "dégivrage" in text or "degivrage" in text,
        "setpoint": "+4°C" if "4" in text else None,
        "pump_on": "12°C" if "12" in text else None,
        "pump_off": "10°C" if "10" in text else None,
    }

# -------------------------
# VUE GLOBALE
# -------------------------
def build_global_mermaid(data: dict) -> str:
    lines = [
        "flowchart TD",
        "A[Analyse fonctionnelle]",
        "REG[Controleur]",
        "A --> REG",
    ]

    if data["has_temp_sensor"]:
        lines += [
            "TT1[Sonde entree]",
            "TT2[Sonde reprise]",
            "TT1 --> REG",
            "TT2 --> REG",
        ]

    if data["has_3way_valve"]:
        lines += [
            "V3V[Vanne 3 voies]",
            "REG -->|0-10V| V3V",
        ]

    if data["has_pump"]:
        lines += [
            "P1[Pompe]",
            "REG -->|Marche| P1",
        ]

    if data["has_fan"]:
        lines += [
            "FAN[Ventilation]",
            "REG --> FAN",
        ]

    if data["has_defrost"]:
        lines += [
            "DEG[Degivrage]",
            "REG --> DEG",
        ]

    return "\n".join(lines)

# -------------------------
# LOGIQUE
# -------------------------
def build_function_mermaid(data: dict) -> str:
    lines = [
        "flowchart TD",
        "START[Temperature mesuree]",
    ]

    if data["has_temp_sensor"]:
        lines += [
            "TT2[Sonde reprise]",
            "TT1[Sonde entree]",
            "TT2 --> START",
            "TT1 --> START",
        ]

    if data["pump_on"] or data["pump_off"]:
        on_txt = (data["pump_on"] or "seuil").replace("°", "")
        off_txt = (data["pump_off"] or "seuil").replace("°", "")

        lines += [
            f"D1{{T reprise > {on_txt} ?}}",
            "START --> D1",
            "PON[Pompe ON]",
            f"D2{{T reprise < {off_txt} ?}}",
            "D1 -->|Oui| PON",
            "D1 -->|Non| D2",
            "POFF[Pompe OFF]",
            "D2 -->|Oui| POFF",
        ]

    if data["has_3way_valve"]:
        sp = (data["setpoint"] or "consigne").replace("°", "")

        lines += [
            "REG[Regulation]",
            f"SP[Consigne {sp}]",
            "START --> REG",
            "SP --> REG",
            "V3V[Vanne]",
            "REG --> V3V",
        ]

    if data["has_defrost"]:
        lines += [
            "DEG[Degivrage]",
            "BYP[Bypass]",
            "DEG --> BYP",
        ]

        if data["has_pump"]:
            lines += ["DEG --> POFF"]

        if data["has_fan"]:
            lines += [
                "FANON[Ventilation ON]",
                "DEG --> FANON",
            ]

    return "\n".join(lines)

# -------------------------
# PUISSANCE
# -------------------------
def build_power_mermaid(data: dict) -> str:
    lines = [
        "flowchart LR",
        "ALIM[Alimentation]",
    ]

    if data["has_pump"]:
        lines += [
            "QF1[Protection pompe]",
            "KM1[Contacteur]",
            "M1[Moteur pompe]",
            "ALIM --> QF1 --> KM1 --> M1",
        ]

    if data["has_fan"]:
        lines += [
            "QF2[Protection ventil]",
            "MV1[Moteur ventil]",
            "ALIM --> QF2 --> MV1",
        ]

    if data["has_3way_valve"]:
        lines += [
            "PS1[Alim regul]",
            "YV1[Actionneur vanne]",
            "ALIM --> PS1 --> YV1",
        ]

    return "\n".join(lines)

# -------------------------
# COMMANDE
# -------------------------
def build_control_mermaid(data: dict) -> str:
    lines = [
        "flowchart LR",
        "REG[Controleur]",
    ]

    if data["has_temp_sensor"]:
        lines += [
            "TT1[Sonde entree]",
            "TT2[Sonde reprise]",
            "TT1 --> REG",
            "TT2 --> REG",
        ]

    if data["has_pump"]:
        lines += [
            "KM1[Relais pompe]",
            "REG --> KM1",
        ]

    if data["has_3way_valve"]:
        lines += [
            "YV1[0-10V vanne]",
            "REG --> YV1",
        ]

    if data["has_defrost"]:
        lines += [
            "DEG[Degivrage]",
            "DEG --> REG",
        ]

    return "\n".join(lines)

# -------------------------
# AFFICHAGE
# -------------------------
if st.button("Générer"):

    data = analyze_text(text)

    tab1, tab2, tab3, tab4 = st.tabs([
        "Vue globale",
        "Logique",
        "Puissance",
        "Commande"
    ])

    with tab1:
        st.subheader("Vue globale")
        st.code(build_global_mermaid(data), language="mermaid")

    with tab2:
        st.subheader("Logique")
        st.code(build_function_mermaid(data), language="mermaid")

    with tab3:
        st.subheader("Puissance")
        st.code(build_power_mermaid(data), language="mermaid")

    with tab4:
        st.subheader("Commande")
        st.code(build_control_mermaid(data), language="mermaid")
