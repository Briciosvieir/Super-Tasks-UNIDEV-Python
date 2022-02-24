
arquivo_json = [
    {
        "Escola":"Rotary",
        "Diretor":"Paulo",
        "Professor":"Alex",
        "Aluno":"Fabricio"
    },
    {
        "Segunda":"Português",
        "Terca":"Matematica",
        "Quarta":"Ciencias",
    },
    {
        "Data do primeiro dia": 15,
        "Data do segundo dia": 22,
        "Data do terceiro dia": 25,
    }
]


def aula(aulas):

    whiter = aulas
    whiter = whiter.upper()

    return whiter
print(aula(arquivo_json[0]['Escola']))