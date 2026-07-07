from src.utils.helper import base_query_table
def generateTableDescipline(list_disciplines):
    columnas_sql = [
        "_id",
        'name',
        'sport_id',
        '"createdAt"',
        '"updatedAt"',
        '"deletedAt"'
    ]
    insert_query = base_query_table("Disciplines" , columnas_sql,list_disciplines )
  
    with open("disciplines.sql", 'w', encoding='utf-8') as f:
        f.write(insert_query)