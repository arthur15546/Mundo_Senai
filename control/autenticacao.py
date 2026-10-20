from database.repository import encontrar_usuario

def autenticacao():
    cracha = input("cracha: ")
    usuario = encontrar_usuario(cracha)
    if usuario["funcao"] == "professor":
        return 1
    elif usuario["funcao"] == "monitor":
        return 2
    else:
        return 0

