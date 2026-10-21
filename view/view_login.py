import streamlit as st
from control.autenticacao import autenticacao

def pagina_login():
    st.set_page_config(
        layout="wide",
        page_title="Mundo Senai",
        page_icon=":computer:",)

    col1, col2 = st.columns(2)

    with col1:
        st.title("login")

    with col2:
        if st.session_state.pop("limpar_cracha", False):
            st.session_state.cracha = ""

        with st.form("form_cracha"):
            cracha = st.text_input("Escaneie seu crachá", key="cracha")
            enviar = st.form_submit_button("Entrar")

        if enviar:
            usuario = autenticacao(cracha)

            if usuario is not None:
                st.session_state.funcao = (
                    1 if usuario["funcao"] == "professor" else 2
                )

                st.session_state.professor_id = usuario["id"]
                st.session_state.professor_nome = usuario["nome"]
                st.rerun()

            else:
                st.session_state.limpar_cracha = True
                st.error("Usuário não encontrado")
                st.rerun()