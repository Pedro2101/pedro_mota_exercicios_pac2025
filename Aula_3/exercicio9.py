notas = {
    'João': [7, 8, 9],
    'Maria': [10, 9, 8],
    'Ana': [6, 7, 8]
}

media_joao = sum(notas['João']) / len(notas['João'])
media_maria = sum(notas['Maria']) / len(notas['Maria'])
media_ana = sum(notas['Ana']) / len(notas['Ana'])

print(f"João: {media_joao}\nMaria: {media_maria}\nAna: {media_ana}")