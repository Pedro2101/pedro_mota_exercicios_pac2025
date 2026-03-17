# exercicio 1

alunos = {}

while True:
    input_nome = input("Introduza o nome do aluno: ")
    input_idade = int(input("Introduza a idade do aluno: "))
    input_curso = input("Introduza o curso do aluno: ")
    

    alunos = {"nome": input_nome, "idade": input_idade, "curso": input_curso}

    print(f"nome: {alunos['nome']} \nidade: {alunos['idade']} \ncurso: {alunos['curso']}")

