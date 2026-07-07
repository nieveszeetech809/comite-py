import uuid
from src.utils.helper import base_query_table
from src.utils.sql_validatiion import sql_value
list_competions_participants =[]

def competion_participant(competion_id , participants_list , list_postions_id ,lists_disiplines ):
    for participant in participants_list:
        user_id = participant['user_id']
        disciplina = participant['desiplina']
        tipo = participant['type']

        disciplina_id = lists_disiplines.get(disciplina) 
        position_id = ''
        posicion_encontrada = next(
            (p for p in list_postions_id 
            if p['desiplina_id'] == disciplina_id 
            and p['name_position'] == "GENERAL"), 
            None
        )
        if not posicion_encontrada:
            continue

        position_id = posicion_encontrada['position_id']

        competion_participant_id = str(uuid.uuid4())
        competions_participant_insert=(
                f"({sql_value(competion_participant_id)}, "
                f"{sql_value(user_id)}, "
                f"{sql_value(competion_id)}, "
                f"{sql_value(position_id)}, "
                f"'2026-07-02 23:22:31.327+00', "
                f"'2026-07-02 23:22:31.327+00', "
                f"{sql_value('')})" 
            )
        list_competions_participants.append(competions_participant_insert)
    table_competion_participant()


def table_competion_participant():
    columnas_sql = [
        "_id",
        'participant_id',
        'competition_id',
        'position_id',
        '"createdAt"',
        '"updatedAt"',
        '"deletedAt"'
    ]
    insert_query = base_query_table("CompetitionParticipants" , columnas_sql,list_competions_participants )
  
    with open("CompetitionParticipants.sql", 'w', encoding='utf-8') as f:
        f.write(insert_query)