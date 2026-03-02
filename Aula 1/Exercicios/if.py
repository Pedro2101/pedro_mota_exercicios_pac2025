# exercicio 1

segundos = int(input("Introduza o total de segundos: "))

horas = segundos // 3600
resto = segundos % 3600
minutos = resto // 60
segundos_finais = resto % 60

print(horas, "hora(s),", minutos, "minuto(s) e", segundos_finais, "segundo(s).")

# exercicio 2

num1 = int(input("Introduza o primeiro número: "))
num2 = int(input("Introduza o segundo número: "))
num3 = int(input("Introduza o terceiro número: "))

maior = num1
menor = num1

if num2 > maior:
    maior = num2
if num3 > maior:
    maior = num3

if num2 < menor:
    menor = num2
if num3 < menor:
    menor = num3

print("Maior:", maior)
print("Menor:", menor)


# exercicio 3

num1 = int(input("Introduza o primeiro número: "))
num2 = int(input("Introduza o segundo número: "))

if num1 < num2:
    print("Crescente:", num1, ",", num2)
    print("Decrescente:", num2, ",", num1)
elif num2 < num1:
    print("Crescente:", num2, ",", num1)
    print("Decrescente:", num1, ",", num2)
else:
    print("Os números são iguais:", num1, "e", num2)

# exercicio 4

saldo_cliente = float(input("Introduza o saldo do cliente: "))
cheque = float(input("Introduza o valor do cheque a descontar: "))

if saldo_cliente >= cheque:
    novo_saldo = saldo_cliente - cheque
    print("Cheque descontado, saldo:", novo_saldo)
else:
    print("Saldo insuficiente para descontar o cheque.")

# exercicio 5

num1 = int(input("Introduza o primeiro número: "))
num2 = int(input("Introduza o segundo número: "))
num3 = int(input("Introduza o terceiro número: "))

# ordem crescente
if num1 <= num2 <= num3:
    a, b, c = num1, num2, num3
elif num1 <= num3 <= num2:
    a, b, c = num1, num3, num2
elif num2 <= num1 <= num3:
    a, b, c = num2, num1, num3
elif num2 <= num3 <= num1:
    a, b, c = num2, num3, num1
elif num3 <= num1 <= num2:
    a, b, c = num3, num1, num2
else:
    a, b, c = num3, num2, num1

print("Crescente:", a, ",", b, ",", c)
print("Decrescente:", c, ",", b, ",", a)

# exercicio 6

nome = input("Introduza o nome do cliente: ")
compra = float(input("Introduza o valor da compra: "))

if compra <= 200:
    percentual = 0.10
elif compra <= 500:
    percentual = 0.15
else:
    percentual = 0.20

desconto = compra * percentual
total = compra - desconto

print("Nome:", nome)
print(f"Compra: {compra}€")
print(f"Desconto: {desconto}€")
print(f"Total a pagar: {total}€")



# exercicio 7

nota1 = float(input("Introduza a Nota 1: "))
nota2 = float(input("Introduza a Nota 2: "))
nota3 = float(input("Introduza a Nota 3: "))

media = (nota1 * 2 + nota2 * 3 + nota3 * 5) / 10

print(f"Média: {media:.1f}")

if media >= 6:
    print("Aprovado")
else:
    print("Reprovado")




# exercicio 8

notas = []
soma = 0

for i in range(1, 11):
    nota = float(input(f"Introduza a nota do aluno {i} (0 a 20): "))
    notas.append(nota)
    soma += nota

media = soma / 10

acima_ou_igual = 0
for nota in notas:
    if nota >= media:
        acima_ou_igual += 1

print(f"Média da turma: {media}")
print("Alunos com nota igual ou acima da média:", acima_ou_igual)


# exercicio 9
numero = int(input("Introduza o mês pretendente de 1 a 12: "))

if numero == 1:
    print("Janeiro")
elif numero == 2:
    print("Fevereiro")
elif numero == 3:
    print("Março")
elif numero == 4:
    print("Abril")
elif numero == 5:
    print("Maio")
elif numero == 6:
    print("Junho")
elif numero == 7:
    print("Julho")
elif numero == 8:
    print("Agosto")
elif numero == 9:
    print("Setembro")
elif numero == 10:
    print("Outubro")
elif numero == 11:
    print("Novembro")
elif numero == 12:
    print("Dezembro")
else:
    print("Erro: número inválido.")



# exercicio 10 
pares = 0
impares = 0

for i in range(1, 11):
    numero = int(input(f"Introduza o número {i}: "))

    if numero % 2 == 0:
        pares += 1
    else:
        impares += 1

print("Pares:", pares)
print("Ímpares:", impares)
