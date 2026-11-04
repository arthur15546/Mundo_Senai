import streamlit as st
from control.emprestimo import (
    devolver_notebook,
    recolher_notebook,
    validar_devolucao,
    validar_emprestimo,
)
from database.repository import listar_notebooks_emprestados_por_professor

def pagina_professor():
    st.set_page_config(
        layout="wide",
        page_title="Mundo Senai",
        page_icon=":computer:",)

    mensagem_sucesso = st.session_state.pop("mensagem_sucesso", None)
    if mensagem_sucesso:
        st.success(mensagem_sucesso)

    professor_id = st.session_state.professor_id
    professor_nome = st.session_state.professor_nome

    st.markdown(f"""
        <style>
        div[data-testid="stTextInput"] {{
            width: 75%;
            margin: 0 auto;
        }}

        div[data-testid="stTextInput"] input {{
            height: 50px;
            font-size: 18px;
        }}

        div[data-testid="stMainBlockContainer"] {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 85vh;
        }}

        .titulo {{
            width: 75%;
            margin: auto;
            text-align: center;
        }}
        </style>

        <div class="titulo">
            <h1>Bem vindo</h1>
            <h2>Professor {professor_nome}</h2>
        </div>
        

    """, unsafe_allow_html=True)

    with st.sidebar:
        st.write(f"Logado como: **{st.session_state.get('professor_nome', 'Usuário')}**")
        if st.button("Sair", type="primary"):
            st.session_state.clear()
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

        notebooks_emprestados = listar_notebooks_emprestados_por_professor(professor_id)
        if notebooks_emprestados:
            st.dataframe(
                notebooks_emprestados,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Nenhum notebook emprestado no momento.")
        

    estado_inicial = {
        "notebooks_listados": [],
        "notebook_selecionado": "",
        "notebook_processar": "",
        "notebooks_recolher": [],
    }
    for chave, valor_inicial in estado_inicial.items():
        if chave not in st.session_state:
            st.session_state[chave] = valor_inicial
            

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
                validar_emprestimo(notebook_recolhimento, professor_id)
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
    col1, col2, col3 = st.columns([0.5, 3, 0.5])
    with col2:
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
                                recolher_notebook(notebook, professor_id)
                            except ValueError as error:
                                st.error(f"Erro ao recolher notebook {notebook}: {error}")
                                recolhimento_concluido = False
                                st.session_state.notebooks_recolher = []
                                break

                            st.session_state.notebooks_recolher.remove(notebook)

                        if recolhimento_concluido:
                            st.session_state.notebook_processar = ""
                            st.session_state.notebooks_recolher = []
                            st.session_state.mensagem_sucesso = "Notebooks recolhidos com sucesso!"
                            st.rerun()

            elif acao_notebook == "Devolução":
                if len(st.session_state.notebooks_listados) > 0:
                    if st.button("Devolver notebooks", key="confirmar_devolucao"):
                        devolucao_concluida = True
                        for notebook in st.session_state.notebooks_listados.copy():
                            try:
                                devolver_notebook(notebook, professor_id)
                            except ValueError as error:
                                st.error(f"Erro ao devolver notebook {notebook}: {error}")
                                devolucao_concluida = False
                                st.session_state.notebooks_listados = []
                                break
                
                            st.session_state.notebooks_listados.remove(notebook)
                
                        if devolucao_concluida:
                            st.session_state.notebook_processar = ""
                            st.session_state.notebooks_listados = []
                            st.session_state.mensagem_sucesso = "Notebooks devolvidos com sucesso!"
                            st.rerun()