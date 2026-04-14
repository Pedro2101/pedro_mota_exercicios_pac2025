# controlo de fluxos
#Exemplo
#i=1
#while (i<255):
#    print(i,"   ",chr(i))
#    i+=1
#print ( ord("o"))
#i=0
#numLista=[3,2,7,9,1,4,6]
# ordenar [2,3,7,9,1,4,6]

#print(numLista)
#numLista.insert(i,numLista[i+1])
#print(numLista)
#numLista.pop(i+2)
#print(numLista)

flagtroca=True
numLista=[3,2,7,9,4,6,1]
#index    0 1 2 3 4 5 6
print("tamanho lista" ,len(numLista) )
while flagtroca:
    flagtroca=False
    for i in range(len(numLista)-1):
        if numLista[i] > numLista[i+1]:
            numLista[i],numLista[i+1] = numLista[i+1],numLista[i]
            flagtroca=True

print (numLista)


# Exemplo 2
#nomelista=["joana quental", "joao quental" , "pedro lameiro"]

#nomelista[0][6] comparar nomelista[1][6]

#nomelista[0]=nomelista[1]