from datetime import datetime

def split_full_name(full_name: str):
    parts = full_name.strip().split()

    if len(parts) == 1:
        return parts[0], "" 

    if len(parts) == 2:
        return parts[0], parts[1]

    first_names = parts[:-2]
    last_names = parts[-2:]

    particles = {"de", "del", "de", "la", "las", "los", "y"}

    if len(parts) >= 3:
        if parts[-2].lower() in particles:
            first_names = parts[:-3]
            last_names = parts[-3:]

        elif len(parts) >= 4 and parts[-3].lower() == "de" and parts[-2].lower() == "la":
            first_names = parts[:-4]
            last_names = parts[-4:]

    first_name = " ".join(first_names).strip()
    last_name = " ".join(last_names).strip()

    return first_name, last_name



def age_to_birthdate(age):
    if age is None or str(age).strip() == "":
        return "1970-01-01 00:00:00+00"

    try:
        age = int(float(age))
    except (ValueError, TypeError):
        return "1970-01-01 00:00:00+00"

    current_year = datetime.utcnow().year
    birth_year = current_year - age

    return f"{birth_year}-01-01 00:00:00+00"


def clean_number(value):
    try:
        num = float(value)
        return int(num) if num.is_integer() else num
    except:
        return None


def log_error(lista_errores, row, motivo):
    lista_errores.append(f"ERROR: {motivo} | DATA: {list(row)}")