# exercicio 1

alunos = [{}]

while True:
    input_nome = input("Introduza o nome do aluno (s para sair): ")
    input_idade = int(input("Introduza a idade do aluno (s para sair): "))
    input_curso = input("Introduza o curso do aluno (s para sair): ")
    
    
    alunos.append({"nome": input_nome, "idade": input_idade, "curso": input_curso})


    print(alunos[1])