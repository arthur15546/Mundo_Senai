
from database.repository import (
    notebook_disponivel,
    emprestado_corretamente,
    devolver,
    recolher_notebook as repo_recolher,
)


def devolver_notebook(notebook_id, professor_id):
    disponibilidade = notebook_disponivel(notebook_id)

    if disponibilidade:
        raise ValueError(
            "O notebook não está emprestado, portanto não pode ser devolvido"
        )

    emprestado_corretamente(notebook_id, professor_id)

    devolver(notebook_id)


def recolher_notebook(notebook_id, professor_id):
    disponibilidade = notebook_disponivel(notebook_id)

    if not disponibilidade:
        raise ValueError(
            "O notebook não está disponível para recolhimento"
        )

    repo_recolher(notebook_id, professor_id)
