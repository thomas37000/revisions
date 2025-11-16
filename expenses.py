import csv
import os
import json
from datetime import datetime
from typing import List, Dict
from operator import attrgetter, itemgetter
from matplotlib import pyplot as plt
from utils.ask_continue import ask_continue
from utils.delete_item import delete_item
from utils.validate_date import validate_date


# ---- Charge les dépenses depuis expenses.csv à chaque fois que le programme démarre l'app ----
def load_expenses(filename: str = "data/expenses.csv") -> List[Dict]:
    if not os.path.exists(filename):
        print("⚠️ Aucun fichier CSV trouvé, démarrage à vide.")
        return []

    expenses = []
    with open(filename, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                expenses.append(
                    {
                        "id": row["id"],
                        "date": row["date"],
                        "categorie": row["categorie"],
                        "montant": row["montant"],
                        "description": row["description"],
                    }
                )
            except ValueError:
                print(f"⚠️ Ligne ignorée : données invalides pour '{row['date']}').")

    print(f"📂 {len(expenses)} dépenses chargées depuis {filename}.")
    return expenses


# ---- Sauvegarde la liste des dépenses dans expenses.json quand on quitte l'app ----
def save_json(expenses: List[Dict], filename: str = "data/expenses.json") -> None:

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(
            expenses,
            f,
            ensure_ascii=False,
            indent=4,
        )

    print(f"💾 Données sauvegardées dans {filename}")


# ---- Sauvegarde la liste des dépenses dans expenses.csv quand on quitte l'app ----
def save_expenses(expenses: List[Dict], filename: str = "data/expenses.csv") -> None:

    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "date", "categorie", "montant", "description"])

        for i, ex in enumerate(expenses, start=1):
            try:
                writer.writerow(
                    [
                        i,
                        ex["date"],
                        ex["categorie"],
                        ex["montant"],
                        ex["description"],
                    ]
                )
            except KeyError as e:
                print(f"⚠️ Champ manquant dans la dépense : {e}")
                continue
    print(f"💾 Données sauvegardées dans {filename}")


# ---- TRI par Date ou Catégorie ou Montant ----
def sorted_by_date(expenses: List[Dict]) -> None:

    sorted_date = sorted(expenses, key=lambda x: x["date"])

    print(
        f"{'id':<5} {'date':<15} {'Catégorie':<15} {'Montant':<10} {'Description':<30}"
    )
    print("-" * 100)

    for ex in sorted_date:
        print(
            f"{ex['id']:<5} {ex['date']:<15} {ex['categorie']:<15} {ex['montant']:>10} €  {ex['description']:<30}"
        )

        print("-" * 100)


def sorted_by_cat(expenses: List[Dict]) -> None:

    sorted_cat = sorted(expenses, key=lambda x: x["categorie"])

    print(
        f"{'id':<5} {'date':<15} {'Catégorie':<15} {'Montant':<10} {'Description':<30}"
    )
    print("-" * 100)

    for ex in sorted_cat:
        print(
            f"{ex['id']:<5} {ex['date']:<15} {ex['categorie']:<15} {ex['montant']:>10} €  {ex['description']:<30}"
        )

        print("-" * 100)


def sorted_by_sum(expenses: List[Dict]) -> None:

    sorted_sum = sorted(expenses, key=lambda x: float(x["montant"]))

    print(
        f"{'id':<5} {'date':<15} {'Catégorie':<15} {'Montant':<10} {'Description':<30}"
    )
    print("-" * 100)

    for ex in sorted_sum:
        print(
            f"{ex['id']:<5} {ex['date']:<15} {ex['categorie']:<15} {ex['montant']:>10} €  {ex['description']:<30}"
        )

        print("-" * 100)


def display_by_sorted(expenses: List[Dict]) -> None:

    while True:
        print("\n=== Trier ===")
        print(f"{'Date(d)':<5} {'Catégorie(c)':<5} {'Montant(m)':<5} {'Menu(q)':<5}")
        sortedBy = input("\nd/c/m/q : ").strip().lower()
        print("\n")

        if sortedBy == "d":
            sorted_by_date(expenses)

        if sortedBy == "c":
            sorted_by_cat(expenses)

        if sortedBy == "m":
            sorted_by_sum(expenses)

        elif sortedBy == "q":
            print("Retour au menu")
            break


# ---- Filtrer par catégorie ou par intervalle de date ou par montant minimum / maximum ----
def filter_by_date(expenses: List[Dict]) -> None:
    date_min = input("Tapez la Date minimum à filtrer au format YYYY-MM-DD : ").strip()
    date_max = input("Tapez la Date maximum à filtrer au format YYYY-MM-DD : ").strip()

    filtered_date = sorted(
        filter(lambda x: date_min <= x["date"] <= date_max, expenses),
        key=lambda x: x["date"],
    )

    print(
        f"{'id':<5} {'date':<15} {'Catégorie':<15} {'Montant':<10} {'Description':<30}"
    )
    print("-" * 100)

    for ex in filtered_date:
        print(
            f"{ex['id']:<5} {ex['date']:<15} {ex['categorie']:<15} {ex['montant']:>10} €  {ex['description']:<30}"
        )

        print("-" * 100)


def filter_by_cat(expenses: List[Dict]) -> None:

    cat = collect_cat_expense()  # Choix de la catégorie

    # Filtre selon la catégorie choisie
    filter_cat = list(filter(lambda x: x["categorie"].lower() == cat.lower(), expenses))

    print("\n")
    print(
        f"{'id':<5} {'date':<15} {'Catégorie':<15} {'Montant':<10} {'Description':<30}"
    )
    print("-" * 100)

    for ex in filter_cat:
        print(
            f"{ex['id']:<5} {ex['date']:<15} {ex['categorie']:<15} {ex['montant']:>10} €  {ex['description']:<30}"
        )

        print("-" * 100)

    if not filter_cat:
        print("📦 Aucune dépense trouvée pour cette catégorie.")
        return


def filter_by_sum(expenses: List[Dict]) -> None:

    sum_max = float(input("Montant maximum (€) : ").strip())
    sum_min = float(input("Montant minimum (€) : ").strip())
    filtered = sorted(
        filter(lambda x: sum_min <= float(x["montant"]) <= sum_max, expenses),
        key=lambda x: float(x["montant"]),
    )

    print(
        f"{'id':<5} {'date':<15} {'Catégorie':<15} {'Montant':<10} {'Description':<30}"
    )
    print("-" * 100)

    for ex in filtered:
        print(
            f"{ex['id']:<5} {ex['date']:<15} {ex['categorie']:<15} {ex['montant']:>10} €  {ex['description']:<30}"
        )

        print("-" * 100)


def filter_expenses(expenses: List[Dict]) -> None:

    while True:
        print("\n=== Filtrer ===")
        print(f"{'Date(d)':<5} {'Catégorie(c)':<5} {'Montant(m)':<5} {'Menu(q)':<5}")
        filterBy = input("\nd/c/m/q : ").strip().lower()
        print("\n")

        if filterBy == "d":
            filter_by_date(expenses)

        if filterBy == "c":
            filter_by_cat(expenses)

        if filterBy == "m":
            filter_by_sum(expenses)

        elif filterBy == "q":
            print("Retour au menu")
            break


# ---- Affiche la liste des dépenses ----
def display_expenses(expenses: List[Dict]) -> None:

    if not expenses:
        print("📦 Aucune dépense dans la liste.")
        return

    print("\n=== Dépenses ===")
    print(
        f"{'id':<5} {'date':<15} {'Catégorie':<15} {'Montant':<10} {'Description':<30}"
    )
    print("-" * 100)

    """
    Tri avec lambda
    ✅ Avantage : très flexible — tu peux faire des calculs, conversions, conditions, etc.
    ⚠️ Inconvénient : un peu plus lent que itemgetter pour de gros volumes (négligeable pour des petits fichiers).
    """

    """
    Tri avec itemgetter
    itemgetter — pour extraire une ou plusieurs clés “brutes”
    itemgetter (de operator) est une fonction optimisée en C qui va chercher directement la valeur d' une ou plusieurs clés dans un dictionnaire ou tuple.
    ⚠️ Par contre, itemgetter ne permet aucun calcul — si tu veux convertir "montant" en float, tu dois repasser à lambda.
    """

    # sorted_expenses = sorted(
    #     expenses, key=itemgetter("date", "categorie", "montant") # Tri d'abord par date puis categorie puis montant
    # )  # , reverse=True => by desc

    for ex in expenses:
        print(
            f"{ex['id']:<5} {ex['date']:<15} {ex['categorie']:<15} {ex['montant']:>10} €  {ex['description']:<30}"
        )

        # total = sum(float(ex(["montant"])) for ex in expenses)
        # TypeError: 'dict' object is not callable
        # print(f"{'Total':<35} {total:>25} €")
        print("-" * 100)


# ---- Ajout d' une nouvelle dépense ----
def collect_date_expense(i: int) -> str:
    """Demande le date de la dépense au format YYYY-MM-DD"""
    while True:
        date = input(f"date de la dépense {i + 1} : ").strip()
        if not date:
            print("⚠️ Le date ne peut pas être vide.")
            continue

        if validate_date(date):
            return date
        else:
            print("⚠️ Format de date invalide")
            print("Format valide ex: 2025-11-01 de type YYYY-MM-DD")


def collect_cat_expense() -> str:
    """Demande une catégorie parmis les options."""

    categories = [
        "alimentation",
        "logement",
        "transport",
        "santé",
        "loisirs",
        "voyages",
        "cadeaux",
        "vêtements",
        "éducation",
        "abonnements",
        "impôts",
        "autre",
    ]

    while True:
        print("\nChoisissez la catégorie :")
        for i, cat in enumerate(categories, start=1):
            print(f"{i}. {cat.capitalize()}")

        choix = input("👉 Votre choix (1-12) : ").strip()

        if choix in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]:
            return categories[int(choix) - 1]

        print("⚠️ Choix invalide. Veuillez entrer 1, 2 ou 3.")


def collect_sum_expense(i: int) -> float:
    """Demande le montant de la dépense"""
    while True:
        montant = input(f"Montant de la dépense {int(i)} : ").strip()
        try:
            if float(montant) > 0:
                return montant
            else:
                print("⚠️ Le montant doit être un chiffre supérieur à 0")

        except ValueError:
            print("⚠️ Entrez un nombre valide (ex: 12 ou 12.5)")


def collect_desc_expense(i: int) -> str:
    """Demande la description de la dépense"""
    while True:
        description = input(f"Description de la dépense {i + 1} : ").strip()
        if description:
            return description
        print("⚠️ La description ne peut pas être vide.")


def add_expense(expenses: List[Dict]) -> None:
    """Ajoute un ou plusieurs dépenses."""
    nb_expenses = int(input("Combien de dépenses veux-tu ajouter ? "))

    for i in range(nb_expenses):
        expense_id = len(expenses) + 1
        date = collect_date_expense(i)
        categorie = collect_cat_expense()
        montant = collect_sum_expense(i)
        description = collect_desc_expense(i)

        expenses.append(
            {
                "id": expense_id,
                "date": date,
                "categorie": categorie,
                "montant": montant,
                "description": description,
            }
        )

        print(f"✅ dépense '{date}' ajoutée avec succès !")


# ---- Modification d'une dépense par key(date, catégorie ...) ----
def collect_new_date(old_date: str) -> str:
    # Demande une nouvelle date (ou le même) pour une dépense existante."""
    date = input(
        f"date actuelle : {old_date}. Nouvelle date (laisser vide pour garder le même) : "
    ).strip()
    return date if date else old_date


def collect_new_cat(old_cat: str) -> str:
    # Demande une nouvelle dépense (ou le même) pour une dépense existante."""
    categorie = input(
        f"Catégorie actuelle : {old_cat}. Nouvelle dépense (laisser vide pour garder le même) : "
    ).strip()
    return categorie if categorie else old_cat


def collect_new_sum(old_sum: str) -> str:
    # Demande une nouvelle monatnt (ou le même) pour une dépense existante."""
    montant = input(
        f"Montant actuel : {old_sum}. Nouveau montant (laisser vide pour garder le même) : "
    ).strip()
    return montant if montant else old_sum


def collect_new_desc(old_desc: str) -> str:
    # Demande une nouvelle description (ou le même) pour une dépense existante."""
    description = input(
        f"description actuel : {old_desc}. Nouvelle description (laisser vide pour garder le même) : "
    ).strip()
    return description if description else old_desc


def update_expense(expenses: List[Dict]):
    while True:

        id_expense = int(input("N° de la dépense à modifier : ").strip())
        # date = input("date de la dépense à modifier : ").strip()
        found = False

        for ex in expenses:
            if int(ex["id"]) == id_expense:
                print(f"dépense trouvée : {ex['date']}")
                ex["date"] = collect_new_date(ex["date"])
                ex["categorie"] = collect_new_cat(ex["categorie"])
                ex["montant"] = collect_new_sum(ex["montant"])
                ex["description"] = collect_new_desc(ex["description"])
                print("✅ dépense mis à jour !")

                found = True
                break

        for index, t in enumerate(expenses, start=1):
            t["id"] = index

        if not found:
            print("⚠️ dépense non trouvée.")

        if not ask_continue(" Modifier une autre dépense ? (o/n) : "):
            print("👋 Retour au menu principal.")
            break


# ---- Supprimer une dépense ----
def delete_expense(expenses: List[Dict]) -> None:
    delete_item(expenses, key="id", display_key="date", item_name="dépense")


# ---- Affiche un graphique de statistiques(ex : total par catégorie) ----
def display_graphic(expenses: List[Dict]) -> None:
    # création de la liste avant la boucle
    x_sum = []
    y_cat = []

    # convertir les catégories en nombres pour SCATTER avec un dict de mapping
    cat_to_num = {
        "alimentation": 1,
        "logement": 2,
        "transport": 3,
        "loisirs": 4,
        "autre": 5,
        "impôts": 6,
        "cadeaux": 7,
        "abonnements": 8,
    }

    for ex in expenses:
        x_sum.append(float(ex["montant"]))
        y_cat.append(cat_to_num[ex["categorie"]])

    plt.scatter(x_sum, y_cat, color="navy")
    plt.plot(x_sum, y_cat, color="navy")

    plt.title("Dépenses")

    plt.xlabel("x Montants")
    plt.ylabel("y Catégories")

    plt.show()


# ---- Fonction principale chargée depuis main.py ----
def expenses() -> None:
    expenses = []

    expenses = load_expenses()  # ← charge les anciennes dépenses

    if expenses:
        print("\nListe des dépenses :")
        display_expenses(expenses)

    print("\n=== 📒 Menu ===")
    print(
        f"{'Ajouter(a)':<5} {'Modifier(m)':<5} {'Supprimer(d)':<5} {'Lister(l)':<5} {'Statistiques(q)':<5} {'Trier(t)':<5} {'Filtrer(f)':<5} {'Graphique(g)':<5} {'Exportez en Json(e)':<5} {'Quitter(q)':<10}"
    )

    while True:
        action = input("\na/d/e/f/g/l/m/q/t : ").strip().lower()

        # ---- Ajouter ----
        if action == "a":
            add_expense(expenses)

        # ---- Modifier ----
        elif action == "m":
            update_expense(expenses)

        # ---- Supprimer ----
        elif action == "d":
            delete_expense(expenses)

        # ---- Liste des dépenses ----
        elif action == "l":
            display_expenses(expenses)

        # ---- Tri ----
        elif action == "t":
            display_by_sorted(expenses)

        # ---- Filtrer ----
        elif action == "f":
            filter_expenses(expenses)

        # ---- Json ----
        elif action == "e":
            save_json(expenses)

        # ---- Statistiques ----
        # elif action == "v":
        #     show_stats(expenses)

        # ---- Graphique ----
        elif action == "g":
            display_graphic(expenses)

        # ---- Quitter ----
        elif action == "q":
            print("👋 À bientôt !")
            break

        else:
            print("Aucune modification effectuée.")

    save_expenses(expenses)


if __name__ == "__expenses__":
    expenses()
