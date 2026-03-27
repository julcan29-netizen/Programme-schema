import streamlit as st

# ==============================
# DEBUG GLOBAL
# ==============================
st.set_page_config(layout="wide")

st.title("APP FINAL CONTROL")

st.success("SI TU VOIS CE MESSAGE → APP.PY EST OK")

# ==============================
# IMPORT FORCÉ
# ==============================

try:
    import folio_power_v3
    st.success("IMPORT folio_power_v3 OK")
except Exception as e:
    st.error(f"ERREUR IMPORT folio_power_v3 : {e}")

# ==============================
# TEST RENDU DIRECT
# ==============================

st.warning("ON FORCE LE RENDU V3 CI-DESSOUS")

try:
    st.info("AVANT APPEL FOLIO V3")

    folio_power_v3.render_power_folio_streamlit()

    st.info("APRES APPEL FOLIO V3")

except Exception as e:
    st.error(f"ERREUR EXECUTION FOLIO V3 : {e}")
