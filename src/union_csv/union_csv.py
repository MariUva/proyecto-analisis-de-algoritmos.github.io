import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


'''
Metodo que limpia las columnas (elimina algunas columnas)
'''
def limpiar_columnas_csv(directory_path_csv):
 # Obtiene las columnas estándar y sus posibles variantes
    nombre_columnas = crear_diccionario()

    # Recorre todos los archivos en el directorio
    for filename in os.listdir(directory_path_csv):
        if filename.endswith(".csv"):  # Verifica que sea un archivo CSV
            file_path = os.path.join(directory_path_csv, filename)
            print(f"Procesando archivo: {file_path}")
            
            try:
                # Lee el archivo CSV en un DataFrame
                df = pd.read_csv(file_path)
                
                # Diccionario para mapear las columnas actuales a las estandarizadas
                columnas_renombrar = {}

                # Busca las columnas en el CSV y las mapea a los nombres estandarizados
                for nombre_estandar, nombres_posibles in nombre_columnas.items():
                    for nombre in nombres_posibles:
                        if nombre in df.columns:
                            # Si encuentra una columna que coincide, la mapea al nombre estándar
                            columnas_renombrar[nombre] = nombre_estandar
                
                # Renombra las columnas en el DataFrame usando el diccionario
                df.rename(columns=columnas_renombrar, inplace=True)
                
                # Filtra el DataFrame para conservar solo las columnas que están en el diccionario
                columnas_a_conservar = list(columnas_renombrar.values())
                columnas_a_conservar = list(set(columnas_a_conservar))  # Elimina duplicados
                columnas_existentes = [col for col in columnas_a_conservar if col in df.columns]
                
                if not columnas_existentes:
                    print(f"Advertencia: Ninguna de las columnas a conservar se encuentra en {filename}")
                    continue
                
                # Conserva solo las columnas especificadas que existen
                df = df[columnas_existentes]
                
                # Reescribe el archivo CSV limpio sobre el archivo original
                df.to_csv(file_path, index=False)
                print(f"Archivo limpio guardado en: {file_path}")
            
            except Exception as e:
                print(f"Error procesando {filename}: {e}")
    
'''
Metodo que se encarga de unir toda la data en un solo archivo
'''
import os
import pandas as pd
import random

import os
import pandas as pd
import random

def unificar_data(directory_path_csv, nombre_csv_final):
    # Lista para almacenar los dataframes de cada archivo CSV
    dataframes = []

    # Recorre todos los archivos en la carpeta
    for archivo in os.listdir(directory_path_csv):
        if archivo.endswith('.csv'):  # Verificar que sea un archivo CSV
            ruta_archivo = os.path.join(directory_path_csv, archivo)
            # Leer el archivo CSV y agregarlo a la lista
            df = pd.read_csv(ruta_archivo)
            dataframes.append(df)

    # Concatenar todos los dataframes en uno solo
    df_final = pd.concat(dataframes, ignore_index=True)

    # Lista de países aleatorios
    paises = ["Colombia", "México", "Argentina", "Chile", "Inglaterra", "Brasil", "China", "Usa", "España", "Francia", "Alemania", "Rusia",  "Portugal",
               "India", "Ucrania", "Afganistan", "Nicaragua", "Filipinas", "Egipto"]

    # Agregar las columnas 'pais' y 'numero_citas' al final
    df_final['Country'] = [random.choice(paises) for _ in range(len(df_final))]
    df_final['Number of citation'] = [random.randint(1, 1000) for _ in range(len(df_final))]

    # Guardar el dataframe final en el archivo de salida
    ruta_completa = os.path.join(directory_path_csv, nombre_csv_final)
    df_final.to_csv(ruta_completa, index=False)

#Metodo para eliminar duplicados
def eliminar_duplicados(ruta,nombre_archivo):
    file_path = os.path.join(ruta, nombre_archivo)

        # Leer el archivo CSV
    df = pd.read_csv(file_path)

     # Concatenar las columnas relevantes (en este caso, 'titulo' y 'abstract') para comparar similitudes
    texto_concatenado = df[['Title', 'Abstract']].astype(str).agg(' '.join, axis=1)
    
    # Crear matriz de similitud utilizando TF-IDF
    vectorizer = TfidfVectorizer().fit_transform(texto_concatenado)
    similarity_matrix = cosine_similarity(vectorizer)
    
    # Configuración para el filtrado de similitud (ajusta el umbral según tus necesidades)
    umbral_similitud = 1
    eliminar_indices = set()
    
    # Comparar cada registro con los demás
    for i in range(len(df)):
        if i in eliminar_indices:
            continue
        for j in range(i + 1, len(df)):
            if j in eliminar_indices:
                continue
            if similarity_matrix[i, j] > umbral_similitud:
                # Determinar cuál es "menos completo" en base a los valores nulos
                if df.iloc[i].isna().sum() > df.iloc[j].isna().sum():
                    print(f"Eliminando registro duplicado: {df.iloc[i]['Title']}")
                    eliminar_indices.add(i)
                    
                else:
                    print(f"Eliminando registro duplicado: {df.iloc[j]['Title']}")
                    eliminar_indices.add(j)
    
    # Eliminar los registros identificados
    df_filtrado = df.drop(index=list(eliminar_indices))
    
    # Sobrescribir el archivo CSV original con el DataFrame filtrado
    df_filtrado.to_csv(file_path, index=False)
    print(f"Archivo '{nombre_archivo}' procesado y sobrescrito con {len(df_filtrado)} registros restantes.")


'''
Metodo el cual crea el diccionario para filtrar columnas'''
def crear_diccionario():
     # Crea el diccionario con las columnas estándar y sus posibles variantes
    nombres_columnas = {
        "Title": ["Article Title", "Title", "Document Title"],
        "Author": ["Author", "Authors"],
        "Publication Title": ["Publication Title", "Journal Title", "Source title"],
        "Year": ["Year", "Publication year", "Publication date"],
        "Volume": ["Volume"],
        "DOI": ["DOI"],
        "Issue": ["Issue"],
        "Publisher": ["Publisher"],
        "Abstract": ["Abstract"],
        "ISSN": ["ISSN"],
        "Pais": ["Pais"],
        "Numero de citas":["Numero de citas"]
    }
    return nombres_columnas

    
    