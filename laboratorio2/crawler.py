"""
LAB 2 - Web Crawler Ético
"""

import requests
from bs4 import BeautifulSoup
import time
import json
import urllib.robotparser
from urllib.parse import urljoin, urlparse


# Configs importantes

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
DELAY = 5000             # 5000ms = 5 segundos
TIMEOUT = 15             # timeout por pedido (segundos)


# Funções auxiliares


def obter_robots(url_base):
    # tenta ler robots.txt
    rp = urllib.robotparser.RobotFileParser()
    robots_url = urljoin(url_base, "/robots.txt")
    try:
        resposta = requests.get(robots_url, timeout=TIMEOUT)
        if resposta.status_code != 200:
            print(f"[robots.txt] {robots_url} -> HTTP {resposta.status_code} (sem restricoes)")
            return rp, False

        rp.parse(resposta.text.splitlines())
        print(f"[robots.txt] Lido em {robots_url}")
        return rp, True
    except Exception:
        print(f"[robots.txt] Nao foi possivel ler {robots_url} (sem restricoes)")
        return rp, False


def dominio_base(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def normalizar_url(url):
    parsed = urlparse(url)
    limpa = parsed._replace(fragment="")
    return limpa.geturl().rstrip("/")


def obter_pagina(url, sessao):
    try:
        resposta = sessao.get(url, timeout=TIMEOUT)
        resposta.raise_for_status()
        return resposta
    except requests.RequestException as e:
        print(f"[ERRO] {url} -> {e}")
        return None


def extrair_dados(url, html, url_base):
    soup = BeautifulSoup(html, "html.parser")

    # Título
    titulo_tag = soup.find("title")
    titulo = titulo_tag.get_text(strip=True) if titulo_tag else "(sem título)"

    # links absolutos
    links = []
    for a in soup.find_all("a", href=True):
        href = urljoin(url, a["href"])
        href = normalizar_url(href)
        parsed = urlparse(href)
        if parsed.scheme in ("http", "https"):
            links.append(href)
    links = sorted(set(links))

    return {
        "url": url,
        "titulo": titulo,
        "links": links,
    }


# Função principal do crawler

def crawler(url_inicial, max_paginas):
    url_base = dominio_base(url_inicial)

    # Configurar a sessão HTTP com User-Agent
    sessao = requests.Session()
    sessao.headers.update({"User-Agent": USER_AGENT})

    # Ler o robots.txt
    robots, usar_robots = obter_robots(url_base)

    fila = [normalizar_url(url_inicial)]
    visitadas = set()
    resultados = []

    print("\n--- Crawler iniciado ---")
    print("URL inicial:", url_inicial)
    print("Max paginas:", max_paginas)
    print("------------------------\n")

    while fila and len(visitadas) < max_paginas:
        url_atual = fila.pop(0)

        # Evita revisitar
        if url_atual in visitadas:
            continue

        if usar_robots and not robots.can_fetch(USER_AGENT, url_atual):
            print(f"[BLOQUEADO robots.txt] {url_atual}")
            visitadas.add(url_atual)
            continue

        print(f"[{len(visitadas)+1}/{max_paginas}] A visitar: {url_atual}")

        # Pedido HTTP
        resposta = obter_pagina(url_atual, sessao)
        visitadas.add(url_atual)

        if resposta is None:
            continue

        # Verifica se é HTML
        content_type = resposta.headers.get("Content-Type", "")
        if "text/html" not in content_type:
            print(f"[IGNORADO] Content-Type: {content_type}")
            continue

        # Extrai dados
        dados = extrair_dados(url_atual, resposta.text, url_base)
        resultados.append(dados)

        print(f"Titulo: {dados['titulo']}")
        print(f"Links encontrados: {len(dados['links'])}")

        # Adiciona novos links à fila
        for link in dados["links"]:
            if link not in visitadas and link not in fila:
                fila.append(link)

        # Delay
        if fila and len(visitadas) < max_paginas:
            print(f"Pausa: {DELAY}ms")
            time.sleep(DELAY / 1000)

    print("\n--- Crawl concluido ---")
    print("Paginas com dados:", len(resultados))
    print("-----------------------\n")

    # Guarda resultados em JSON
    with open("resultados.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    print("Dados guardados em resultados.json")

    return resultados

# Ponto de entrada

if __name__ == "__main__":
    # Exemplo de uso - site de treino para scraping/crawling
    URL_INICIAL = "https://books.toscrape.com/"
    MAX_PAGINAS = 5

    dados = crawler(URL_INICIAL, MAX_PAGINAS)

    # Mostra um resumo no terminal
    print("\n── Resumo ──────────────────────────────────────────")
    for entrada in dados:
        print(f"\n  URL    : {entrada['url']}")
        print(f"  Título : {entrada['titulo']}")
        print(f"  Links  : {len(entrada['links'])}")
