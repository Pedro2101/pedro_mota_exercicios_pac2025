# exercicio 1

numero=30
def algoritmo(numero):
    #impares
    for i in range(1, numero+1, 2):
        print("Números ímpares:", i)
    #pares
    for i in range(0, numero+1, 2):
        print("Números pares:", i)

algoritmo(numero)

# exercicio 2

def check_nums():
    numeros = []

    for i in range(10):
        numero = int(input(f"Introduza o {i+1}º número: "))
        numeros.append(numero)

        if numero % 2 == 0:
            print(f"{numero} é par.")
        else:
            print(f"{numero} é ímpar.")

check_nums()

# exercicio 3

def media_alunos():
    soma = 0

    for i in range(10):
        nota = float(input(f"Introduza a nota do {i+1}º aluno: "))
        soma += nota

    media = soma / 10
    print(f"A média das notas é: {media}")

media_alunos()

# exercicio 4

def numero_primo():
    numero = int(input("Introduza um número inteiro: "))

    if numero <= 1:
        print("Não é um número primo.")
        return

    primo = True

    for i in range(2, numero):
        if numero % i == 0:
            primo = False
            break

    if primo:
        print(f"{numero} é um número primo.")
    else:
        print(f"{numero} não é um número primo.")

numero_primo()

# exercicio 5

def dez_mil():
    for i in range(1, 10001):
        print(i)

dez_mil()

# exercicio 6

def dez_primos():
    contador = 0
    numero = 2

    while contador < 10:
        primo = True

        for i in range(2, numero):
            if numero % i == 0:
                primo = False
                break

        if primo:
            print(numero)
            contador += 1

        numero += 1

dez_primos()

# exercicio 7

def serie_dez():
    for i in range(10, 1001, 10):
        print(i)

serie_dez()

# exercicio 8

def duas_series():
    # série 1: 10, 20, 30 ... 1000
    for i in range(10, 1001, 10):
        print(i)

    print("--- SEGUNDA SÉRIE ---")

    # série 2: 15, 25, 35 ... 995
    for i in range(15, 1000, 10):
        print(i)

duas_series()

# exercicio 9

def numero_entre_1_e_100():
    while True:
        numero = int(input("Introduza um número entre 1 e 100: "))

        if 1 <= numero <= 100:
            print("Número válido.")
            break
        else:
            print("Número inválido. Tente novamente.")

numero_entre_1_e_100()

# exercicio 10

def contar_divisores():
    numero = int(input("Introduza um número inteiro: "))
    divisores = 0

    for i in range(1, numero + 1):
        if numero % i == 0:
            divisores += 1

    print(f"O número {numero} possui {divisores} divisores.")

contar_divisores()

# exercicio 11

def padrao_numeros():
    for i in range(1, 6):
        print(str(i) * i)

padrao_numeros()

# exercicio 12

def operacoes_acumulador():
    numero = int(input("Introduza um número: "))
    contador = 0

    for i in range(1, numero):
        print(f"{numero} + {i} = {numero + i}")
        contador += 1

        print(f"{numero} - {i} = {numero - i}")
        contador += 1

        print(f"{numero} * {i} = {numero * i}")
        contador += 1

        print(f"{numero} / {i} = {numero / i}")
        contador += 1

    print(f"Total de operações efetuadas: {contador}")

operacoes_acumulador()

# exercicio 13

def tabuada():
    numero = int(input("Introduza um número para ver a tabuada: "))

    for i in range(1, 11):
        print(f"{numero} x {i} = {numero * i}")

tabuada()

# exercicio 14

def tabuadas():
    for numero in range(1, 101):
        print(f"\nTabuada do {numero}")
        for i in range(1, 11):
            print(f"{numero} x {i} = {numero * i}")

tabuadas()

# exercicio 15

def tabela_ascii():
    contador = 0

    for i in range(256):
        print(f"Código: {i}  Caractere: {chr(i)}")
        contador += 1

        if contador == 20:
            resposta = input("Mostrar mais 20? (s para continuar, qualquer tecla para sair): ")
            if resposta.lower() != "s":
                break
            contador = 0

tabela_ascii()

# exercicio 16

def media_30_pares():
    soma = 0
    contador = 0

    while contador < 30:
        numero = int(input("Introduza um número par entre 1 e 50: "))

        if 1 <= numero <= 50 and numero % 2 == 0:
            soma += numero
            contador += 1
        else:
            print("Número inválido. Tem de ser PAR e entre 1 e 50.")

    media = soma / 30
    print(f"A média dos 30 números pares é: {media}")

media_30_pares()

# exercicio 17

def multiplos_5_3():
    for i in range(1, 1001):
        if i % 5 == 0 and i % 3 == 0:
            print(i)
    
multiplos_5_3()

# exercicio 18

def numeros_perfeitos():
    limite = int(input("Introduza um número para verificar quantos números perfeitos existem até ele: "))
    contador = 0

    for n in range(1, limite + 1):
        soma_divisores = 0

        for i in range(1, n):
            if n % i == 0:
                soma_divisores += i

        if soma_divisores == n:
            print(f"{n} é um número perfeito")
            contador += 1

    print(f"Existem {contador} números perfeitos entre 1 e {limite}")

numeros_perfeitos()

# exercicio 19

def serie60():
    a = 1
    b = 1

    for i in range(58):
        c = a + b
        print(f"{a}+{b}={c}")
        a = b
        b = c

serie60()



# teste final

def ler_inteiro_validado(mensagem, minimo, maximo):
    while True:
        valor = int(input(mensagem))
        if minimo <= valor <= maximo:
            return valor
        print(f"Valor inválido. Introduza um número entre {minimo} e {maximo}.")


def eh_primo(numero):
    if numero <= 1:
        return False

    for i in range(2, numero):
        if numero % i == 0:
            return False
    return True


def contar_divisores_numero(numero):
    divisores = 0
    for i in range(1, numero + 1):
        if numero % i == 0:
            divisores += 1
    return divisores


def eh_perfeito(numero):
    soma_divisores = 0
    for i in range(1, numero):
        if numero % i == 0:
            soma_divisores += i
    return soma_divisores == numero


def analisar_valores():
    valor = ler_inteiro_validado(
        "Introduza um valor entre 1 e 30000: ", 1, 30000
    )
    contador = 0

    for numero in range(valor, 0, -1):
        primo = "Sim" if eh_primo(numero) else "Não"
        divisores = contar_divisores_numero(numero)
        perfeito = "Sim" if eh_perfeito(numero) else "Não"

        print(
            f"Número: {numero} | Primo: {primo} | Divisores: {divisores} | Perfeito: {perfeito}"
        )

        contador += 1
        if contador == 10 and numero > 1:
            resposta = input("Continuar mais 10 valores? (s/n): ")
            if resposta.lower() != "s":
                break
            contador = 0


def calculadora_simples():
    while True:
        print("\n--- CALCULADORA ---")
        print("1 - Soma")
        print("2 - Subtração")
        print("3 - Multiplicação")
        print("4 - Divisão")
        print("5 - Tabuada")
        print("0 - Voltar ao menu principal")

        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            break

        if opcao in ["1", "2", "3", "4"]:
            numero1 = ler_inteiro_validado("Introduza o primeiro número (1 a 1000): ", 1, 1000)
            numero2 = ler_inteiro_validado("Introduza o segundo número (1 a 1000): ", 1, 1000)

            if opcao == "1":
                print(f"Resultado: {numero1} + {numero2} = {numero1 + numero2}")
            elif opcao == "2":
                print(f"Resultado: {numero1} - {numero2} = {numero1 - numero2}")
            elif opcao == "3":
                print(f"Resultado: {numero1} * {numero2} = {numero1 * numero2}")
            elif opcao == "4":
                print(f"Resultado: {numero1} / {numero2} = {numero1 / numero2}")

        elif opcao == "5":
            numero = ler_inteiro_validado("Introduza o número da tabuada (1 a 1000): ", 1, 1000)
            maximo = ler_inteiro_validado(
                "Introduza até que multiplicador quer ver (1 a 1000): ", 1, 1000
            )

            contador = 0
            for i in range(1, maximo + 1):
                print(f"{numero} x {i} = {numero * i}")
                contador += 1

                if contador == 20 and i < maximo:
                    resposta = input("Continuar mais 20 valores? (s/n): ")
                    if resposta.lower() != "s":
                        break
                    contador = 0
        else:
            print("Opção inválida.")


def menu_principal():
    while True:
        print("\n===== MENU PRINCIPAL =====")
        print("1 - Analisar valores até 1")
        print("2 - Calculadora simples")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            analisar_valores()
        elif opcao == "2":
            calculadora_simples()
        elif opcao == "0":
            print("Programa terminado.")
            break
        else:
            print("Opção inválida.")


menu_principal()

# teste final 2

def ler_texto_nao_vazio(mensagem):
    while True:
        texto = input(mensagem).strip()
        if texto != "":
            return texto
        print("Entrada inválida. Não pode ficar vazia.")


def ler_numero_positivo(mensagem):
    while True:
        texto = input(mensagem).strip().replace(",", ".")
        try:
            valor = float(texto)
            if valor >= 0:
                return valor
            print("Introduza um valor igual ou superior a 0.")
        except ValueError:
            print("Entrada inválida. Introduza um número válido.")


def ler_telefone(mensagem):
    while True:
        telefone = input(mensagem).strip().replace(" ", "")
        if telefone.isdigit() and 9 <= len(telefone) <= 15:
            return telefone
        print("Telefone inválido. Introduza apenas dígitos (9 a 15).")


def ler_nif(mensagem):
    while True:
        nif = input(mensagem).strip().replace(" ", "")
        if nif.isdigit() and len(nif) == 9:
            return nif
        print("NIF inválido. Tem de ter exatamente 9 dígitos.")


def calcular_desconto(compra):
    if 100 <= compra <= 200:
        return compra * 0.05
    elif 200 < compra < 500:
        return compra * 0.10
    elif compra > 500:
        return compra * 0.15
    return 0


def inserir_cliente(clientes, proximo_numero):
    print("\n--- INSERIR CLIENTE ---")
    nome = ler_texto_nao_vazio("Nome do cliente: ")
    morada = ler_texto_nao_vazio("Morada: ")
    telefone = ler_telefone("Telefone: ")
    nif = ler_nif("NIF: ")
    compra = ler_numero_positivo("Valor da compra: ")

    desconto = calcular_desconto(compra)
    divfin = compra - desconto

    cliente = {
        "numcli": proximo_numero,
        "nome": nome,
        "morada": morada,
        "telefone": telefone,
        "nif": nif,
        "compra": compra,
        "desconto": desconto,
        "divfin": divfin,
    }

    clientes.append(cliente)
    print(f"Cliente inserido com sucesso. Número do cliente: {proximo_numero}")
    return proximo_numero + 1


def mostrar_cliente(cliente):
    print("\n------------------------------")
    print(f"NúmCli : {cliente['numcli']}")
    print(f"NomCli : {cliente['nome']}")
    print(f"Morada : {cliente['morada']}")
    print(f"Tel    : {cliente['telefone']}")
    print(f"NIF    : {cliente['nif']}")
    print(f"Compra : {cliente['compra']:.2f} €")
    print(f"Desc.  : {cliente['desconto']:.2f} €")
    print(f"DivFin : {cliente['divfin']:.2f} €")
    print("------------------------------")


def listar_clientes(clientes):
    if len(clientes) == 0:
        print("\nAinda não existem clientes registados.")
        return

    print("\n--- LISTAGEM DE CLIENTES ---")
    for indice, cliente in enumerate(clientes):
        mostrar_cliente(cliente)
        if indice < len(clientes) - 1:
            resposta = input("Prima ENTER para ver o próximo cliente ou escreva s para sair: ")
            if resposta.lower() == "s":
                break


def procurar_cliente_por_numero(clientes):
    if len(clientes) == 0:
        print("\nAinda não existem clientes registados.")
        return

    while True:
        texto = input("Introduza o número do cliente que pretende procurar: ").strip()
        if texto.isdigit():
            numero = int(texto)
            break
        print("Número de cliente inválido.")

    for cliente in clientes:
        if cliente["numcli"] == numero:
            print("\nCliente encontrado:")
            mostrar_cliente(cliente)
            return

    print("\nNão foi encontrado nenhum cliente com esse número.")


def menu_base_dados_clientes():
    clientes = []
    proximo_numero = 1

    while True:
        print("\n===== BASE DE DADOS DE CLIENTES =====")
        print("1 - Inserir cliente")
        print("2 - Listar clientes")
        print("3 - Procurar cliente por número")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            proximo_numero = inserir_cliente(clientes, proximo_numero)
        elif opcao == "2":
            listar_clientes(clientes)
        elif opcao == "3":
            procurar_cliente_por_numero(clientes)
        elif opcao == "0":
            print("Programa terminado.")
            break
        else:
            print("Opção inválida. Tente novamente.")


menu_base_dados_clientes()