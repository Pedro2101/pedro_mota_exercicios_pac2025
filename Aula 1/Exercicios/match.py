# exercicio 1

dias = input("Introuza o dia de semana: (segunda, terca, quarta, quinta, sexta, sabado ou domingo): ")

match dias :
    case "segunda":
        print("dia útil")
    case "terca":
        print("dia útil")
    case "quarta":
        print("dia útil")
    case "quinta":
        print("dia útil")
    case "sexta":
        print("dia útil")
    case "sabado":
        print("fim de semana")
    case "domingo":
        print("fim de semana")

# exercicio 2

classific = int(input("Introduza uma classifação de 0 a 100: "))

match classific :
    case classific if classific >= 90 and classific <= 100:
        print("Excelente")
    case classific if classific >= 70 and classific <= 89:
        print("Bom")
    case classific if classific >=50 and classific <= 69:
        print("Suficiente")
    case classific if classific >= 0 and classific <= 49:
        print("Insuficiente")
    case _:
        print("Classificação inválida. Experimente com valores compreendidos entre 0 e 100.")

# exercicio 3

pedido = {"tipo": "venda", "valor": 100}
match pedido :
    case {"tipo": "venda"}:
        print("venda no valor de", pedido["valor"])
    case {"tipo": "compra"}:
        print("compra no valor de", pedido["valor"])
    case _:
        print("tipo de pedido desconhecido")


#exercicio 4

dado = "Pedro Mota"
match dado:
    case int():
        print("é um número inteiro.")
    case str():
        if dado.isnumeric():
            print("é uma string numérica.")
        else:
            print("é uma string textual.")
    case list():
        print("é uma lista.")
    case _:
        print("tipo de dado desconhecido.")

# exercicio 5

mensagem = input("Introduza uma mensagem: ")
match mensagem:
    case mensagem if mensagem == "olá" or mensagem == "bom dia":
        print("saudação")
    case mensagem if mensagem.endswith("?"):
        print("pergunta")
    case mensagem if mensagem == "tchau" or mensagem == "adeus":
        print("despedida")
    case _:
        print("mensagem desconhecida")

# exercicio 6

servidor = {"status": "erro", "tempo_resposta": 100}

match servidor:
    case {"status": "ok", "tempo_resposta": tempo} if tempo > 200:
        print("Servidor lento")
    case {"status": "ok"}:
        print("Servidor ativo")
    case {"status": "erro"}:
        print("Servidor indisponível")
    case _:
        print("Estado desconhecido")

# exercicio 7

categoria = input("Introduza a categoria do produto (eletrônico, alimento, outros: ")
valor = int(input("Introduza o valor do produto: "))

classificacao = {"categoria": categoria, "valor": valor}

match classificacao:
    case {"categoria": "eletrônico", "valor": valor} if valor > 1000:
        print("Produto de luxo")
    case {"categoria": "eletrônico", "valor": valor} if valor <= 1000:
        print("Produto comum")
    case {"categoria": "alimento"}:
        print("Produto alimentar")
    case _:
        print("categoria desconhecida")

# exercicio 8

calculo = input("escolha um cálculo (soma, subtrai, multiplica, divide): ")
num1 = float(input("Introduza o primeiro número: "))
num2 = float(input("Introduza o segundo número: "))

match calculo:
    case "soma":
        resultado = num1 + num2
        print("O resultado da soma é:", resultado)
    case "subtrai":
        resultado = num1 - num2
        print("O resultado da subtração é:", resultado)
    case "multiplica":
        resultado = num1 * num2
        print("O resultado da multiplicação é:", resultado)
    case "divide":
        if num2 != 0:
            resultado = num1 / num2
            print("O resultado da divisão é:", resultado)
        else:
            print("Erro: divisão por zero é impossível .")
    case _:
        print("Cálculo desconhecido. Escolha entre soma, subtrai, multiplica ou divide.")

# exercicio 9

requesicao = {"metodo": "GET", "conteudo": ""}

match requesicao:
    case {"metodo": "GET"}:
        print("Requisição GET recebida")
    case {"metodo": "POST"}:
        print("Requisição POST com dados validos")
    case {"metodo": "POST", "conteudo": ""}:
        print("Requisição POST sem dados")
    case _:
        print("Método não suportado")

# exercicio 10

jogador1 = input("Jogador 1 (pedra, papel ou tesoura): ")
jogador2 = input("Jogador 2 (pedra, papel ou tesoura): ")

match (jogador1, jogador2):
    case (j1, j2) if j1 == j2:
        print("Empate")
    case ("pedra", "tesoura") | ("tesoura", "papel") | ("papel", "pedra"):
        print("Jogador 1 venceu")
    case ("tesoura", "pedra") | ("papel", "tesoura") | ("pedra", "papel"):
        print("Jogador 2 venceu")
    case _:
        print("Jogada inválida. Use pedra, papel ou tesoura.")
