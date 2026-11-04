from pathlib import Path
import csv
from threading import RLock

PASTA_PROJETO = Path(__file__).resolve().parent.parent
PASTA_DADOS = PASTA_PROJETO / "database" / "dados"

colunas_notebooks = ["id", "estado", "professor"]
_LOCK_DADOS = RLock()


def ler_arquivo(arq):
    with _LOCK_DADOS:
        with open(arq, "r", newline="", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo)
            usuarios = list(leitor)

    return usuarios


def escrever_arquivo(arq, colunas, dados):
    with _LOCK_DADOS:
        with open(arq, mode="w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=colunas)
            escritor.writeheader()
            escritor.writerows(dados)


def encontrar_usuario(cracha):
    usuarios = ler_arquivo(PASTA_DADOS / "usuarios.csv")

    usuario_encontrado = next(
    (u for u in usuarios if u["cracha"] == cracha),
    None)

    return usuario_encontrado


def identificar_notebook(id):
    notebooks = ler_arquivo(PASTA_DADOS / "notebooks.csv")
    for notebook in notebooks:
        if notebook["id"] == id:
            return notebook
    return None


def notebook_disponivel(id):
    notebook = identificar_notebook(id)
    if(notebook is None):
        raise ValueError("o notebook não existe")
    else:
        if notebook["estado"] == "disponivel":
            return True
        else:
            return False


def emprestado_corretamente(notebook_id, professor_id):
    notebook = identificar_notebook(notebook_id)
    if notebook is None:
        raise ValueError("o notebook não existe")
    professores = ler_arquivo(PASTA_DADOS / "usuarios.csv")
    professor = next((p for p in professores if p["id"] == str(professor_id)), None)
    
    if professor is None:
        raise ValueError("Professor não encontrado")

    if notebook["professor"] == str(professor_id) or professor["funcao"] == "monitor":
        return True
    else:
        raise ValueError("Este notebook não está emprestado para você")

def devolver(notebook_id, professor_id):
    with _LOCK_DADOS:
        notebooks = ler_arquivo(PASTA_DADOS / "notebooks.csv")
        notebook_encontrado = next(
            (notebook for notebook in notebooks if notebook["id"] == notebook_id),
            None,
        )

        if notebook_encontrado is None:
            raise ValueError("o notebook não existe")
        if notebook_encontrado["estado"] != "emprestado":
            raise ValueError("O notebook não está emprestado")

        professor = next(
            (
                usuario
                for usuario in ler_arquivo(PASTA_DADOS / "usuarios.csv")
                if usuario["id"] == str(professor_id)
            ),
            None,
        )
        if professor is None:
            raise ValueError("Professor não encontrado")
        if (
            professor["funcao"] != "monitor"
            and notebook_encontrado["professor"] != str(professor_id)
        ):
            raise ValueError("Este notebook não está emprestado para você")

        notebook_encontrado["estado"] = "disponivel"
        notebook_encontrado["professor"] = "-"
        escrever_arquivo(PASTA_DADOS / "notebooks.csv", colunas_notebooks, notebooks)


def recolher_notebook(notebook_id, professor_id):
    with _LOCK_DADOS:
        notebooks = ler_arquivo(PASTA_DADOS / "notebooks.csv")
        notebook_encontrado = next(
            (notebook for notebook in notebooks if notebook["id"] == notebook_id),
            None,
        )

        if notebook_encontrado is None:
            raise ValueError("o notebook não existe")
        if notebook_encontrado["estado"] != "disponivel":
            raise ValueError("O notebook não está disponível para recolhimento")

        professor = next(
            (
                usuario
                for usuario in ler_arquivo(PASTA_DADOS / "usuarios.csv")
                if usuario["id"] == str(professor_id)
            ),
            None,
        )
        if professor is None:
            raise ValueError("Professor não encontrado")
        if professor["funcao"] != "monitor":
            emprestados = sum(
                1
                for notebook in notebooks
                if notebook["estado"] == "emprestado"
                and notebook["professor"] == str(professor_id)
            )
            if emprestados >= 3:
                raise ValueError(
                    "Você atingiu o limite de notebooks emprestados (3). "
                    "Devolva um notebook antes de recolher outro."
                )

        notebook_encontrado["estado"] = "emprestado"
        notebook_encontrado["professor"] = str(professor_id)
        escrever_arquivo(PASTA_DADOS / "notebooks.csv", colunas_notebooks, notebooks)

def dentro_do_limite(professor_id):
    limite = 3
    professores = ler_arquivo(PASTA_DADOS / "usuarios.csv")
    professor = next((p for p in professores if p["id"] == str(professor_id)), None)
    if professor is None:
        raise ValueError("Professor não encontrado")
    if professor["funcao"] == "monitor":
        return True

    notebooks = ler_arquivo(PASTA_DADOS / "notebooks.csv")
    notebooks_emprestados = [n for n in notebooks if n["professor"] == str(professor_id)]
    
    return len(notebooks_emprestados) < limite

def listar_notebooks_emprestados():
    notebooks = ler_arquivo(PASTA_DADOS / "notebooks.csv")
    emprestados = [n for n in notebooks if n["estado"] == "emprestado"]
    emprestados = sorted(emprestados, key=lambda x: x["id"])
    return emprestados


def identificar_usuario(id):
    usuarios = ler_arquivo(PASTA_DADOS / "usuarios.csv")
    usuario_identificado = next(
        (u for u in usuarios if u["id"] == str(id)),
        None
    )
    if usuario_identificado is None:
        raise ValueError("Usuário não encontrado")
    return usuario_identificado

def listar_notebooks_emprestados_por_professor(professor_id):
    notebooks_emprestados = listar_notebooks_emprestados()
    notebooks_do_professor = [
        n for n in notebooks_emprestados if n["professor"] == str(professor_id)
    ]
    notebooks_do_professor = sorted(notebooks_do_professor, key=lambda x: x["id"])
    return notebooks_do_professor