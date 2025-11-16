"""
format français
pattern = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/[0-9]{4}$"

Format ISO 8601, plus pratique pour le tri et l'import/export CSV

from datetime import datetime
date = datetime.strptime("2025-11-08", "%Y-%m-%d")
print(date.strftime("%d/%m/%Y"))  # 08/11/2025

"""

import re
from datetime import datetime


def validate_date(date_str: str) -> bool:
    """Valide que la date est au format YYYY-MM-DD et correspond à une vraie date."""
    pattern = r"^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"

    # Vérifie la forme (regex)
    if not re.match(pattern, date_str):
        return False

    # Vérifie que la date existe réellement
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
