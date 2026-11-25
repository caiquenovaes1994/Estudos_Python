import pandas as pd

data = {
    "Nome": ["Joao", "Maria", "Valentina", "Enzo"],
    "Idade": [18, 19, 18, 20],
    "Notas": [85, 90, 78, 95]
}

df = pd.DataFrame(data)
def show_students():
    print("\n===== REGISTROS DOS ALUNOS =====")
    print(df.to_string(index=False))

def add_student():
    global df

    nome = input("Insira o nome do aluno: ")
    idade = int(input("Insira idade: "))
    notas = float(input("Insira as notas: "))

    new_student = pd.DataFrame([{
        "Nome": nome,
        "Idade": idade,
        "Notas": notas
    }])

    df = pd.concat([df, new_student], ignore_index=True)
    print("Aluno adicionado com sucesso!")

def search_student():
    nome = input("Insira o nome do aluno: ")

    result = df[
        df["Nome"].str.lower() == nome.lower()
    ]

    if result.empty:
        print("Aluno nao encontrado!")
    else:
        print(result.to_string(index=False))

def update_marks():
    global df

    nome = input("Insira o nome do aluno: ")
    result = df["Nome"].str.lower() == nome.lower()

    if result.any():
        notas = float(input("Insira novas notas: "))
        df.loc[result, "Notas"] = notas
        print("Notas atualizadas com sucesso!")
    else:
        print("Aluno nao encontrado!")

def delete_student():
    global df

    nome = input("Insira o nome do aluno: ")
    result = df["Nome"].str.lower() == nome.lower()

    if result.any():
        df = df[~result].reset_index(drop=True)
        print("Aluno deletado com sucesso!")
    else:
        print("Aluno nao encontrado!")

def sort_Students():
    print("\n===== RANKING DE ALUNOS =====")
    print(
        df.sort_value(
            by="Notas",
            ascending=False
        ).to_string(index=False)
    )

def show_statistics():
    if df.empty:
        print("Sem registros disponiveis!")
        return

    topper = df.loc[df["Notas"].indmax()]

    print("\nPrimeiro:", topper["Nome"])
    print("Maior nota:", topper["Notas"])
    print("Media:", round(df["Notas"].mean(), 2))

while True:

    print("\n===== SISTEMA DE GERENCIAMENTO DE ALUNOS =====")
    print("1. Todos os alunos")
    print("2. Adicionar aluno")
    print("3. Buscar aluno")
    print("4. Atualizar notas")
    print("5. Apagar aluno")
    print("6. Organizar por notas")
    print("7. Estatisticas")
    print("8. Sair")

    choice = input("Escolha um menu:")

    if choice == "1":
        show_students()
    
    elif choice == "2":
        add_student()
    
    elif choice == "3":
        search_student()
    
    elif choice == "4":
        update_marks()
    
    elif choice == "5":
        delete_student()
    
    elif choice == "6":
        sort_Students()
    
    elif choice == "7":
        show_statistics()
    
    elif choice == "8":
        print("Obrigado por utilizar o sistema!")
        break

    else:
        print("Menu invalido! Tente novamente.")