# exercicio 1

fruta=["banana", "uva", "abacaxi", "laranja"]

ordenado = True

while ordenado:
    ordenado = False
    for i in range(len(fruta)-1):
        if fruta[i] > fruta[i+1]:
            fruta[i],fruta[i+1] = fruta[i+1],fruta[i]
            ordenado = True

print(fruta)

# exercicio 2

