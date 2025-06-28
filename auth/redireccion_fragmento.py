import streamlit as st
from streamlit_javascript import st_javascript

def redireccionar_fragmento_si_es_necesario():
    fragment = st_javascript("window.location.hash")

    if fragment:
        st.warning("🔄 Detectado fragmento en URL")

        params = fragment.lstrip("#")
        if "access_token=" in params:
            st.info(f"🔑 Token detectado en fragmento: {params[:30]}...")
            new_url = f"{st_javascript('window.location.origin')}?{params}"
            st.markdown(f"<script>window.location.replace('{new_url}');</script>", unsafe_allow_html=True)
            st.stop()
        else:
            st.warning("⚠️ Fragmento presente pero sin access_token")
