"""
LAB 1 - Sistema de Chat com Deteção de Dados Pessoais (GDPR)
"""

import json
import logging
import re
import socket
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------

ENCODING    = "utf-8"
BUFFER_SIZE = 4096
HOST        = "0.0.0.0"
PORT        = 5555

BASE_DIR    = Path(__file__).resolve().parent
CAPTURAS_LOG = BASE_DIR / "capturas.json"

# ---------------------------------------------------------------------------
# Padrões GDPR (expressões regulares)
# ---------------------------------------------------------------------------

EMAIL_RE     = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b")
PHONE_RE     = re.compile(r"(?<!\d)(?:\+351[\s-]?)?(?:9[1236]\d[\s-]?\d{3}[\s-]?\d{3}|2\d{2}[\s-]?\d{3}[\s-]?\d{3})(?!\d)")
IP_RE        = re.compile(
    r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"
)
FULL_NAME_RE = re.compile(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3}\b")
DOB_RE       = re.compile(
    r"\b(?:0[1-9]|[12]\d|3[01])[/-](?:0[1-9]|1[0-2])[/-](?:19|20)\d{2}\b"
)
CC_RE        = re.compile(r"\b(?:\d[ -]?){13,19}\b")

# Deteção de divulgação de credenciais: "password é X", "iban: X", "pin=X", etc.
# Conector aceita: é/e/eh (com ou sem acento), : = -> sera/será/is/foi
DISCLOSURE_RE = re.compile(
    r"\b(?:password|palavra-passe|iban|pin|otp|token|codigo|cvv|nib)\b"
    r"\s*(?:é|e|eh|:|=|->|sera|será|is|foi)\s*\S+",
    re.IGNORECASE,
)

# Palavras-chave associadas a tentativas de engenharia social
SE_KEYWORDS = {
    "urgente", "password", "palavra-passe", "codigo", "otp",
    "token", "iban", "cartao", "pin", "confirma", "verifica",
}

# ---------------------------------------------------------------------------
# Estado global do servidor
# ---------------------------------------------------------------------------

# clients: socket -> {"username": str, "addr": tuple, "consent": bool}
clients: Dict[socket.socket, dict] = {}
clients_lock  = threading.Lock()
storage_lock  = threading.Lock()

# ---------------------------------------------------------------------------
# Utilitários de persistência
# ---------------------------------------------------------------------------

def gravar_registo(caminho: Path, registo: dict) -> None:
    """Acrescenta um registo a um ficheiro JSON (lista de registos)."""
    with storage_lock:
        lista: list = []
        if caminho.exists():
            try:
                conteudo = json.loads(caminho.read_text(encoding=ENCODING))
                if isinstance(conteudo, list):
                    lista = conteudo
            except (OSError, json.JSONDecodeError):
                lista = []
        lista.append(registo)
        caminho.write_text(
            json.dumps(lista, indent=2, ensure_ascii=False),
            encoding=ENCODING,
        )

# ---------------------------------------------------------------------------
# Deteção GDPR
# ---------------------------------------------------------------------------

def algoritmo_luhn(numero: str) -> bool:
    """Valida um possível número de cartão de crédito/débito pelo algoritmo de Luhn."""
    digitos = [int(c) for c in numero if c.isdigit()]
    if not (13 <= len(digitos) <= 19):
        return False
    checksum = 0
    paridade = len(digitos) % 2
    for i, d in enumerate(digitos):
        if i % 2 == paridade:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
    return checksum % 10 == 0

def detetar_dados_pessoais(texto: str) -> Dict[str, List[str]]:
    """
    Procura dados pessoais no texto com expressões regulares.
    Devolve um dicionário {categoria: [valores encontrados]}.
    """
    resultado: Dict[str, List[str]] = {}

    def unicos(padrao: re.Pattern) -> List[str]:
        return sorted({m.group(0).strip() for m in padrao.finditer(texto)})

    emails = unicos(EMAIL_RE)
    if emails:
        resultado["emails"] = emails

    telefones = unicos(PHONE_RE)
    if telefones:
        resultado["telefones"] = telefones

    ips = unicos(IP_RE)
    if ips:
        resultado["ips"] = ips

    nomes = unicos(FULL_NAME_RE)
    if nomes:
        resultado["nomes_completos"] = nomes

    datas = unicos(DOB_RE)
    if datas:
        resultado["datas_nascimento"] = datas

    cartoes: set = set()
    for candidato in unicos(CC_RE):
        if algoritmo_luhn(candidato):
            cartoes.add(candidato)
    if cartoes:
        resultado["cartoes_credito"] = sorted(cartoes)

    divulgacoes = unicos(DISCLOSURE_RE)
    if divulgacoes:
        resultado["divulgacao_credenciais"] = divulgacoes

    return resultado

def detetar_engenharia_social(texto: str, deteções: Dict[str, List[str]]) -> List[str]:
    """
    Identifica padrões de engenharia social.
    Devolve lista de razões de suspeita (vazia se não houver).
    """
    razoes: List[str] = []
    lower = texto.lower()

    hits = [kw for kw in SE_KEYWORDS if kw in lower]
    if hits:
        razoes.append(f"palavras-chave suspeitas: {', '.join(sorted(hits))}")

    if len(deteções) >= 2:
        razoes.append("mensagem contém vários tipos de dados pessoais em simultâneo")

    if "cartoes_credito" in deteções and any(kw in lower for kw in {"codigo", "pin", "cvv"}):
        razoes.append("pedido de dados de cartão com código/pin")

    return razoes

# ---------------------------------------------------------------------------
# Comunicação com clientes
# ---------------------------------------------------------------------------

def enviar(conn: socket.socket, texto: str) -> bool:
    """Envia uma linha de texto ao cliente. Devolve False se falhar."""
    try:
        payload = texto if texto.endswith("\n") else texto + "\n"
        conn.sendall(payload.encode(ENCODING))
        return True
    except OSError:
        return False

def receber(conn: socket.socket) -> Optional[str]:
    """Recebe uma mensagem do cliente. Devolve None se a ligação fechar."""
    try:
        dados = conn.recv(BUFFER_SIZE)
    except OSError:
        return None
    if not dados:
        return None
    return dados.decode(ENCODING, errors="replace").strip()

def broadcast(mensagem: str, excluir: Optional[socket.socket] = None) -> None:
    """Envia uma mensagem a todos os clientes ligados, exceto ao remetente."""
    with clients_lock:
        alvos = [s for s in clients if s is not excluir]
    for s in alvos:
        enviar(s, mensagem)

def username_em_uso(nome: str) -> bool:
    with clients_lock:
        return any(
            info["username"].casefold() == nome.casefold()
            for info in clients.values()
        )

def obter_sessao_por_username(nome: str) -> Optional[Tuple[socket.socket, dict]]:
    with clients_lock:
        for s, info in clients.items():
            if info["username"].casefold() == nome.casefold():
                return s, info
    return None

# ---------------------------------------------------------------------------
# Lógica de mensagens (GDPR + broadcast/DM)
# ---------------------------------------------------------------------------

def resumo_deteções(deteções: Dict[str, List[str]]) -> str:
    partes = []
    for chave, valores in deteções.items():
        partes.append(f"{chave}: {', '.join(valores[:3])}")
    return " | ".join(partes)

def processar_mensagem(
    conn: socket.socket,
    info: dict,
    mensagem: str,
    canal: str,
    alvo: Optional[str] = None,
) -> None:
    """
    Verifica dados pessoais, bloqueia se necessário e distribui a mensagem.
    A deteção de engenharia social corre em todas as mensagens,
    independentemente de conterem dados pessoais GDPR ou não.
    """
    deteções = detetar_dados_pessoais(mensagem)

    # --- Verificação GDPR ---
    if deteções:
        resumo = resumo_deteções(deteções)
        enviar(conn, f"[ALERTA GDPR] Mensagem BLOQUEADA. Dados pessoais detetados -> {resumo}")

        if info["consent"]:
            enviar(conn, "[ALERTA GDPR] Deteção registada com o teu consentimento.")
            registo = {
                "tipo":      "gdpr",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "username":  info["username"],
                "addr":      f"{info['addr'][0]}:{info['addr'][1]}",
                "canal":     canal,
                "alvo":      alvo,
                "mensagem":  mensagem,
                "deteções":  deteções,
            }
            gravar_registo(CAPTURAS_LOG, registo)
        else:
            enviar(conn, "[ALERTA GDPR] Deteção NÃO guardada (sem consentimento).")

    # --- Verificação de Engenharia Social (corre sempre, independente do GDPR) ---
    razoes = detetar_engenharia_social(mensagem, deteções)
    if razoes:
        registo_se = {
            "tipo":            "engenharia_social",
            "timestamp":       datetime.utcnow().isoformat() + "Z",
            "username":        info["username"],
            "addr":            f"{info['addr'][0]}:{info['addr'][1]}",
            "alvo":            alvo,
            "razoes":          razoes,
            "tipos_detetados": sorted(deteções.keys()),
            "mensagem":        mensagem,
        }
        gravar_registo(CAPTURAS_LOG, registo_se)
        logging.warning(
            "Possível engenharia social por %s (%s): %s",
            info["username"], info["addr"], "; ".join(razoes),
        )

    if deteções:
        return  # mensagem bloqueada — não é distribuída

    # Sem dados pessoais → distribui normalmente
    if canal == "direto" and alvo:
        resultado = obter_sessao_por_username(alvo)
        if not resultado:
            enviar(conn, f"[SISTEMA] Utilizador '{alvo}' não encontrado ou desligado.")
            return
        conn_alvo, _ = resultado
        enviar(conn_alvo, f"[DM de {info['username']}] {mensagem}")
        enviar(conn,      f"[DM para {alvo}] {mensagem}")
    else:
        broadcast(f"[{info['username']}] {mensagem}", excluir=conn)

# ---------------------------------------------------------------------------
# Comandos especiais
# ---------------------------------------------------------------------------

def tratar_comando(conn: socket.socket, info: dict, comando: str) -> bool:
    """
    Interpreta comandos que começam com '/'.
    Devolve False quando o cliente deve desligar-se.
    """
    cmd = comando.strip()

    if cmd == "/help":
        enviar(conn,
            "[SISTEMA] Comandos disponíveis:\n"
            "  /users             - lista utilizadores online\n"
            "  /w <user> <msg>    - mensagem privada\n"
            "  /consent on|off    - ativar/desativar consentimento GDPR\n"
            "  /help              - esta ajuda\n"
            "  exit               - desligar"
        )
        return True

    if cmd == "/users":
        with clients_lock:
            nomes = sorted(i["username"] for i in clients.values())
        enviar(conn, "[SISTEMA] Online: " + ", ".join(nomes))
        return True

    if cmd.startswith("/consent "):
        _, valor = cmd.split(" ", 1)
        valor = valor.strip().lower()
        if valor in {"on", "sim", "yes", "1"}:
            info["consent"] = True
            enviar(conn, "[SISTEMA] Consentimento GDPR ativado.")
        elif valor in {"off", "nao", "não", "no", "0"}:
            info["consent"] = False
            enviar(conn, "[SISTEMA] Consentimento GDPR desativado.")
        else:
            enviar(conn, "[SISTEMA] Usa: /consent on|off")
        return True

    if cmd.startswith("/w "):
        partes = cmd.split(" ", 2)
        if len(partes) < 3:
            enviar(conn, "[SISTEMA] Usa: /w <username> <mensagem>")
            return True
        _, alvo, msg_privada = partes
        processar_mensagem(conn, info, msg_privada.strip(), canal="direto", alvo=alvo.strip())
        return True

    if cmd in {"/exit", "exit"}:
        return False

    enviar(conn, "[SISTEMA] Comando inválido. Usa /help para ver os comandos.")
    return True

# ---------------------------------------------------------------------------
# Ciclo de vida de cada cliente (corre numa thread)
# ---------------------------------------------------------------------------

def registar_cliente(conn: socket.socket, addr: Tuple[str, int]) -> Optional[dict]:
    """Pede username e consentimento. Devolve o dict de sessão ou None."""
    if not enviar(conn, "[SISTEMA] Bem-vindo ao Chat GDPR!\nEscolhe um username:"):
        return None

    while True:
        username = receber(conn)
        if username is None:
            return None
        username = username.strip()
        if username.lower() in {"exit", "/exit"}:
            return None
        if len(username) < 3:
            enviar(conn, "[SISTEMA] Username demasiado curto (mínimo 3 caracteres):")
            continue
        if username_em_uso(username):
            enviar(conn, "[SISTEMA] Username já em uso. Escolhe outro:")
            continue
        break

    enviar(conn, "[SISTEMA] Permites que dados pessoais detetados nas tuas mensagens sejam guardados para análise? (sim/nao)")
    resposta = receber(conn)
    consentimento = bool(resposta and resposta.strip().lower() in {"sim", "s", "yes", "y"})

    info = {"username": username, "addr": addr, "consent": consentimento}
    with clients_lock:
        clients[conn] = info

    msg_consent = (
        "[SISTEMA] Consentimento ativo. Deteções serão registadas."
        if consentimento
        else "[SISTEMA] Consentimento inativo. Deteções apenas em memória."
    )
    enviar(conn, msg_consent)
    enviar(conn, "[SISTEMA] Comandos: /users | /w <user> <msg> | /consent on|off | /help | exit")
    return info

def gerir_cliente(conn: socket.socket, addr: Tuple[str, int]) -> None:
    """Thread principal de cada cliente."""
    info = registar_cliente(conn, addr)
    if not info:
        try:
            conn.close()
        except OSError:
            pass
        return

    logging.info("Cliente ligado: %s %s", info["username"], addr)
    broadcast(f"[SISTEMA] {info['username']} entrou no chat.", excluir=conn)
    enviar(conn, "[SISTEMA] Ligação estabelecida. Podes começar a escrever!")

    try:
        while True:
            mensagem = receber(conn)
            if mensagem is None:
                break
            if not mensagem:
                continue

            if mensagem.startswith("/"):
                continuar = tratar_comando(conn, info, mensagem)
                if not continuar:
                    break
            elif mensagem.lower() == "exit":
                break
            else:
                processar_mensagem(conn, info, mensagem, canal="broadcast")
    finally:
        with clients_lock:
            clients.pop(conn, None)
        try:
            conn.close()
        except OSError:
            pass
        logging.info("Cliente desligado: %s %s", info["username"], addr)
        broadcast(f"[SISTEMA] {info['username']} saiu do chat.")

# ---------------------------------------------------------------------------
# Arranque do servidor
# ---------------------------------------------------------------------------

def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORT))
    servidor.listen(20)

    logging.info("Servidor GDPR Chat a correr em %s:%s", HOST, PORT)
    logging.info("Capturas   -> %s", CAPTURAS_LOG)
    logging.info("Aguarda clientes... (Ctrl+C para parar)")

    try:
        while True:
            conn, addr = servidor.accept()
            thread = threading.Thread(target=gerir_cliente, args=(conn, addr), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        logging.info("A encerrar servidor...")
    finally:
        with clients_lock:
            for s in list(clients):
                try:
                    s.close()
                except OSError:
                    pass
            clients.clear()
        servidor.close()


if __name__ == "__main__":
    main()