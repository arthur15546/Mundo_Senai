import streamlit as st
from control.emprestimo import devolver_notebook, recolher_notebook
from database.repository import listar_notebooks_emprestados

def pagina_monitor():
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

    st.title("pagina do monitor")
    st.subheader(f"Bem-vindo, {professor_nome}!")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Notebooks Emprestados")
        
        # Busca os notebooks emprestados ordenados
        notebooks_emprestados = listar_notebooks_emprestados()
        
        if notebooks_emprestados:
            # Exibe em formato de tabela interativa no Streamlit
            st.dataframe(
                notebooks_emprestados,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Nenhum notebook emprestado no momento.")

    with col2:
        st.subheader("Gerenciar notebooks")    
        secao = st.radio(
            "O que você deseja fazer?",
            ["Recolher notebook", "Devolver notebook"],
            key="acao_notebook"
        )

        if secao == "Recolher notebook":
            if st.session_state.pop("limpar_notebook", False):
                st.session_state.notebook = ""

            with st.form("form_notebook"):
                notebook = st.text_input(
                    "Escaneie o notebook",
                    key="notebook"
                )
                recolher = st.form_submit_button("Recolher notebook")

            if recolher:
                try:
                    recolher_notebook(notebook, professor_id)
                    st.session_state.limpar_notebook = True
                    st.success("Notebook recolhido com sucesso!")
                    st.rerun()

                except ValueError as erro:
                    st.error(str(erro))
            

        elif secao == "Devolver notebook":
            st.write("Seção de devolução")

            if st.session_state.pop("limpar_notebook", False):
                            st.session_state.notebook = ""
            
            with st.form("form_notebook"):
                notebook = st.text_input(
                    "Escaneie o notebook",
                    key="notebook"
                )
                devolver = st.form_submit_button("Devolver notebook")

            if devolver:
                try:
                    devolver_notebook(notebook, professor_id)
                    st.session_state.limpar_notebook = True
                    st.success("Notebook devolvido com sucesso!")
                    st.rerun()

                except ValueError as erro:
                    st.error(str(erro))

