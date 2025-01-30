def main():
    print("Bem-vindo ao Chat Distribuído!")
    usuario = input("Digite seu nome de usuário: ")
    sala = input("Digite o nome da sala: ")

    entrar_sala(sala, usuario)

    while True:
        mensagem = input(f"[{sala}] {usuario}: ")
        if mensagem.lower() == "sair":
            break
        enviar_mensagem(sala, usuario, mensagem)

if __name__ == "__main__":
    main()