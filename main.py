import csv
from io import StringIO

def extract_rows_from_sql(filepath):
    records = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Identificamos únicamente las líneas que son tuplas de valores
            if line.startswith("(") and (line.endswith("),") or line.endswith(");")):
                # Quitamos la coma o punto y coma final, y los paréntesis de los extremos
                clean_line = line.rstrip(",;").strip()[1:-1]
                
                # El módulo CSV de Python es infalible para separar strings con comillas simples y comas internas
                reader = csv.reader(StringIO(clean_line), quotechar="'", skipinitialspace=True, doublequote=True)
                try:
                    parsed_row = next(reader)
                    records.append(parsed_row)
                except StopIteration:
                    continue
    return records

def generar_script_migracion():
    # 1. Cargar ambos archivos
    original_rows = extract_rows_from_sql('participants.sql')
    generated_rows = extract_rows_from_sql('participants_segundo.sql')

    # 2. Crear un diccionario del archivo nuevo, indexado por (nombre, apellido, correo)
    generated_dict = {}
    for row in generated_rows:
        # Los índices: 1=name, 2=last_name, 4=foot_size, 5=pants_size, 6=email
        name = row[1]
        last_name = row[2]
        foot_size = row[4]
        pants_size = row[5]
        email = row[6]
        
        llave = (name, last_name, email)
        generated_dict[llave] = {
            'foot_size': foot_size,
            'pants_size': pants_size
        }

    updates = []
    deletes = []

    # 3. Recorrer la base original y comparar
    for row in original_rows:
        _id = row[0]
        name = row[1]
        last_name = row[2]
        email = row[6]
        
        llave = (name, last_name, email)
        
        if llave in generated_dict:
            # Sí existe: Sacamos sus nuevas tallas y armamos el ALTER/UPDATE
            nuevos_datos = generated_dict[llave]
            foot = nuevos_datos['foot_size']
            pants = nuevos_datos['pants_size']
            
            # Respetamos el formato SQL, si no es NULL le colocamos comillas simples
            foot_sql = f"'{foot}'" if foot != 'NULL' else "NULL"
            pants_sql = f"'{pants}'" if pants != 'NULL' else "NULL"
            
            sql = f"UPDATE public.\"Participants\" SET foot_size = {foot_sql}, pants_size = {pants_sql} WHERE _id = '{_id}';"
            updates.append(sql)
        else:
            # Faltan comparados con el primero: Generamos el DROP/DELETE
            sql = f"DELETE FROM public.\"Participants\" WHERE _id = '{_id}';"
            deletes.append(sql)

    # 4. Exportar las consultas al nuevo archivo SQL
    with open('migracion_actualizacion.sql', 'w', encoding='utf-8') as f:
        f.write("-- ==================================================\n")
        f.write("-- SCRIPT DE ACTUALIZACIÓN DE TALLAS (ALTER / UPDATE)\n")
        f.write("-- ==================================================\n")
        for u in updates:
            f.write(u + "\n")
            
        f.write("\n-- ==================================================\n")
        f.write("-- SCRIPT DE REGISTROS FALTANTES (DROP / DELETE)\n")
        f.write("-- ==================================================\n")
        for d in deletes:
            f.write(d + "\n")

    print(f"✅ ¡Éxito! Se detectaron {len(updates)} registros para actualizar y {len(deletes)} para eliminar.")
    print("Revisa el archivo 'migracion_actualizacion.sql'.")

if __name__ == "__main__":
    generar_script_migracion()