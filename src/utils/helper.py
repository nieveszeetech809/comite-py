def base_query_table(name ,columnas_sql , list):
    base_query =  f"""INSERT INTO public."{name}" ({', '.join(columnas_sql)}) VALUES\n"""
    return base_query + ",\n".join(list) + ";"