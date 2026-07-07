import pandas as pd
import os
import uuid
from src.utils.participants import split_full_name ,age_to_birthdate ,clean_number ,log_error
from src.utils.sql_validatiion import sql_value
from src.athletes.athleta import generateTableAthletes ,generate_athletes
from src.utils.helper import base_query_table


lista_errores = []
lista_valores_atletas = []

mapSizePants = {
    "2XS": "XXS",
    "XS": "XS",
    "S": "S",
    "M": "M",
    "L": "L",
    "XL": "XL",
    "2XL": "XXL",
    "XXL":"XXL",
    "3XL": "XXXL",
    "XXXL":"XXXL",
    "4XL": "XXXXL", 
}


mapUuid = {
    "Deportista": "86aadf24-3ee0-4f5d-bd1f-d26fb3464f5a",
    "Delegado": "c3b30df3-3f15-436f-b81e-242e890289c2",
    "Entrenador": "aec0fb07-5b38-4991-a0a7-7825edc61b0d",
    "Técnico Mecánico": "cdca173e-8c4b-4f6b-b489-8a944115c68c",
    "Técnico Embarcaciones": "0e64e143-f11f-4600-abe9-f482f0add3a9",
    "Oficial Técnico": "49d1796f-0c6b-4892-9203-e23e8dfd2eba",
    "Mecánico": "3e0b5ecf-8de6-4f50-b2da-6fff55b87d10",
    "Entrenadora": "aec0fb07-5b38-4991-a0a7-7825edc61b0d",
    "Veterinario": "02ecab16-a8a0-4392-9a41-516e3370b46b",
    "Caballerango": "6ebc0472-a22c-415f-8fab-72a53baf5138"
}


def readExecl():
    list_participants = []
    if not os.path.exists('partcipants.xlsx'):
        print(f"Error: No se encontró el archivo partcipants.slsx en esta carpeta.")
        return
    
    if not os.path.exists('mails.xlsx'):
        print(f"Error: No se encontró el archivo mails.slsx en esta carpeta.")
        return


    # print("Leyendo el archivo Excel...")
    df = pd.read_excel('partcipants.xlsx')
    df = df.fillna('')

    df_mails = pd.read_excel('mails.xlsx')
    df_mails = df_mails.fillna('')

    # 
    # df_filtrado = df_mails.iloc[:, [0, 1]]
    # df_filtrado.columns = ['nombre', 'correo']
    # list_mails = df_filtrado.to_dict(orient='records')

    # 2. Obtener los nombres reales de las columnas por su posición numérica
    col_nombre = df_mails.columns[0]
    col_correo = df_mails.columns[1]

# 3. Crear el diccionario {Nombre: Correo} directo
    diccionario_contactos = dict(zip(df_mails[col_nombre], df_mails[col_correo]))
    # print(diccionario_contactos)


    def findEmail(name):
        email = diccionario_contactos.get(name)
        if email:
            return email
        else:
            return 'contacto@zeetech.com.mx'



    for index, row in df.iterrows():
        user_id = str(uuid.uuid4())
        nombre_completo = str(row.iloc[0]).strip()
        masculino = str(row.iloc[1]).strip()
        femenino = str(row.iloc[2]).strip()
        type_participant = str(row.iloc[3]).strip()
        get_pants_size =  str(row.iloc[5]).strip()
        get_foot_size =  str(row.iloc[6]).strip()
        email =  findEmail(nombre_completo.upper())
        first_name, last_name = split_full_name(nombre_completo)
        age = str(row.iloc[4]).strip()
        born_date = age_to_birthdate(age)

        gender = 'male'
        if masculino == '1':
            gender = 'male'
        if femenino == '1':
            gender = 'female'

        pants_size = mapSizePants.get(get_pants_size,"")
        foot_size = clean_number(get_foot_size)

        type_id = mapUuid.get(type_participant, "")
        if type_id == "":
            log_error(lista_errores, row, "TIPO PARTICIPANTE INVÁLIDO")
            continue

        if type_participant == "Deportista":
            generate_athletes(lista_valores_atletas, user_id)

        user_insert = (
            f"({sql_value(user_id)}, "
            f"{sql_value(first_name)}, "
            f"{sql_value(last_name)}, "
            f"{sql_value(born_date)}, "
            f"{sql_value(foot_size)}, "
            f"{sql_value(pants_size)}, "
            f"{sql_value(email)}, "
            f"{sql_value(type_id)}, "
            f"{sql_value(gender)}, "
            f"'2026-07-02 23:22:31.327+00', "
            f"'2026-07-02 23:22:31.327+00', "
            f"{sql_value('')})"
        )

        list_participants.append(user_insert)
        



    generateTableAthletes( list_athletes=lista_valores_atletas)
    generateTableParticipants(list_participants=list_participants)


def generateTableParticipants(list_participants):
    columnas_sql = [
        "_id",
        'name',
        'last_name',
        'born_date',
        'foot_size',
        'pants_size',
        'email',
        'type_id',
        'gender',
        '"createdAt"',
        '"updatedAt"',
        '"deletedAt"'
    ]
    insert_query = base_query_table("Participants", columnas_sql ,list_participants)
    
    with open("participants.sql", 'w', encoding='utf-8') as f:
        f.write(insert_query)
