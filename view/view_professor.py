import streamlit as st
from control.emprestimo import (
    devolver_notebook,
    recolher_notebook,
    validar_devolucao,
    validar_emprestimo,
)


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

    estado_inicial = {
        "notebooks_listados": [],
        "notebook_selecionado": "",
        "notebook_processar": "",
        "notebooks_recolher": [],
        "notebook_recolher_selecionado": "",
        "notebook_recolher_processar": "",
    }
    for chave, valor_inicial in estado_inicial.items():
        if chave not in st.session_state:
            st.session_state[chave] = valor_inicial

    st.title("pagina do professor")
    st.subheader(f"Bem-vindo, {professor_nome}!")

    col1, col2 = st.columns(2)

    with col1:
        pass
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
            )

            st.text_input(
                "scaneie o número do notebook a ser devolvido",
                key="notebook_selecionado",
                on_change=lambda: st.session_state.update(
                    notebook_processar=st.session_state.notebook_selecionado,
                    notebook_selecionado="",
                ),
            )

            notebook_devolucao = st.session_state.notebook_processar

            if notebook_devolucao:
                if acao_devolucao == "Escolher":
                    try:
                        validar_devolucao(notebook_devolucao, professor_id)
                        if notebook_devolucao in st.session_state.notebooks_listados:
                            raise ValueError("O notebook já está na lista")
                        if len(st.session_state.notebooks_listados) >= 3:
                            raise ValueError("Você atingiu o limite de notebooks por professor")
                    except ValueError as error:
                        st.session_state.notebook_processar = ""
                        st.error(str(error))

                    else:
                        st.session_state.notebooks_listados.append(notebook_devolucao)

                elif acao_devolucao == "Retirar":
                    if notebook_devolucao in st.session_state.notebooks_listados:
                        st.session_state.notebooks_listados.remove(notebook_devolucao)

                    else:
                        st.session_state.notebook_processar = ""
                        st.error("O notebook não está na lista")

                st.session_state.notebook_processar = ""

            if st.session_state.notebooks_listados:
                st.write("Notebooks selecionados para devolução:")
                st.write(", ".join(st.session_state.notebooks_listados))

            if st.button("Devolver notebooks", key="confirmar_devolucao"):
                devolucao_concluida = True
                for notebook in st.session_state.notebooks_listados.copy():
                    try:
                        devolver_notebook(notebook, professor_id)
                    except ValueError as error:
                        st.error(f"Erro ao devolver notebook {notebook}: {error}")
                        devolucao_concluida = False
                        break

                    st.session_state.notebooks_listados.remove(notebook)

                if devolucao_concluida:
                    st.session_state.notebook_processar = ""
                    st.success("Notebooks devolvidos com sucesso!")

        elif acao_notebook == "Recolher notebook":
            acao_recolhimento = st.segmented_control(
                " ",
                ["Escolher", "Retirar"],
                default="Escolher",
                key="acao_recolhimento_professor",
            )

            st.text_input(
                "Escaneie o número do notebook a ser recolhido",
                key="notebook_recolher_selecionado",
                on_change=lambda: st.session_state.update(
                    notebook_recolher_processar=st.session_state.notebook_recolher_selecionado,
                    notebook_recolher_selecionado="",
                ),
            )

            notebook_recolhimento = st.session_state.notebook_recolher_processar

            if notebook_recolhimento:
                if acao_recolhimento == "Escolher":
                    try:
                        validar_emprestimo(notebook_recolhimento, professor_id)
                        if notebook_recolhimento in st.session_state.notebooks_recolher:
                            raise ValueError("O notebook já está na lista")
                    except ValueError as error:
                        st.session_state.notebook_recolher_processar = ""
                        st.error(str(error))
                    else:
                        st.session_state.notebooks_recolher.append(notebook_recolhimento)

                elif acao_recolhimento == "Retirar":
                    if notebook_recolhimento in st.session_state.notebooks_recolher:
                        st.session_state.notebooks_recolher.remove(notebook_recolhimento)
                    else:
                        st.session_state.notebook_recolher_processar = ""
                        st.error("O notebook não está na lista")

                st.session_state.notebook_recolher_processar = ""

            if st.session_state.notebooks_recolher:
                st.write("Notebooks selecionados para recolhimento:")
                st.write(", ".join(st.session_state.notebooks_recolher))

            if st.button("Recolher notebooks"):
                recolhimento_concluido = True
                for notebook in st.session_state.notebooks_recolher.copy():
                    try:
                        recolher_notebook(notebook, professor_id)
                    except ValueError as error:
                        st.error(f"Erro ao recolher notebook {notebook}: {error}")
                        recolhimento_concluido = False
                        break

                    st.session_state.notebooks_recolher.remove(notebook)

                if recolhimento_concluido:
                    st.session_state.notebook_recolher_processar = ""
                    st.success("Notebooks recolhidos com sucesso!")
                    st.rerun()
