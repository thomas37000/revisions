# utils/delete_item.py
from typing import List, Dict, Callable
from utils.ask_continue import ask_continue

def delete_item(
    items: List[Dict],
    key: str,
    display_key: str,
    item_name: str = "élément"
) -> None:
    """
    Supprime un item générique (tâche, contact, dépense, etc.) selon une clé (ex: 'id' ou 'nom').
    Peut être réutilisé dans plusieurs scripts.
    """
    while True:
        search = input(f"N° ou nom du {item_name} à supprimer : ").strip()
        found = False

        for it in items:
            if str(it.get(key)).lower() == search.lower():
                confirmation = input(
                    f"Confirmer la suppression de {it[display_key]} ? (o/n) : "
                ).strip().lower()

                if confirmation == "o":
                    items.remove(it)
                    print(f"✅ {item_name.capitalize()} '{it[display_key]}' supprimé avec succès !")
                else:
                    print("❌ Suppression annulée.")
                found = True
                break

        if not found:
            print(f"⚠️ {item_name.capitalize()} non trouvé.")

        # Réattribuer des IDs si applicable
        if key == "id":
            for index, i in enumerate(items, start=1):
                i["id"] = index

        if not ask_continue(f"Voulez-vous continuer la suppression d’un {item_name} ? (o/n) : "):
            print("👋 Retour au menu principal.")
            break
