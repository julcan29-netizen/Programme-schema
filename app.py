import streamlit as st

st.title("Générateur de schéma simple")

text = st.text_area("Décris ton installation")

if st.button("Générer"):
    st.markdown(f"""
```mermaid
flowchart TD
A[Analyse] --> B[Installation]
B --> C[Pompe]
B --> D[Vanne]
B --> E[Ventilation]
