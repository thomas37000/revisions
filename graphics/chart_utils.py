from matplotlib import pyplot as plt
from typing import List, Dict


# ---- Affiche un graphique de statistiques(ex : total par catégorie) ----
def display_graphic(expenses: List[Dict]) -> None:
    # création de la liste avant la boucle
    x_sum = []
    y_cat = []

    # # convertir les catégories en nombres pour SCATTER avec un dict de mapping
    cat_to_num = {
        "alimentation": 1,
        "logement": 2,
        "transport": 3,
        "santé": 4,
        "loisirs": 5,
        "voyages": 6,
        "cadeaux": 7,
        "vêtements": 8,
        "éducation": 9,
        "abonnements": 10,
        "impôts": 11,
        "autre": 12,
    }

    x_sum = [float(ex["montant"]) for ex in expenses]
    y_cat = [cat_to_num[ex["categorie"]] for ex in expenses]

    plt.figure(figsize=(8, 5))  # largeur et hauteur de la fenêtre
    plt.scatter(x_sum, y_cat)

    plt.yticks(
        list(cat_to_num.values()), list(cat_to_num.keys())
    )  # affiche les points selon le montant et la catégorie
    plt.xlabel("Montants (€)")
    plt.ylabel("Catégories")
    plt.title("Dépenses")
    plt.grid(True)  # affiche en vue grille

    plt.show()
