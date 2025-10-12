"""Fonction parse_note qui va recevoir une chaîne de texte (str) saisie par l’utilisateur via input().
Convertit la chaîne en float normalisé et lève ValueError si invalide.

Comportement souhaité :
accepte "12", "12.5", " 8 " → renvoie float
refuse "abc", "", -3, 25 → lève ValueError avec message utile
"""


def parse_note(s: str) -> float:
    try:
        valeur = float(s)
    except ValueError:
        raise ValueError("La note doit être un nombre.")
