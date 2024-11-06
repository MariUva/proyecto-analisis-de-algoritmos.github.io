import pandas as pd

def descriptive_statistics(df, column1):
    """
    Realiza un análisis unidimensional en una columna de un DataFrame,
    incluyendo los valores repetidos y su frecuencia.
    
    :param df: DataFrame que contiene los datos a analizar.
    :param column1: str, nombre de la columna para análisis unidimensional.
    :return: dict con estadísticas descriptivas y valores repetidos.
    """
    
    # Asegura que la columna existe en el DataFrame
    if column1 in df.columns:
        # Filas contadas (total de filas no nulas)
        conteo = df[column1].count()

        # Valores únicos
        valores_unicos = df[column1].nunique()

        # Valores repetidos (total - únicos)
        valores_repetidos = conteo - valores_unicos

        # Encuentra los valores repetidos y sus frecuencias
        valores_repetidos_lista = df[column1].value_counts()
        valores_repetidos_lista = valores_repetidos_lista[valores_repetidos_lista > 1].to_dict()

        # Diccionario para devolver los resultados en español
        resultado = {
            'conteo': conteo,
            'valores únicos': valores_unicos,
            'valores repetidos': valores_repetidos,
        }

        return resultado
    else:
        raise ValueError(f"La columna especificada '{column1}' no existe en el DataFrame.")
