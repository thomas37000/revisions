from typing import List, Tuple

"""raise, c’est pour signaler une erreur volontairement
Quand ton code rencontre une situation anormale ou inattendue, tu peux dire à Python :
“Stoppe tout, quelque chose ne va pas ici.

raise -> Lancer une exception
raise ValueError("message") -> Signaler une erreur spécifique
try/except -> Intercepter une erreur levée
raise sans argument (dans un except) -> Relancer la même erreur """s


def collect_number_of_notes() -> int:
    """Demander à l'utilisateur combien de notes il souhaite saisir (entier > 0)."""
    raise NotImplementedError


def collect_note(index: int) -> float:
    """Demander une note (décimale possible) pour l'indice donné, la valider et renvoyer la note."""
    raise NotImplementedError


def compute_stats(notes: List[float]) -> Tuple[float, float, float, float]:
    """Retourne (somme, moyenne, min, max) pour la liste de notes (liste non vide)."""
    raise NotImplementedError


def format_report(notes: List[float], stats: Tuple[float, float, float, float]) -> str:
    """Renvoie une chaîne contenant un résumé lisible (notes, moyenne arrondie, appréciation)."""
    raise NotImplementedError


def main() -> None:
    """Orchestre le programme : collecte, calcul, affichage."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
