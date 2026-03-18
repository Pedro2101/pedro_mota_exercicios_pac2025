import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "127.0.0.1"
port = 12340

server.bind((host, port))

server.listen(1)

print(f"Ligado. A ouvir em {host}:{port}")
print("A aguardar ligação do cliente")


is_on = True

while is_on:
    clientSocket, addressSocket = server.accept()
    print(f"Ligação establecida com {addressSocket}.")
    while True:
        mensagem_cliente = clientSocket.recv(1024).decode()
        if mensagem_cliente == "sair":
            clientSocket.send("A encerrar o servidor. Adeus!".encode())
            clientSocket.close()
            server.close()

            print("Server a fechar.")
            is_on = False
            break
        else:
            print(f"Mensagem recebida do cliente: {mensagem_cliente}")
            clientSocket.send("o servidor recebeu a mensagem".encode())

