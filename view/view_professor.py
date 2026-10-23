import streamlit as st
from control.emprestimo import devolver_notebook, recolher_notebook


def pagina_professor():
    st.set_page_config(
        layout="wide",
        page_title="Mundo Senai",
        page_icon=":computer:",)

    with st.sidebar:
        st.write(f"Logado como: **{st.session_state.get('professor_nome', 'Usuário')}**")
        if st.button("Sair", type="primary"):
            st.session_state.funcao = None
            st.session_state.pop("professor_id", None)
            st.session_state.pop("professor_nome", None)
            st.rerun()

    professor_id = st.session_state.professor_id
    professor_nome = st.session_state.professor_nome

    st.title("pagina do professor")
    st.subheader(f"Bem-vindo, {professor_nome}!")

    col1, col2 = st.columns(2)

    with col1:
        pass
    with col2:
        st.subheader("Gerenciar notebooks")

        if "notebook_selecionado" not in st.session_state:
            st.session_state.notebook_selecionado = ""

        if "notebook_processar" not in st.session_state:
            st.session_state.notebook_processar = ""

        pagina = st.segmented_control(
            " ",
            ["Devolver notebook", "Recolher notebook"],
            default = "Devolver notebook"
        )

        if pagina == "Devolver notebook":
            st.text_input("scaneie o número do notebook a ser devolvido",
                           key="notebook_selecionado",
                           on_change=lambda: st.session_state.update(
                                notebook_processar=st.session_state.notebook_selecionado,
                                notebook_selecionado =""))
            
            notebook_selecionado = st.session_state.notebook_processar


            
