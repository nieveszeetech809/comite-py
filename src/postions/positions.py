import uuid
from src.utils.sql_validatiion import sql_value
from src.utils.helper import base_query_table
list_postions = []
list_postions_ids = []


def generateLogicPostions(list_disciplines_ids):
    position = ["ENTRENADOR","DELEGADO","GENERAL"]
    for name_position in position:
        for discipline_id in list_disciplines_ids:
            postion_id = str(uuid.uuid4())
            position_insert=(
                f"({sql_value(postion_id)}, "
                f"{sql_value(name_position)}, "
                f"{sql_value(discipline_id)}, "
                f"'2026-07-02 23:22:31.327+00', "
                f"'2026-07-02 23:22:31.327+00', "
                f"{sql_value('')})" 
            )
            list_postions.append(position_insert)
            list_postions_ids.append({"position_id":postion_id ,"desiplina_id":discipline_id , "name_position":name_position})
    generateTablePositions()
    return list_postions_ids

def generateTablePositions():
    columnas_sql = [
        "_id",
        'name',
        'discipline_id',
        '"createdAt"',
        '"updatedAt"',
        '"deletedAt"'
    ]
    insert_query = base_query_table("Positions", columnas_sql ,list_postions)

    with open("positions.sql", 'w', encoding='utf-8') as f:
        f.write(insert_query)