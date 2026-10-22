import streamlit as st
from view.view_login import pagina_login
from view.view_professor import pagina_professor
from view.view_monitor import pagina_monitor



if "funcao" not in st.session_state:
    st.session_state.funcao = None

if st.session_state.funcao is None:
    login = st.Page(
        pagina_login,
        title="Login",
        url_path="login"
    )

    pagina = st.navigation([login], position="hidden")

else:
    if st.session_state.funcao == 1:
        professor = st.Page(
            pagina_professor,
            title="Professor",
            url_path="professor"
        )
        pagina = st.navigation([professor], position="hidden")

    elif st.session_state.funcao == 2:
        monitor = st.Page(
            pagina_monitor,
            title="Monitor",
            url_path="monitor"
        )
        pagina = st.navigation([monitor], position="hidden")

    else:
        st.session_state.funcao = None
        st.rerun()

pagina.run()