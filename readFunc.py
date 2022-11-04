
def readToken():
    """Funcao para ler um arquivo txt que contem apenas o bearer token

    Returns:
        string: o token contido no arquivo
    """
    with open('token.txt') as f:
        lines = f.readlines()
    return lines[0]