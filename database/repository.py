from pathlib import Path
import csv

PASTA_PROJETO = Path(__file__).resolve().parent.parent
PASTA_DADOS = PASTA_PROJETO / "database" / "dados"

colunas_notebooks = ["id", "estado", "professor"]


def ler_arquivo(arq):
    with open(arq, "r", newline="", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        usuarios = list(leitor)

    return usuarios


def escrever_arquivo(arq, colunas, dados):
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
    
    if notebook["professor"] == professor_id:
        return True
    else:
        raise ValueError("Este notebook não está emprestado para você")

def devolver(notebook_id):
    notebooks = ler_arquivo(PASTA_DADOS / "notebooks.csv")
    
    encontrado = False
    for notebook in notebooks:
        if notebook["id"] == notebook_id:
            notebook["estado"] = "disponivel"
            notebook["professor"] = "-"
            encontrado = True
            break
            
    if not encontrado:
        raise ValueError("o notebook não existe")

    escrever_arquivo(PASTA_DADOS / "notebooks.csv", colunas_notebooks, notebooks)


def recolher_notebook(notebook_id, professor_id):
    notebooks = ler_arquivo(PASTA_DADOS / "notebooks.csv")

    encontrado = False
    for notebook in notebooks:
        if notebook["id"] == notebook_id:
            notebook["estado"] = "emprestado"
            notebook["professor"] = professor_id
            encontrado = True
            break
            
    if not encontrado:
        raise ValueError("o notebook não existe")

    escrever_arquivo(PASTA_DADOS / "notebooks.csv", colunas_notebooks, notebooks)
