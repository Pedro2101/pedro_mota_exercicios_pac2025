#ex 1

palavras = ["banana", "uva", "abacaxi", "laranja"]
troca = True

while troca:
    troca = False
    
    # precorrer as palavras
    for i in range(len(palavras) - 1):
        p1 = palavras[i]
        p2 = palavras[i + 1]
        
        # temos de saber onde parar de comparar para o programa não dar erro se uma palavra for mais curta que a outra
        tamanho_min = min(len(p1), len(p2))
        need_trocar = False
        
        # percorrer cada carácter da palavra
        for j in range(tamanho_min):
            # Compara o código ASCII das letras
            if ord(p1[j]) > ord(p2[j]): 
                need_trocar = True
                break
            elif ord(p1[j]) < ord(p2[j]): 
                break # agora que esta tudo certo vou sair do loop
        else:
            # a palavra mais longa tem de ir para trás
            if len(p1) > len(p2):
                need_trocar = True

        if need_trocar:
            palavras[i], palavras[i + 1] = palavras[i + 1], palavras[i]
            troca = True

print(palavras) # ['abacaxi', 'banana', 'laranja', 'uva']


# ex 2

palavras = ["Python", "inteligência", "Aprender", "dados", "Rede"]
troca = True

while troca:
    troca = False
    
    for i in range(len(palavras) - 1):
        # agora a diferença é trocar as maiúsculas so para comparar
        p1 = palavras[i].lower()
        p2 = palavras[i + 1].lower()
        
        tamanho_min = min(len(p1), len(p2))
        need_trocar = False
        
        for j in range(tamanho_min):
            # como vai ser de Z a A, queremos os maiores códigos ASCII no início.
            if ord(p1[j]) < ord(p2[j]): 
                need_trocar = True
                break
            elif ord(p1[j]) > ord(p2[j]): 
                break 
        else:
            if len(p1) < len(p2):
                need_trocar = True

        if need_trocar:
            palavras[i], palavras[i + 1] = palavras[i + 1], palavras[i]
            troca = True

print(palavras) # ['Rede', 'Python', 'inteligência', 'dados', 'Aprender']



# ex 3

palavra = "algoritmo"

# vamos trocar a string por uma lista
letras = list(palavra)
troca = True

while troca:
    troca = False
    
    for i in range(len(letras) - 1):
        # se o valor da tabella ascii da letra da esquerda for maior que o da direita, então temos de trocar
        if ord(letras[i]) > ord(letras[i + 1]):
            letras[i], letras[i + 1] = letras[i + 1], letras[i]
            troca = True

# juntar as palavras numa string vazia
resultado = "".join(letras)

print(resultado)


# ex 4

# temos uma função para contar o numero de letras minusculas numa palavra
def conta_minusculas(palavra):
    contador = 0
    for letra in palavra:
        # se na tabela ASCII da letra estiver no intervalo das minúsculas, soma 1
        if ord('a') <= ord(letra) <= ord('z'):
            contador += 1
    return contador

palavras = ["PYthon", "banana", "CÓDIGO", "intELIGENTE", "dados"]
troca = True

while troca:
    troca = False
    
    for i in range(len(palavras) - 1):
        # vai buscar o número de minúsculas de cada palavra para comparar
        peso_atual = conta_minusculas(palavras[i])
        peso_seguinte = conta_minusculas(palavras[i + 1])
        
        # se a palavra atual tiver mais minúsculas que a seguinte, vai para o fim da lista
        if peso_atual > peso_seguinte:
            palavras[i], palavras[i + 1] = palavras[i + 1], palavras[i]
            troca = True

print(palavras) # ['CÓDIGO', 'intELIGENTE', 'PYthon', 'dados', 'banana']


# ex 5

# isolamos na logica de sort numa função
def ordena_grupo_a_z(lista):
    troca = True
    while troca:
        troca = False
        for i in range(len(lista) - 1):
            p1 = lista[i]
            p2 = lista[i + 1]
            
            tamanho_min = min(len(p1), len(p2))
            need_trocar = False
            
            for j in range(tamanho_min):
                if ord(p1[j]) > ord(p2[j]): 
                    need_trocar = True
                    break
                elif ord(p1[j]) < ord(p2[j]): 
                    break 
            else:
                if len(p1) > len(p2):
                    need_trocar = True

            if need_trocar:
                lista[i], lista[i + 1] = lista[i + 1], lista[i]
                troca = True
    return lista


# logica de organização das palavras
palavras = ["banana", "bola", "abacaxi", "arroz", "uva", "urso"]
grupos = {}

# agrupar as palavras pela letra inicial
for palavra in palavras:
    letra_inicial = palavra[0] # vamos buscar a primeira letra
    
    # se a letra ainda não existe no dicionário, cria uma lista vazia para ela
    if letra_inicial not in grupos:
        grupos[letra_inicial] = []
        
    # adiciona a palavra à lista da letra correspondente
    grupos[letra_inicial].append(palavra)

for letra in grupos:
    grupos[letra] = ordena_grupo_a_z(grupos[letra])

print(grupos) 
# Resultado: {'b': ['banana', 'bola'], 'a': ['abacaxi', 'arroz'], 'u': ['urso', 'uva']}