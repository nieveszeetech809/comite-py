import uuid
from src.utils.sql_validatiion import sql_value
from src.utils.helper import base_query_table

def generateTableAthletes(list_athletes):
    columnas_sql = [
        "_id",
        'participant_id',
        '"createdAt"',
        '"updatedAt"',
        '"deletedAt"'
    ]
    insert_query = base_query_table("Athletes",columnas_sql,list_athletes)
    with open("athletes.sql", 'w', encoding='utf-8') as f:
        f.write(insert_query)


def generate_athletes(lista_valores, participant_id):
    _id = str(uuid.uuid4())
    fila_valores = f"('{_id}', '{participant_id}', '2026-07-02 23:22:31.327+00','2026-07-02 23:22:31.327+00', {sql_value('')})"
    lista_valores.append(fila_valores)