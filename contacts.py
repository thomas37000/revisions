import csv
import os
import re
from typing import List, Dict
from datetime import datetime


def display_contacts(contacts: List[Dict]) -> None:
    """Affiche la liste des contacts dans un format lisible."""
    if not contacts:
        print("📦 Aucun contact dans l'inventaire.")
        return

    print("\n=== Inventaire ===")
    print(f"{'Nom':<10} {'Télephone':<10} {'email':<20} {'Ville':<10}")
    print(
        "-" * 50
    )  # sert simplement à afficher une ligne horizontale de 50 tirets (-) dans la console.

    for co in contacts:
        try:
            telephone = int(co["telephone"])
        except ValueError:
            print(f"⚠️ Données invalides pour {co['nom']}")
            continue

        print(f"{co['nom']:<10} {telephone:<10} {co['email']:<20} {co['ville']:<10}")
        print("-" * 50)


def collect_item_name(i: int) -> str:
    """Demande le nom du contact"""
    while True:
        name = input(f"Nom du contact {i + 1} : ").strip()
        if name:
            return name
        print("⚠️ Le nom ne peut pas être vide.")


def collect_item_email(i: int) -> str:
    """Demande le email du contact"""
    while True:
        email = input(f"email du contact {i + 1} : ").strip()

        if not email:  # if not Vérifie si vide
            print("⚠️ Le email ne peut pas être vide.")
            continue  # on repart au début de la boucle sans tester le reste

        # Vérification simple avec une regex
        if re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email):
            return email
        else:
            print("⚠️ Format d'email invalide (ex : nom@example.com).")


def collect_item_telephone(i: int) -> str:
    """Demande le téléphone du contact"""
    while True:
        telephone = input(f"Télephone du contact {i + 1} : ").strip()

        if not telephone:
            print("⚠️ Le n° de télephone ne peut pas être vide.")
            continue

        # Supprime tous les caractères non numériques / chiffres
        digits = re.sub(r"\D", "", telephone)

        # Convertit un format +33 6... → 06...
        if digits.startswith("33") and len(digits) == 11:
            digits = "0" + digits[2:]

        # Vérifie que c’est un numéro français valide (10 chiffres)
        if len(digits) == 10 and digits.startswith("0"):
            return digits

        # Message si ce n’est pas un nombre
        print("⚠️ Le n° de télephone doit être ex : 0601020304.")


def collect_item_ville(i: int) -> str:
    """Demande la ville du contact"""
    while True:
        ville = input(f"Ville du contact {i + 1} : ").strip()
        if ville:
            return ville
        print("⚠️ La ville ne peut pas être vide.")


def collect_new_name(old_name: str) -> str:
    # Demande un nouveau nom (ou le même) pour un contact existant."""
    name = input(
        f"Nom actuel : {old_name}. Nouveau nom (laisser vide pour garder le même) : "
    ).strip()
    return name if name else old_name


def collect_new_email(old_email: str) -> str:
    # Demande un nouveau email (ou le même) pour un contact existant."""
    email = input(
        f"email actuel : {old_email}. Nouveau email (laisser vide pour garder le même) : "
    ).strip()
    return email if email else old_email


def collect_new_telephone(old_tel: int) -> int:
    # Demande un nouveau télephone (ou le même) pour un contact existant."""
    telephone = input(
        f"Télephone actuel : {old_tel}. Nouveau télephone (laisser vide pour garder le même) : "
    ).strip()
    return telephone if telephone else old_tel


def collect_new_city(old_city: str) -> str:
    # Demande un nouveau nom (ou le même) pour un contact existant."""
    ville = input(
        f"Ville actuel : {old_city}. Nouvelle ville (laisser vide pour garder le même) : "
    ).strip()
    return ville if ville else old_city


def add_contacts(contacts: List[Dict]):
    """Ajoute un ou plusieurs contacts."""
    nb_contacts = int(input("Combien de contacts veux-tu ajouter ? "))

    for i in range(nb_contacts):
        nom = collect_item_name(i)
        email = collect_item_email(i)
        telephone = collect_item_telephone(i)
        ville = collect_item_ville(i)

        contacts.append(
            {"nom": nom, "email": email, "telephone": telephone, "ville": ville}
        )

        print(f"✅ Contact '{nom}' ajouté avec succès !")
    return contacts


def update_contacts(contacts: List[Dict]):
    nom = input("Nom du contact à modifier : ").strip()
    found = False

    for co in contacts:
        if co["nom"].lower() == nom.lower():
            print(f"contact trouvé : {co['nom']}")
            co["nom"] = collect_new_name(co["nom"])
            co["email"] = collect_new_email(co["email"])
            co["telephone"] = collect_new_telephone(co["telephone"])
            co["ville"] = collect_new_city(co["ville"])
            print("✅ Contact mis à jour !")

            found = True
            break
    if not found:
        print("⚠️ contact non trouvé.")


def delete_contacts(contacts):
    """Supprime un contact de l'inventaire par son nom, avec option d'arrêt."""
    while True:
        nom = input("Nom du contact à supprimer : ").strip()
        found = False

        for co in contacts:
            if co["nom"].lower() == nom.lower():
                confirmation = (
                    input(f"Confirmer la suppression de {co['nom']} ? (o/n) : ")
                    .strip()
                    .lower()
                )
                if confirmation == "o":
                    contacts.remove(co)
                    print(f"✅ contact '{co['nom']}' supprimé avec succès !")
                else:
                    print("❌ Suppression annulée.")
                found = True
                break

        if not found:
            print("⚠️ contact non trouvé.")

        # Demande si on continue ou on arrête (comme fermer une popup)
        continuer = (
            input("Voulez-vous continuer la suppression ? (o/n) : ").strip().lower()
        )

        if continuer != "o":
            print("👋 Retour au menu principal.")
            break


# ---- Fonction principale ----
def contacts():
    contacts = []

    contacts = load_contacts()  # ← charge les anciens

    if contacts:
        print("\ncontacts existants :")
        display_contacts(contacts)

    print("\n=== 📒 Menu ===")
    print(
        f"{'Ajouter(a)':<10} {'Modifier(m)':<10} {'Supprimer(d)':<10} {'Liste des contacts(v)':<10} {'Quitter(q)':<10}"
    )

    while True:
        action = input("\na/m/d/v/q : ").strip().lower()

        # ---- Ajouter ----
        if action == "a":
            add_contacts(contacts)

        # ---- Modifier ----
        elif action == "m":
            update_contacts(contacts)

        # ---- Supprimer ----
        elif action == "d":
            delete_contacts(contacts)

        # ---- Voir ----
        elif action == "v":
            display_contacts(contacts)

        # ---- Quitter ----
        elif action == "q":
            print("👋 À bientôt !")
            break

        else:
            print("Aucune modification effectuée.")

    save_contacts(contacts)


def load_contacts(filename: str = "data/contacts.csv") -> List[Dict]:
    """Charge les contacts depuis un fichier CSV, s'il existe."""
    if not os.path.exists(filename):
        print("⚠️ Aucun fichier CSV trouvé, démarrage à vide.")
        return []

    contacts = []
    with open(filename, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                telephone = int(row["telephone"])
                contacts.append(
                    {
                        "nom": row["nom"],
                        "telephone": telephone,
                        "email": row["email"],
                        "ville": row["ville"],
                    }
                )
            except ValueError:
                print(
                    f"⚠️ Ligne ignorée : données invalides pour '{row['nom']}' (telephone='{row['telephone']}')."
                )

    print(f"📂 {len(contacts)} contacts chargés depuis {filename}.")
    return contacts


def save_contacts(contacts: List[Dict], filename: str = "data/contacts.csv") -> None:
    """Sauvegarde la liste des contacts dans un fichier CSV."""
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["nom", "telephone", "email", "ville"])  # en-têtes
        for co in contacts:
            # co["date_ajout"]
            writer.writerow([co["nom"], co["telephone"], co["email"], co["ville"]])
    print(f"💾 Données sauvegardées dans {filename}")


if __name__ == "__contacts__":
    contacts()
