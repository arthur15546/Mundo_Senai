from database.repository import encontrar_usuario

def autenticacao(cracha):
    usuario = encontrar_usuario(cracha)
    
    if usuario is None: return None

    return usuario

