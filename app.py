import streamlit as st
import streamlit.components.v1 as components

from folio_power import svg_power
from folio_command import svg_command
from folio_bornier import svg_bornier
from folio_nomenclature import svg_nomenclature

st.set_page_config(page_title="Générateur de schéma électrique", layout="wide")

st.title("Générateur de schéma électrique")

st.subheader("Analyse fonctionnelle")
analyse = st.text_area(
    "",
    "Batterie eau glycolée avec circulateur commandé par relais froid via KM1, "
    "ventilateur commandé directement par le relais ventilation du MXPRO, "
    "vanne 3 voies modulante 24V avec 0/10V, sondes reprise et glycol, dégivrage naturel.",
    height=160,
)

tabs = st.tabs(["Résumé", "Puissance", "Commande", "Bornier", "Nomenclature"])

with tabs[0]:
    st.subheader("Résumé de fonctionnement")
    st.write("Cas de référence figé")
    st.write("• Circulateur M1 en puissance via contact KM1")
    st.write("• Bobine KM1 pilotée en commande par relais froid MXPRO")
    st.write("• Ventilateur commandé directement par relais ventilation MXPRO")
    st.write("• Vanne 3 voies modulante alimentée en 24V")
    st.write("• Signal 0/10V vers YV1")
    st.write("• Sondes : glycol + reprise")
    st.write("• Bornier X1 représenté sur les liaisons terrain")
    st.write("• Renvois inter-folios visibles")

with tabs[1]:
    st.subheader("Folio 10 - Puissance")
    components.html(svg_power(), height=760, scrolling=True)

with tabs[2]:
    st.subheader("Folio 11 - Commande")
    components.html(svg_command(), height=760, scrolling=True)

with tabs[3]:
    st.subheader("Folio 15 - Bornier")
    components.html(svg_bornier(), height=760, scrolling=True)

with tabs[4]:
    st.subheader("Folio 20 - Nomenclature")
    components.html(svg_nomenclature(), height=760, scrolling=True)
