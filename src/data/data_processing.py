import pandas as pd  # Importa la librería pandas para manipular y analizar datos en forma de tablas.

def load_data(file_path):  # Define una función llamada 'load_data' que toma como argumento la ruta del archivo CSV.
    
    # Cargar el archivo CSV
    df = pd.read_csv(file_path)  # Utiliza la función 'read_csv' de pandas para leer el archivo CSV y cargarlo en un DataFrame (df).
    
    # Renombrar columnas si es necesario
    df.columns = [  # Renombra las columnas del DataFrame 'df' para que tengan nombres más descriptivos y fáciles de usar.
        'Volume',  # Título del artículo.
        'Author',  # Autor(es) del artículo.
        'Issn',  # Número ISSN de la revista.
        'Issue',  # Número de la edición o entrega (issue) de la publicación.
        'DOI',  # DOI (Identificador de Objeto Digital) del artículo.
        'Publisher',  # Editorial que publicó el artículo.
        'Abstract',  # Resumen del artículo.
        'Title',#Titulo
        'Publication Title',#Titulo de publicacioón
        'Year'#Ano de publicacion
    ]
    
    # Verificar valores faltantes
    missing_data = df.isnull().sum()  # Calcula el número de valores nulos (faltantes) en cada columna del DataFrame y lo almacena en 'missing_data'.
    print(f"Datos faltantes por columna:\n{missing_data}\n")  # Imprime una tabla mostrando cuántos valores faltantes hay en cada columna.
    
    # Mostrar número total de filas
    print(f"Total de filas en el archivo: {len(df)}")  # Muestra cuántas filas (registros) tiene el DataFrame, es decir, cuántos artículos se cargaron.
    
    # Extraer el año de la fecha de publicación
    df['year'] = pd.to_datetime(df['Year'], errors='coerce')  # Convierte la columna 'publication_date' a un formato de fecha y extrae el año de esa fecha. Si hay errores en la conversión, los ignora (coerce).
    
    return df  # Devuelve el DataFrame 'df' con las columnas renombradas y la nueva columna 'year' que contiene solo el año de publicación.
