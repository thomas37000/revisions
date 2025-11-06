def ask_continue(message: str = "Voulez-vous continuer ? (o/n) : ") -> bool:
    """
    Demande à l'utilisateur s'il veut continuer une action.
    Retourne True si 'o', sinon False.
    """
    while True:
        choix = input(message).strip().lower()
        if choix in ("o", "n"):
            return choix == "o"
        print("⚠️ Répondez par 'o' (oui) ou 'n' (non).")
