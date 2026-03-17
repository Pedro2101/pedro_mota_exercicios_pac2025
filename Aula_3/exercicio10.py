frase = input("Introduza uma frase: ")
contador_palavras = {}
for palavra in frase.split():
    contador_palavras[palavra] = contador_palavras.get(palavra, 0) + 1
print(contador_palavras)