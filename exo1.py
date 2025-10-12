"""
Tant que l'utlisateur tape un chiffre la boucle for peut s'excécuter:

    for n in range(int(question)) => pour chaque note dans question affiche autant de fois Entrez la note :
        range => commence à partir de 0
        range(start, begin, end)
        n + 1 pour que la 1° phrase Entre la note ne commence pas par 0
        append => permet d'insérer la valeur rentrée dans le tableau

    Sinon message d'érreurs jusqu'à que la condition soit respectée
"""

notes = []

while True:
    question = input(f" Combien de notes veux-tu entrer ? ")

    # isdigit()
    # Vérifie que c'est un nombre et obliger à taper un chiffre et pas une lettre au autre caractères
    if question.isdigit():
        question = int(question)
        if 0 < question <= 10:  # if question > 0 and question <= 10:
            break  # on sort de la boucle si c'est bon
        else:
            print(
                " Le nombre de notes doit être supérieur à 0 ou < ou = 10 !"
            )  # ZeroDivisionError : division by zero
    else:
        print("⚠️ Tapez un chiffre valide !")

for n in range(question):
    while True:
        note = input(f" Entrez la note {n + 1}: ")
        if note.isdigit():
            notes.append(int(note))
            break
        else:
            print("⚠️ Veuillez entrer un nombre valide pour la note.")

print("")

somme = sum(notes)
print(f" Somme des notes: {somme}")

moyenne = somme / len(notes)
print(f" La moyenne est de: {round(moyenne, 2)}")

if moyenne < 10:
    print(" Appréciation: Peut mieux faire 😢")
elif moyenne >= 15:
    print(" Appréciation: Très bien 🙂")
elif moyenne >= 10:
    print(" Appréciation: Passable 🙂")

print("")
