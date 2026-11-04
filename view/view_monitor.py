import streamlit as st
from control.emprestimo import (
    devolver_notebook,
    recolher_notebook,
    validar_devolucao,
    validar_emprestimo,
)
from database.repository import listar_notebooks_emprestados
from database.historico import ler_historico, apagar_historico


def pagina_monitor():
    st.set_page_config(
        layout="wide",
        page_title="Mundo Senai",
        page_icon=":computer:",)

    monitor_id = st.session_state.professor_id
    monitor_nome = st.session_state.professor_nome
    
    with st.sidebar:
        st.write(f"Logado como: **{st.session_state.get('professor_nome', 'Usuário')}**")
        if st.button("Sair", type="primary"):
            st.session_state.clear()
            st.rerun()

        if st.download_button(
            label="Baixar histórico",
            data="\n".join([",".join(h.values()) for h in ler_historico()]),
            file_name="historico_diario.csv",
            mime="text/csv"):
            pass

        if st.button("Apagar histórico", type="primary"):
            apagar_historico()
            st.rerun()

        acao_notebook = st.pills(
            " ",
            ["Emprestimo", "Devolução"],
            default="Emprestimo",
        )
        
        if acao_notebook == "Devolução":
            acao_devolucao = st.segmented_control(
                "lista de notebooks",
                ["Selecionar", "Desselecionar"],
                default="Selecionar",
            )
        elif acao_notebook == "Emprestimo":
            acao_recolhimento = st.segmented_control(
                "lista de notebooks",
                ["Selecionar", "Desselecionar"],
                default="Selecionar",
                key="acao_recolhimento_professor",
            )

    estado_inicial = {
        "notebooks_listados": [],
        "notebook_selecionado": "",
        "notebook_processar": "",
        "notebooks_recolher": [],
    }
    for chave, valor_inicial in estado_inicial.items():
        if chave not in st.session_state:
            st.session_state[chave] = valor_inicial

    st.title("Bem vindo")
    st.subheader(f"monitor {monitor_nome}!")

    col1, col2 = st.columns([3, 1])

    with col1:
        st.text_input(
                "scaneie o número do notebook",
                key="notebook_selecionado",
                on_change=lambda: st.session_state.update(
                    notebook_processar=st.session_state.notebook_selecionado,
                    notebook_selecionado="",
                ),
            )
            
        notebook_devolucao = None
        notebook_recolhimento = None

        if acao_notebook == "Devolução":
            notebook_devolucao = st.session_state.notebook_processar
        elif acao_notebook == "Emprestimo":
            notebook_recolhimento = st.session_state.notebook_processar

        if notebook_devolucao:
            if acao_devolucao == "Selecionar":
                try:
                    validar_devolucao(notebook_devolucao, monitor_id)
                    if notebook_devolucao in st.session_state.notebooks_listados:
                        raise ValueError("O notebook já está na lista")
                except ValueError as error:
                    st.session_state.notebook_processar = ""
                    st.error(str(error))

                else:
                    st.session_state.notebooks_listados.append(notebook_devolucao)

            elif acao_devolucao == "Desselecionar":
                if notebook_devolucao in st.session_state.notebooks_listados:
                    st.session_state.notebooks_listados.remove(notebook_devolucao)

                else:
                    st.session_state.notebook_processar = ""
                    st.error("O notebook não está na lista")

            st.session_state.notebook_processar = ""

        
        if notebook_recolhimento:
            if acao_recolhimento == "Selecionar":
                try:
                    validar_emprestimo(notebook_recolhimento, monitor_id)
                    if notebook_recolhimento in st.session_state.notebooks_recolher:
                        raise ValueError("O notebook já está na lista")
                except ValueError as error:
                    st.session_state.notebook_processar = ""
                    st.error(str(error))
                else:
                    st.session_state.notebooks_recolher.append(notebook_recolhimento)

            elif acao_recolhimento == "Desselecionar":
                if notebook_recolhimento in st.session_state.notebooks_recolher:
                    st.session_state.notebooks_recolher.remove(notebook_recolhimento)
                else:
                    st.session_state.notebook_processar = ""
                    st.error("O notebook não está na lista")

            st.session_state.notebook_processar = ""


    with col1:
        if acao_notebook == "Emprestimo":
            if st.session_state.notebooks_recolher:
                st.write("Notebooks selecionados para recolhimento:")
                st.write(", ".join(st.session_state.notebooks_recolher))

        elif acao_notebook == "Devolução":
            if st.session_state.notebooks_listados:
                st.write("Notebooks selecionados para devolução:")
                st.write(", ".join(st.session_state.notebooks_listados))   

        if acao_notebook == "Emprestimo":
            if len(st.session_state.notebooks_recolher) > 0:
                if st.button("Recolher notebooks", key="confirmar_recolhimento"):
                    recolhimento_concluido = True
                    for notebook in st.session_state.notebooks_recolher.copy():
                        try:
                            recolher_notebook(notebook, monitor_id)
                        except ValueError as error:
                            st.error(f"Erro ao recolher notebook {notebook}: {error}")
                            recolhimento_concluido = False
                            st.session_state.notebooks_recolher = []
                            break

                        st.session_state.notebooks_recolher.remove(notebook)

                    if recolhimento_concluido:
                        st.session_state.notebook_processar = ""
                        st.success("Notebooks recolhidos com sucesso!")
                        st.session_state.notebooks_recolher = []
                        st.rerun()

        elif acao_notebook == "Devolução":
            if len(st.session_state.notebooks_listados) > 0:
                if st.button("Devolver notebooks", key="confirmar_devolucao"):
                    devolucao_concluida = True
                    for notebook in st.session_state.notebooks_listados.copy():
                        try:
                            devolver_notebook(notebook, monitor_id)
                        except ValueError as error:
                            st.error(f"Erro ao devolver notebook {notebook}: {error}")
                            devolucao_concluida = False
                            st.session_state.notebooks_listados = []
                            break
            
                        st.session_state.notebooks_listados.remove(notebook)
            
                    if devolucao_concluida:
                        st.session_state.notebook_processar = ""
                        st.success("Notebooks devolvidos com sucesso!")
                        st.session_state.notebooks_listados = []
                        st.rerun()

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
        st.subheader("Histórico de Ações")
        historico = ler_historico()
        if historico:
            st.dataframe(
                historico,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Nenhuma ação registrada no histórico.")
    