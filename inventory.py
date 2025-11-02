import csv
import os
from typing import List, Dict


def display_inventory(produits: List[Dict]) -> None:
    """Affiche la liste des produits dans un format lisible."""
    if not produits:
        print("📦 Aucun produit dans l'inventaire.")
        return

    print("\n=== Inventaire ===")
    print(f"{'Nom':<20} {'Quantité':<10} {'Prix (€)':<10} {'Valeur (€)':<10}")
    print("-" * 55)

    total = 0
    for pro in produits:
        try:
            quantite = int(pro["quantite"])
            prix = float(pro["prix"])
        except ValueError:
            print(f"⚠️ Données invalides pour {pro['nom']}")
            continue

        valeur = quantite * prix
        total += valeur
        print(f"{pro['nom']:<20} {quantite:<10} {prix:<10.2f} {valeur:<10.2f}")

    print("-" * 55)
    print(f"Valeur totale du stock : {total:.2f} €")


def collect_item_name(i: int) -> str:
    """Demande le nom du produit"""
    while True:
        name = input(f"Nom du produit {i + 1} : ").strip()
        if name:
            return name
        print("⚠️ Le nom ne peut pas être vide.")


def collect_item_quantite(i: int) -> int:
    """Demande la quantité du produit"""
    while True:
        quantite = input(f"Quantité du produit {int(i)} : ").strip()
        try:  # on vérifie que c'est bien un chiffre et ensuite on vérifie que c'est bien > 0
            if quantite.isdigit():
                valeur = int(quantite)
                if valeur > 0:
                    return valeur
                else:
                    print("⚠️ La quantité doit être un chiffre supérieur à 0")

        except ValueError:
            print("⚠️ Entrez un nombre valide (ex: 3)")


def collect_item_prix(i: int) -> float:
    """Demande le prix du produit"""
    while True:
        prix = input(f"Prix du produit {int(i)} : ").strip()
        try:
            if float(prix) > 0:
                return prix
            else:
                print("⚠️ Le prix doit être un chiffre supérieur à 0")

        except ValueError:
            print("⚠️ Entrez un nombre valide (ex: 12 ou 12.5)")


def collect_new_name(old_name: str) -> str:
    # Demande un nouveau nom (ou le même) pour un produit existant."""
    name = input(
        f"Nom actuel : {old_name}. Nouveau nom (laisser vide pour garder le même) : "
    ).strip()
    return name if name else old_name


def collect_new_quantite(old_quantite: int) -> int:
    # Demande une nouvelle quantitée (ou le même) pour un produit existant."""
    quantite = input(
        f"Quantité actuel : {old_quantite}. Nouvelle quantitée (laisser vide pour garder le même) : "
    ).strip()
    return quantite if quantite else old_quantite


def collect_new_price(old_price: int) -> int:
    # Demande une nouvelle quantitée (ou le même) pour un produit existant."""
    prix = input(
        f"Quantité actuel : {old_price}. Nouvelle quantitée (laisser vide pour garder le même) : "
    ).strip()
    return prix if prix else old_price


def add_inventory(produits: List[Dict]):
    """Ajoute un ou plusieurs produits."""
    nb_produits = int(input("Combien de produits veux-tu ajouter ? "))

    for i in range(nb_produits):
        nom = collect_item_name(i)
        quantite = collect_item_quantite(i)
        prix = collect_item_prix(i)

        produits.append({"nom": nom, "quantite": quantite, "prix": prix})
    return produits


def update_inventory(produits: List[Dict]):
    nom = input("Nom du produit à modifier : ").strip()
    found = False

    for pro in produits:
        if pro["nom"].lower() == nom.lower():
            print(f"Produit trouvé : {pro['nom']}")
            pro["nom"] = collect_new_name(pro["nom"])
            pro["quantite"] = collect_item_quantite(pro["quantite"])
            pro["prix"] = collect_item_prix(pro["prix"])
            found = True
            break
    if not found:
        print("⚠️ Produit non trouvé.")


def delete_inventory(produits):
    """Supprime un produit de l'inventaire par son nom, avec option d'arrêt."""
    while True:
        nom = input("Nom du produit à supprimer : ").strip()
        found = False

        for pro in produits:
            if pro["nom"].lower() == nom.lower():
                confirmation = (
                    input(f"Confirmer la suppression de {pro['nom']} ? (o/n) : ")
                    .strip()
                    .lower()
                )
                if confirmation == "o":
                    produits.remove(pro)
                    print(f"✅ Produit '{pro['nom']}' supprimé avec succès !")
                else:
                    print("❌ Suppression annulée.")
                found = True
                break

        if not found:
            print("⚠️ Produit non trouvé.")

        # Demande si on continue ou on arrête (comme fermer une popup)
        continuer = (
            input("Voulez-vous continuer la suppression ? (o/n) : ").strip().lower()
        )

        if continuer != "o":
            print("👋 Retour au menu principal.")
            break


# ---- Fonction principale ----
def inventory():
    produits = []

    produits = load_inventory()  # ← charge les anciens

    if produits:
        print("\nproduits existants :")
        display_inventory(produits)

    action = (
        input(
            "\nSouhaitez-vous ajouter un nouvel produit / modifier un existant ou en supprimer 1 ? (a/m/d) : "
        )
        .strip()
        .lower()
    )

    # ---- Ajouter ----
    if action == "a":
        add_inventory(produits)

    # ---- Modifier ----
    elif action == "m":
        update_inventory(produits)

    # ---- Supprimer ----
    elif action == "d":
        delete_inventory(produits)

    else:
        print("Aucune modification effectuée.")

    display_inventory(produits)
    save_inventory(produits)


def load_inventory(filename: str = "inventory.csv") -> List[Dict]:
    """Charge les produits depuis un fichier CSV, s'il existe."""
    if not os.path.exists(filename):
        print("⚠️ Aucun fichier CSV trouvé, démarrage à vide.")
        return []

    produits = []
    with open(filename, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                prix = float(row["prix"])
                quantite = int(row["quantite"])
                produits.append(
                    {
                        "nom": row["nom"],
                        "quantite": quantite,
                        "prix": prix,
                    }
                )
            except ValueError:
                print(
                    f"⚠️ Ligne ignorée : données invalides pour '{row['nom']}' (prix='{row['prix']}')."
                )

    print(f"📂 {len(produits)} produits chargés depuis {filename}.")
    return produits


def save_inventory(produits: List[Dict], filename: str = "inventory.csv") -> None:
    """Sauvegarde la liste des produits dans un fichier CSV."""
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["nom", "quantite", "prix"])  # en-têtes
        for pro in produits:
            writer.writerow([pro["nom"], pro["quantite"], pro["prix"]])
    print(f"💾 Données sauvegardées dans {filename}")


if __name__ == "__inventory__":
    inventory()
