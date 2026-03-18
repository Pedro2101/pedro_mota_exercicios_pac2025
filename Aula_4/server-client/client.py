import socket



clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "127.0.0.1"
port = 12340

clientSocket.connect((host, port))
print("Ligado ao servidor com sucesso!")

def cliente():
    while True:
        mensagem = input("Introduza a sua mensagem para enviar ao servidor (escreva sair para fechar): ")
        if mensagem == "sair":
            clientSocket.send(mensagem.encode())
            resposta = clientSocket.recv(1024).decode()
            print("resposta do servidor: ", resposta)

            clientSocket.close()
            break
        else:
            clientSocket.send(mensagem.encode())
            print(f"a enviar para o servidor a mensagem: {mensagem}")
            resposta2 = clientSocket.recv(1024).decode()
            print("resposta do servidor: ", resposta2)
            continue

cliente()