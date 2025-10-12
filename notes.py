from typing import List, Tuple

"""raise, c’est pour signaler une erreur volontairement
Quand ton code rencontre une situation anormale ou inattendue, tu peux dire à Python :
“Stoppe tout, quelque chose ne va pas ici.

raise -> Lancer une exception
raise ValueError("message") -> Signaler une erreur spécifique
try/except -> Intercepter une erreur levée
raise sans argument (dans un except) -> Relancer la même erreur """


def collect_number_of_notes(question: str) -> int:
    """Demander à l'utilisateur combien de notes il souhaite saisir (entier > 0)."""

    while True:
        # isdigit()
        # Vérifie que c'est un nombre et obliger à taper un chiffre et pas une lettre au autre caractères
        if question.isdigit():
            question = int(question)
            if 0 < question <= 10:  # if question > 0 and question <= 10:
                return question  # on renvoie directement l'entier valide
            print(
                " Le nombre de notes doit être supérieur à 0 ou < ou = 10 !"
            )  # ZeroDivisionError : division by zero
        else:
            print("⚠️ Tapez un chiffre valide !")
        # redemander la saisie si invalide

        question = input("Combien de notes veux-tu entrer ? ")

    # raise NotImplementedError # → sert de placeholder, pour marquer “pas encore codé”.


def collect_note(i: int) -> int:
    """Demander une note (décimale possible) pour l'index donné, la valider et renvoyer la note."""
    while True:
        note = input(f" Entrez la note {i + 1}: ")
        if note.isdigit():
            return int(note)
        else:
            print("⚠️ Veuillez entrer un nombre valide pour la note.")


def compute_stats(notes: List[float]) -> Tuple[float, float, float, float]:
    """Retourne (somme, moyenne, min, max) pour la liste de notes (liste non vide)."""
    total = sum(notes)
    moyenne = total / len(notes)
    print(f" La moyenne est de: {round(moyenne, 2)}")
    minimum = min(notes)
    maximum = max(notes)

    if moyenne < 10:
        print(" Appréciation: Peut mieux faire 😢")
    elif moyenne >= 15:
        print(" Appréciation: Très bien 🙂")
    elif moyenne >= 10:
        print(" Appréciation: Passable 🙂")

    return total, moyenne, minimum, maximum 
   # raise NotImplementedError


def format_report(notes: List[float], stats: Tuple[float, float, float, float]) -> str:
    """Renvoie une chaîne contenant un résumé lisible (notes, moyenne arrondie, appréciation)."""
    raise NotImplementedError


def notes() -> None:
    question = input(f" Combien de notes veux-tu entrer ? ")
    nb_notes = collect_number_of_notes(question)
    notes: List[int] = []

    for i in range(nb_notes):
        note = collect_note(i)
        notes.append(note)

    print(" Notes :", notes)

    total, moyenne, minimum, maximum = compute_stats(notes)
    print(f" Total : {total}, Moyenne : {moyenne}, Min : {minimum}, Max : {maximum}")

    # raise NotImplementedError


if __name__ == "__notes__":
    notes()
