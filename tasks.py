import csv
import os
from typing import List, Dict
from utils.ask_continue import ask_continue


def load_tasks(filename: str = "tasks.csv") -> List[Dict]:
    """Charge les tasks depuis un fichier CSV, s'il existe."""
    if not os.path.exists(filename):
        print("⚠️ Aucun fichier CSV trouvé, démarrage à vide.")
        return []

    tasks = []
    with open(filename, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                tasks.append(
                    {
                        "id": row["id"],
                        "titre": row["titre"],
                        "description": row["description"],
                        "priorite": row["priorite"],
                        "statut": row["statut"],
                    }
                )
            except ValueError:
                print(f"⚠️ Ligne ignorée : données invalides pour '{row['titre']}').")

    print(f"📂 {len(tasks)} tâches chargées depuis {filename}.")
    return tasks


def save_tasks(tasks: List[Dict], filename: str = "tasks.csv") -> None:
    """Sauvegarde la liste des tâches dans un fichier CSV."""
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "titre", "description", "priorite", "statut"])

        # enumerate() permet d’ajouter un index automatiquement, en partant de 1
        for i, ta in enumerate(tasks, start=1):
            try:
                writer.writerow(
                    [
                        i,
                        ta["titre"],
                        ta["description"],
                        ta["priorite"],
                        ta["statut"],
                    ]
                )
            except KeyError as e:
                print(f"⚠️ Champ manquant dans la tâche : {e}")
                continue
    print(f"💾 Données sauvegardées dans {filename}")


def display_tasks(tasks: List[Dict]) -> None:
    """Affiche la liste des tâches dans un format lisible."""
    if not tasks:
        print("📦 Aucune tâche dans la liste.")
        return

    print("\n=== Todolist ===")
    print(
        f"{'id':<5} {'Titre':<20} {'Description':<30} {'Priorité':<20} {'Statut':<10}"
    )
    print("-" * 100)

    for ta in tasks:
        print(
            f"{ta['id']:<5} {ta['titre']:<20} {ta['description']:<30} {ta['priorite']:<20} {ta['statut']:<10}"
        )
        print("-" * 100)


def collect_title_task(i: int) -> str:
    """Demande le titre de la tâche"""
    while True:
        titre = input(f"Titre de la tâche {i + 1} : ").strip()
        if titre:
            return titre
        print("⚠️ Le titre ne peut pas être vide.")


def collect_desc_task(i: int) -> str:
    """Demande la description de la tâche"""
    while True:
        description = input(f"Description de la tâche {i + 1} : ").strip()
        if description:
            return description
        print("⚠️ La description ne peut pas être vide.")


def collect_priority_task() -> str:
    """Demande une priorité valide (faible / moyenne / haute)."""
    options = ["faible", "moyenne", "haute"]

    while True:
        print("\nChoisissez la priorité :")
        for i, opt in enumerate(options, start=1):
            print(f"{i}. {opt.capitalize()}")

        choix = input("👉 Votre choix (1-3) : ").strip()

        if choix in ["1", "2", "3"]:
            return options[int(choix) - 1]

        print("⚠️ Choix invalide. Veuillez entrer 1, 2 ou 3.")


def collect_status_task() -> str:
    """Demande un statut valide (à faire / en cours / terminé)."""
    options = ["à faire", "en cours", "terminé"]

    while True:
        print("\nChoisissez le statut :")
        for i, opt in enumerate(options, start=1):
            print(f"{i}. {opt.capitalize()}")

        choix = input("👉 Votre choix (1-3) : ").strip()

        if choix in ["1", "2", "3"]:
            return options[int(choix) - 1]

        print("⚠️ Choix invalide. Veuillez entrer 1, 2 ou 3.")


def add_task(tasks: List[Dict]) -> None:
    """Ajoute un ou plusieurs tâches."""
    nb_tasks = int(input("Combien de tâches veux-tu ajouter ? "))

    for i in range(nb_tasks):
        # L’ID = len(tasks) + 1 pour éviter les doublons
        task_id = len(tasks) + 1
        titre = collect_title_task(i)
        description = collect_desc_task(i)
        priorite = collect_priority_task()
        statut = collect_status_task()

        tasks.append(
            {
                "id": task_id,
                "titre": titre,
                "description": description,
                "priorite": priorite,
                "statut": statut,
            }
        )

        print(f"✅ tâche '{titre}' ajoutée avec succès !")


def mark_task_done(tasks: List[Dict]) -> None:
    return False


def collect_new_task(old_task: str) -> str:
    # Demande une nouvelle tâche (ou le même) pour une tâche existante."""
    titre = input(
        f"Titre actuel : {old_task}. Nouvelle tâche (laisser vide pour garder le même) : "
    ).strip()
    return titre if titre else old_task


def collect_new_desc(old_desc: str) -> str:
    # Demande une nouvelle description (ou le même) pour une tâche existante."""
    description = input(
        f"description actuel : {old_desc}. Nouvelle description (laisser vide pour garder le même) : "
    ).strip()
    return description if description else old_desc


def collect_new_priority(old_priority: str) -> str:
    options = ["faible", "moyenne", "haute"]

    while True:
        print(f"\nPriorité actuelle : {old_priority}")
        print("\nChoisissez la priorité :")
        for i, opt in enumerate(options, start=1):
            print(f"{i}. {opt.capitalize()}")

        choix = input("👉 Votre choix (1-3) : ").strip()

        if choix in ["1", "2", "3"]:
            return options[int(choix) - 1]
        else:
            old_priority

        print("⚠️ Choix invalide. Veuillez entrer 1, 2 ou 3.")


def collect_new_status(old_status: str) -> str:
    options = ["à faire", "en cours", "terminé"]

    while True:
        print(f"\nStatut actuel : {old_status}")
        print("\nChoisissez le statut :")
        for i, opt in enumerate(options, start=1):
            print(f"{i}. {opt.capitalize()}")

        choix = input("👉 Votre choix (1-3) : ").strip()

        if choix in ["1", "2", "3"]:
            return options[int(choix) - 1]
        else:
            old_status

        print("⚠️ Choix invalide. Veuillez entrer 1, 2 ou 3.")


def update_task(tasks: List[Dict]):
    while True:

        id_task = int(input("N° de la tâche à modifier : ").strip())
        # titre = input("Titre de la tâche à modifier : ").strip()
        found = False

        for ta in tasks:
            # if int(ta["id"]) == id_task or ta["titre"].lower() == titre.lower():
            if int(ta["id"]) == id_task:
                print(f"tâche trouvée : {ta['titre']}")
                ta["titre"] = collect_new_task(ta["titre"])
                ta["description"] = collect_new_desc(ta["description"])
                ta["priorite"] = collect_new_priority(ta["priorite"])
                ta["statut"] = collect_new_status(ta["statut"])
                print("✅ tâche mis à jour !")

                found = True
                break

        for index, t in enumerate(tasks, start=1):
            t["id"] = index

        if not found:
            print("⚠️ tâche non trouvée.")

        if not ask_continue(" Modifier une autre tâche ? (o/n) : "):
            print("👋 Retour au menu principal.")
            break


def delete_task(tasks: List[Dict]) -> None:
    """Supprime une tâche de la liste par son titre, avec option d'arrêt."""
    while True:

        id_task = int(input("N° de la tâche à supprimer : ").strip())
        found = False

        for ta in tasks:
            if int(ta["id"]) == id_task:
                confirmation = (
                    input(f"Confirmer la suppression de {ta['titre']} ? (o/n) : ")
                    .strip()
                    .lower()
                )
                if confirmation == "o":
                    tasks.remove(ta)
                    print(f"✅ tâche '{ta['titre']}' supprimé avec succès !")
                else:
                    print("❌ Suppression annulée.")
                found = True
                break

        if not found:
            print("⚠️ tâche non trouvée.")

        # Réattribue des IDs cohérents après suppression
        for index, t in enumerate(tasks, start=1):
            t["id"] = index

        if not ask_continue("Voulez-vous continuer la suppression ? (o/n) : "):
            print("👋 Retour au menu principal.")
            break


def todo_list() -> None:  # fonction principale
    tasks = []

    tasks = load_tasks()  # ← charge les anciens

    if tasks:
        print("\nListe des tâches :")
        display_tasks(tasks)

    print("\n=== 📒 Menu ===")
    print(
        f"{'Ajouter(a)':<10} {'Modifier(m)':<10} {'Supprimer(d)':<10} {'Liste des tâches(v)':<10} {'Quitter(q)':<10}"
    )

    while True:
        action = input("\na/m/d/v/q : ").strip().lower()

        # ---- Ajouter ----
        if action == "a":
            add_task(tasks)

        # ---- Modifier ----
        elif action == "m":
            update_task(tasks)

        # ---- Supprimer ----
        elif action == "d":
            delete_task(tasks)

        # ---- Voir ----
        elif action == "v":
            display_tasks(tasks)

        # ---- Quitter ----
        elif action == "q":
            print("👋 À bientôt !")
            break

        else:
            print("Aucune modification effectuée.")

    save_tasks(tasks)


if __name__ == "__todo_list__":
    todo_list()
