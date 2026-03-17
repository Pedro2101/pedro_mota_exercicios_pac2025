
palavra = input("Introduza uma palavra: ")
contador_letras = {}

for letra in palavra:
    if letra in contador_letras:
        contador_letras[letra] += 1
    else:
        contador_letras[letra] = 1

print(contador_letras)