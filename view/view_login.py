import streamlit as st
from control.autenticacao import autenticacao

def pagina_login():
    st.set_page_config(
        layout="wide",
        page_title="Mundo Senai",
        page_icon=":computer:",)

    st.markdown("""
        <style>
            .stForm {
                width: 50%;
                margin: auto;
            }

            .titulo {
                width: 50%;
                margin: auto;
                text-align: center;
            }
        </style>

        <div class="titulo">
            <h1>SESI - SENAI</h1>
            <h2>Sistema de Empréstimo de Notebooks</h2>
        </div>
    """, unsafe_allow_html=True)


    if st.session_state.pop("limpar_cracha", False):
        st.session_state.cracha = ""

    with st.form("form_cracha"):
        cracha = st.text_input("Escaneie seu crachá", key="cracha")
        enviar = st.form_submit_button("Entrar")

    if enviar:
        usuario = autenticacao(cracha)

        if usuario is not None:
            funcoes = {"professor": 1, "monitor": 2}
            funcao = funcoes.get(usuario["funcao"])
            if funcao is None:
                st.error("Perfil de usuário inválido")
                return

            st.session_state.funcao = funcao

            st.session_state.professor_id = usuario["id"]
            st.session_state.professor_nome = usuario["nome"]
            st.rerun()

        else:
            st.error("Usuário não encontrado")
            st.session_state.limpar_cracha = True
            st.rerun()