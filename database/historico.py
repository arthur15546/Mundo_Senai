from pathlib import Path
import csv
import time
from threading import Lock

PASTA_PROJETO = Path(__file__).resolve().parent.parent
PASTA_DADOS = PASTA_PROJETO / "database" / "dados"
ARQUIVO_HISTORICO = PASTA_DADOS / "historico_diario.csv"
COLUNAS_HISTORICO = ["id", "horario", "notebook", "professor", "acao"]
_LOCK_HISTORICO = Lock()


def _proximo_id():
    with open(ARQUIVO_HISTORICO, "rb") as arquivo:
        arquivo.seek(0, 2)
        posicao = arquivo.tell()

        while posicao > 0:
            posicao -= 1
            arquivo.seek(posicao)
            if arquivo.read(1) not in (b"\n", b"\r"):
                break

        fim_linha = posicao + 1
        while posicao > 0:
            arquivo.seek(posicao - 1)
            if arquivo.read(1) == b"\n":
                break
            posicao -= 1

        arquivo.seek(posicao)
        ultima_linha = arquivo.read(fim_linha - posicao).decode("utf-8").strip()

    if not ultima_linha:
        return 0

    ultimo_registro = next(csv.reader([ultima_linha]))
    if ultimo_registro[0] == "id":
        return 0

    return int(ultimo_registro[0]) + 1


def registrar_historico(notebook, professor_id, acao):
    with _LOCK_HISTORICO:
        novo_id = _proximo_id()
        horario = time.strftime("%X")

        with open(ARQUIVO_HISTORICO, "a", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow([novo_id, horario, notebook, professor_id, acao])


def ler_historico():
    with _LOCK_HISTORICO:
        with open(ARQUIVO_HISTORICO, "r", newline="", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo)
            return list(leitor)


def apagar_historico():
    with _LOCK_HISTORICO:
        with open(ARQUIVO_HISTORICO, "w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(COLUNAS_HISTORICO)