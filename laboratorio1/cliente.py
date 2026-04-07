"""
LAB 1 - Sistema de Chat com Deteção de Dados Pessoais (GDPR)
Cliente CLI
Instituto Politécnico de Setúbal
"""

import socket
import threading

ENCODING    = "utf-8"
BUFFER_SIZE = 4096
HOST        = "127.0.0.1"
PORT        = 5555


def loop_receção(sock: socket.socket, evento_stop: threading.Event) -> None:
    """
    Thread dedicada a receber mensagens do servidor.
    Termina quando a ligação fechar ou o evento de stop for ativado.
    """
    while not evento_stop.is_set():
        try:
            dados = sock.recv(BUFFER_SIZE)
        except OSError:
            break

        if not dados:
            print("\n[SISTEMA] Ligação terminada pelo servidor.")
            break

        mensagem = dados.decode(ENCODING, errors="replace")
        print(mensagem, end="" if mensagem.endswith("\n") else "\n")

    evento_stop.set()


def main() -> None:
    evento_stop = threading.Event()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((HOST, PORT))
    except OSError as e:
        print(f"[ERRO] Não foi possível ligar ao servidor ({HOST}:{PORT}): {e}")
        return

    print(f"[SISTEMA] Ligado ao servidor {HOST}:{PORT}")
    print("[SISTEMA] Escrever 'exit' para sair | '/help' para ver comandos\n")

    recetor = threading.Thread(
        target=loop_receção,
        args=(sock, evento_stop),
        daemon=True,
    )
    recetor.start()

    try:
        while not evento_stop.is_set():
            try:
                mensagem = input()
            except EOFError:
                mensagem = "exit"

            if not mensagem.strip():
                continue

            try:
                sock.sendall(mensagem.encode(ENCODING))
            except OSError:
                print("[ERRO] Falha ao enviar mensagem. Ligação perdida.")
                break

            if mensagem.strip().lower() in {"exit", "/exit"}:
                break
    except KeyboardInterrupt:
        print("\n[SISTEMA] Interrompido pelo utilizador.")
    finally:
        evento_stop.set()
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        sock.close()
        recetor.join(timeout=1.0)
        print("[SISTEMA] Cliente encerrado.")


if __name__ == "__main__":
    main()
