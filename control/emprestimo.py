from database.repository import notebook_disponivel, emprestado_corretamente, devolver
def devolver_notebook(notebook_id, professor_id):
    try:
        disponibilidade = notebook_disponivel(notebook_id)
    except ValueError as erro:
        raise ValueError(erro)

    try:
        emprestado_corretamente(notebook_id, professor_id)
    except ValueError as erro:
        raise ValueError(erro)

    if disponibilidade == False:
        devolver(notebook_id)


        

    