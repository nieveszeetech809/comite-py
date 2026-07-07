def sql_value(value):
    if value is None or str(value).strip() == "" or str(value).lower() == "nan":
        return "NULL"

    value = str(value).replace("'", "''")
    return f"'{value}'"


