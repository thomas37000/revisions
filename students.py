import csv
import os
from typing import List, Dict, Tuple


# ---- 1. Demander combien d'étudiants ----
def collect_number_of_students() -> int:
    """Demande combien d'étudiants on veut saisir (entre 1 et 20)."""
    while True:
        n = input("Combien d'étudiants veux-tu ajouter ? ").strip()  # strip()
        # Remove spaces at the beginning and at the end of the string:
        # txt = "     banana     "
        # x = txt.strip()
        # print("of all fruits", x, "is my favorite")
        if n.isdigit():
            n = int(n)
            if 1 <= n <= 20:
                return n
            print("⚠️ Le nombre doit être entre 1 et 20.")
        else:
            print("⚠️ Entrez un nombre entier valide.")


# ---- 2. Demander le nom d'un étudiant ----
def collect_student_name(i: int) -> str:
    """Demande le nom du iᵉ étudiant."""
    while True:
        name = input(f"Nom de l'étudiant {i + 1} : ").strip()
        if name:
            return name
        print("⚠️ Le nom ne peut pas être vide.")


def collect_new_name(old_name: str) -> str:
    # Demande un nouveau nom (ou le même) pour un étudiant existant."""
    name = input(
        f"Nom actuel : {old_name}. Nouveau nom (laisser vide pour garder le même) : "
    ).strip()
    return name if name else old_name


# ---- 3. Demander les 3 notes d'un étudiant ----
def collect_student_notes() -> List[float]:
    notes = []
    for i in range(3):  # range(3) => Demander 3 notes entre 0 et 10, et les valide.
        while True:
            note = input(f"  Note {i + 1} : ").strip()
            try:
                note = float(note)
                if 0 <= note <= 20:
                    notes.append(note)
                    break
                else:
                    print("⚠️ La note doit être entre 0 et 20.")
            except ValueError:
                print("⚠️ Entrez un nombre valide (ex: 15 ou 12.5).")
    return notes


# ---- 4. Calcul des statistiques ----
def compute_stats(notes: List[float]) -> Tuple[float, float, float, float]:
    """Retourne (somme, moyenne, min, max)."""
    total = sum(notes)
    moyenne = total / len(notes)
    return total, moyenne, min(notes), max(notes)


# ---- 5. Calcul de l'appréciation ----
def compute_appreciation(moyenne: float) -> str:
    """Retourne une appréciation selon la moyenne."""
    if moyenne < 10:
        return "Peut mieux faire 😢"
    elif moyenne < 15:
        return "Passable 🙂"
    else:
        return "Très bien 😎"


# ---- 6. Affichage final ----
def display_summary(etudiants: List[Dict]):
    """Affiche le résumé complet de tous les étudiants."""
    print("\nRésumé des étudiants :")
    print("-" * 40)
    for etu in etudiants:
        print(
            f"{etu['nom']:<10} | Notes : {etu['notes']} | Moyenne : {etu['moyenne']:.2f} | {etu['appreciation']}"
        )
    print("-" * 40)


# ---- 7. Fonction principale ----
def students():
   # nb_etudiants = collect_number_of_students()
    etudiants = []

    etudiants = load_from_csv()  # ← charge les anciens
    if etudiants:
        print("\nÉtudiants existants :")
        display_summary(etudiants)

    action = (
        input(
            "\nSouhaitez-vous ajouter un nouvel étudiant ou modifier un existant ? (a/m) : "
        )
        .strip()
        .lower()
    )

    # ---- Ajouter ----
    if action == "a":
        nb_etudiants = collect_number_of_students()

        for i in range(nb_etudiants):
            nom = collect_student_name(i)
            notes = collect_student_notes()
            total, moyenne, _, _ = compute_stats(notes)
            appreciation = compute_appreciation(moyenne)

            etudiants.append(
                {
                    "nom": nom,
                    "notes": notes,
                    "moyenne": moyenne,
                    "appreciation": appreciation,
                }
            )

    # ---- Modifier ----
    elif action == "m":
        nom = input("Nom de l’étudiant à modifier : ").strip()
        found = False
        for etu in etudiants:
            if etu["nom"].lower() == nom.lower():
                print(f"Étudiant trouvé : {etu['nom']}")
                etu["nom"] = collect_new_name(etu["nom"])
                etu["notes"] = collect_student_notes()
                _, moyenne, _, _ = compute_stats(etu["notes"])
                etu["moyenne"] = moyenne
                etu["appreciation"] = compute_appreciation(moyenne)
                found = True
                break
        if not found:
            print("⚠️ Étudiant non trouvé.")

    else:
        print("Aucune modification effectuée.")

    display_summary(etudiants)
    save_to_csv(etudiants)


# ---- 8. CSV ----
def save_to_csv(etudiants: List[Dict], filename: str = "students.csv") -> None:
    """Sauvegarde la liste d'étudiants dans un fichier CSV."""
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["nom", "notes", "moyenne", "appreciation"])  # en-têtes
        for etu in etudiants:
            notes_str = ";".join(str(n) for n in etu["notes"])
            writer.writerow(
                [etu["nom"], notes_str, etu["moyenne"], etu["appreciation"]]
            )
    print(f"💾 Données sauvegardées dans {filename}")


def load_from_csv(filename: str = "students.csv") -> List[Dict]:
    """Charge les étudiants depuis un fichier CSV, s'il existe."""
    if not os.path.exists(filename):
        print("⚠️ Aucun fichier CSV trouvé, démarrage à vide.")
        return []

    etudiants = []
    with open(filename, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            notes = [float(x) for x in row["notes"].split(";")]
            etudiants.append(
                {
                    "nom": row["nom"],
                    "notes": notes,
                    "moyenne": float(row["moyenne"]),
                    "appreciation": row["appreciation"],
                }
            )
    print(f"📂 {len(etudiants)} étudiants chargés depuis {filename}.")
    return etudiants


# ---- Lancer le programme ----
if __name__ == "__students__":
    students()
