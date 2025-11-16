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
