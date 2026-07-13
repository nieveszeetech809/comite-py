import questionary
import uuid
from src.utils.sql_validatiion import sql_value
from src.disciplines.dicipline import generateTableDescipline
from src.postions.positions import generateLogicPostions
from src.participants.particpants import readExecl
from src.utils.helper import base_query_table
from src.competion_participant.competion_participant import competion_participant

list_disiplines_to_insert = []
list_sports_to_insert = []
list_ids_disciplines = []
list_postions_id = []
lists_disiplines = {}

def generateTableSports():
    columnas_sql = [
        "_id",
        'name',
        '"createdAt"',
        '"updatedAt"',
        '"deletedAt"'
    ]

    insert_query = base_query_table("Sports", columnas_sql,list_sports_to_insert)
    with open("sports.sql", 'w', encoding='utf-8') as f:
        f.write(insert_query)


def generarScript():
    list_of_sports = {
        "ACUÁTICOS":[
            "AGUAS ABIERTAS",
            "CLAVADOS",
            "NATACIÓN",
            "NATACIÓN ARTÍSTICA",
            "POLO ACUÁTICO"
        ],
        "AJEDREZ":[
            "AJEDREZ"
        ],
        "BÁDMINTON":[
            "BÁDMINTON"
        ],
        "AO - TTO":[
            "PERSONAL COMITÉ"
        ],
        "ATLETISMO":[
            "ATLETISMO",
            "ATLETISMO MARCHA",
            "MEDIA MARATÓN"
        ],
        "BALONCESTO":[
            "BALONCESTO",
            "BALONCESTO 3X3"
        ],
        "BALONMANO":[
            "BALONMANO"
        ], 
        "BOLICHE":[
            "BOLICHE"
        ],
        "BÉISBOL":[
            "BÉISBOL"
        ],
        "BOXEO":[
            "BOXEO"
        ],
        "CANOTAJE":[
            "CANOTAJE VELOCIDAD"
        ],
        "CICLISMO":[
            "BMX RACING",
            "MTB",
            "PISTA",
            "RUTA"
        ],
        "ECUESTRE":[
            "ECUESTRE"
        ],
        "ESGRIMA":[
            "ESGRIMA"
        ],
        "ESQUÍ NAUTICO":[
            "ESQUÍ NAUTICO"
        ],
        "FUTBOL":[
            "FUTBOL"
        ],
        "GIMNASIA":[
            "GIMNASIA ARTÍSTICA F.",
            "GIMNASIA ARTÍSTICA V.",
            "GIMNASIA RÍTMICA",
            "GIMNASIA TRAMPOLÍN"
        ],
        "GOLF":[
            "GOLF"
        ],
        "HOCKEY CÉSPED":[
            "HOCKEY CÉSPED"
        ],
        "JUDO":[
            "JUDO"
        ],
        "KARATE":[
            "KARATE"
        ],
        "LEV. PESAS":[
            "LEV. PESAS"
        ],
        "LUCHAS":[
            "LUCHAS"
        ],
        "PATINAJE":[
            "P. ARTÍSTICO",
            "SKATEBOARDING",
            "P. VELOCIDAD"
        ],
        "PENTATLÓN":[
            "PENTATLÓN"
        ],
        "PERSONAL MÉDICO, TÉCNICO - JEFATURA":[
            "PERSONAL COMITÉ"
        ],
        "RÁQUETBOL":[
            "RÁQUETBOL"
        ],
        "REMO":[
            "REMO"
        ],
        "RUGBY 7":[
            "RUGBY 7"
        ],
        "SOFTBOL":[
            "SOFTBOL"
        ],
        "SQUASH":[
            "SQUASH"
        ],
        "SURF":[
            "SURF"
        ],
        "TAEKWONDO":[
            "TAEKWONDO"
        ],
        "TENIS":[
            "TENIS"
        ],
        "TENIS DE MESA":[
            "TENIS DE MESA"
        ],
        "TIRO":[
            "TIRO ESCOPETA",
            "TIRO PISTOLA",
            "TIRO RIFLE",
            "TIRO DEPORTIVO"
        ],
        "TIRO CON ARCO":[
            "TIRO CON ARCO"
        ],
        "TRIATLÓN":[
            "TRIATLÓN"
        ],
        "VELA":[
            "VELA"
        ],
        "VOLEIBOL":[
            "VOLEIBOL PLAYA",
            "VOLEIBOL SALA"
        ],
        "PERSONAL":[
            "PERSONAL ADMINISTRATIVO",
            "PERSONAL MÉDICO",
            "PERSONAL TÉCNICO"
        ],
        "SEGURIDAD":[
            "SEGURIDAD"
        ],
        "DEPORTE SEGURO":[
            "DEPORTE SEGURO"
        ],
        "ATACHÉ":[
            "ATACHÉ PRENSA",
            "ATACHÉ CENTOAM",
        ],
        "JEFE DE MISIÓN":[
            "JEFE DE MISIÓN"
        ],
        "SUBJEFE DE MISIÓN":[
            "SUBJEFE DE MISIÓN"
        ],
        "PRESIDENTA COM":[
            "PRESIDENTA COM"
        ],
        "SECRETARIO G. COM":[
            "SECRETARIO G. COM"
        ]
    }

    for sport ,desiplines in list_of_sports.items():
        sport_id = str(uuid.uuid4())
        sport_insert = (
            f"({sql_value(sport_id)}, "
            f"{sql_value(sport)}, "
            f"'2026-07-02 23:22:31.327+00', "
            f"'2026-07-02 23:22:31.327+00', "
            f"{sql_value('')})"
        )
        list_sports_to_insert.append(sport_insert)


        for discipline in desiplines:
            position_id = str(uuid.uuid4())
            descipline_insert=(
                f"({sql_value(position_id)}, "
                f"{sql_value(discipline)}, "
                f"{sql_value(sport_id)}, "
                f"'2026-07-02 23:22:31.327+00', "
                f"'2026-07-02 23:22:31.327+00', "
                f"{sql_value('')})" 
            )
            lists_disiplines[discipline] = position_id
            list_ids_disciplines.append(position_id)
            list_disiplines_to_insert.append(descipline_insert)

    generateTableSports()
    generateTableDescipline(list_disciplines=list_disiplines_to_insert)
    list_postions_id = generateLogicPostions(list_ids_disciplines)
    
    listparticpants = readExecl()
    ask_generate_competions_participant = questionary.confirm("Are you need integrate competition?").ask()
    if ask_generate_competions_participant:
        # 23cb78ff-8c87-4ada-81d2-9b641593815d
        competition_id = questionary.text("What's the competion_id").ask()
        competion_participant(competition_id,listparticpants , list_postions_id ,lists_disiplines)