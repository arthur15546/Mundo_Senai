import streamlit as st
from control.emprestimo import (
    devolver_notebook,
    recolher_notebook,
    validar_devolucao,
    validar_emprestimo,
)
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

    estado_inicial = {
        "monitor_notebooks_devolucao": [],
        "monitor_notebook_devolucao_selecionado": "",
        "monitor_notebook_devolucao_processar": "",
        "monitor_notebooks_recolhimento": [],
        "monitor_notebook_recolhimento_selecionado": "",
        "monitor_notebook_recolhimento_processar": "",
    }
    for chave, valor_inicial in estado_inicial.items():
        if chave not in st.session_state:
            st.session_state[chave] = valor_inicial

    st.title("pagina do monitor")
    st.subheader(f"Bem-vindo, {professor_nome}!")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Notebooks Emprestados")
        notebooks_emprestados = listar_notebooks_emprestados()
        
        if notebooks_emprestados:
            st.dataframe(
                notebooks_emprestados,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Nenhum notebook emprestado no momento.")

    with col2:
        st.subheader("Gerenciar notebooks")
        acao_notebook = st.segmented_control(
            " ",
            ["Devolver notebook", "Recolher notebook"],
            default="Devolver notebook",
        )

        if acao_notebook == "Devolver notebook":
            acao_devolucao = st.segmented_control(
                " ",
                ["Escolher", "Retirar"],
                default="Escolher",
                key="monitor_acao_devolucao",
            )

            st.text_input(
                "Escaneie o número do notebook a ser devolvido",
                key="monitor_notebook_devolucao_selecionado",
                on_change=lambda: st.session_state.update(
                    monitor_notebook_devolucao_processar=st.session_state.monitor_notebook_devolucao_selecionado,
                    monitor_notebook_devolucao_selecionado="",
                ),
            )
            notebook_devolucao = st.session_state.monitor_notebook_devolucao_processar

            if notebook_devolucao:
                if acao_devolucao == "Escolher":
                    try:
                        validar_devolucao(notebook_devolucao, professor_id)
                        if notebook_devolucao in st.session_state.monitor_notebooks_devolucao:
                            raise ValueError("O notebook já está na lista")
                    except ValueError as error:
                        st.error(str(error))
                    else:
                        st.session_state.monitor_notebooks_devolucao.append(notebook_devolucao)
                elif acao_devolucao == "Retirar":
                    if notebook_devolucao in st.session_state.monitor_notebooks_devolucao:
                        st.session_state.monitor_notebooks_devolucao.remove(notebook_devolucao)
                    else:
                        st.error("O notebook não está na lista")

                st.session_state.monitor_notebook_devolucao_processar = ""

            if st.session_state.monitor_notebooks_devolucao:
                st.write("Notebooks selecionados para devolução:")
                st.write(", ".join(st.session_state.monitor_notebooks_devolucao))

            if st.button("Devolver notebooks", key="monitor_confirmar_devolucao"):
                devolucao_concluida = True
                for notebook in st.session_state.monitor_notebooks_devolucao.copy():
                    try:
                        devolver_notebook(notebook, professor_id)
                    except ValueError as error:
                        st.error(f"Erro ao devolver notebook {notebook}: {error}")
                        devolucao_concluida = False
                        break

                    st.session_state.monitor_notebooks_devolucao.remove(notebook)

                if devolucao_concluida:
                    st.session_state.monitor_notebook_devolucao_processar = ""
                    st.success("Notebooks devolvidos com sucesso!")
                    st.rerun()

        elif acao_notebook == "Recolher notebook":
            acao_recolhimento = st.segmented_control(
                " ",
                ["Escolher", "Retirar"],
                default="Escolher",
                key="monitor_acao_recolhimento",
            )

            st.text_input(
                "Escaneie o número do notebook a ser recolhido",
                key="monitor_notebook_recolhimento_selecionado",
                on_change=lambda: st.session_state.update(
                    monitor_notebook_recolhimento_processar=st.session_state.monitor_notebook_recolhimento_selecionado,
                    monitor_notebook_recolhimento_selecionado="",
                ),
            )
            notebook_recolhimento = st.session_state.monitor_notebook_recolhimento_processar

            if notebook_recolhimento:
                if acao_recolhimento == "Escolher":
                    try:
                        validar_emprestimo(notebook_recolhimento, professor_id)
                        if notebook_recolhimento in st.session_state.monitor_notebooks_recolhimento:
                            raise ValueError("O notebook já está na lista")
                    except ValueError as error:
                        st.error(str(error))
                    else:
                        st.session_state.monitor_notebooks_recolhimento.append(notebook_recolhimento)
                elif acao_recolhimento == "Retirar":
                    if notebook_recolhimento in st.session_state.monitor_notebooks_recolhimento:
                        st.session_state.monitor_notebooks_recolhimento.remove(notebook_recolhimento)
                    else:
                        st.error("O notebook não está na lista")

                st.session_state.monitor_notebook_recolhimento_processar = ""

            if st.session_state.monitor_notebooks_recolhimento:
                st.write("Notebooks selecionados para recolhimento:")
                st.write(", ".join(st.session_state.monitor_notebooks_recolhimento))

            if st.button("Recolher notebooks", key="monitor_confirmar_recolhimento"):
                recolhimento_concluido = True
                for notebook in st.session_state.monitor_notebooks_recolhimento.copy():
                    try:
                        recolher_notebook(notebook, professor_id)
                    except ValueError as error:
                        st.error(f"Erro ao recolher notebook {notebook}: {error}")
                        recolhimento_concluido = False
                        break

                    st.session_state.monitor_notebooks_recolhimento.remove(notebook)

                if recolhimento_concluido:
                    st.session_state.monitor_notebook_recolhimento_processar = ""
                    st.success("Notebooks recolhidos com sucesso!")
                    st.rerun()
