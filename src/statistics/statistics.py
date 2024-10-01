import pandas as pd  # Importa la librería pandas, que es útil para el manejo y análisis de datos estructurados.

def descriptive_statistics(df, column1, column2=None):  # Define una función llamada 'descriptive_statistics' que toma dos argumentos: 'df' (el DataFrame) y 'column1' (una columna). 'column2' es opcional.
    
    if column2:  # Verifica si se proporciona una segunda columna (para análisis bidimensional).
        # Análisis bidimensional
        return df.groupby([column1, column2]).size().reset_index(name='counts')  
        # Agrupa los datos por las dos columnas ('column1' y 'column2'), cuenta cuántos registros hay en cada combinación de valores y devuelve el resultado en un DataFrame. 
        # La columna de conteo se llama 'counts'.

    else:  # Si no se proporciona una segunda columna, realiza un análisis unidimensional.
        # Análisis unidimensional
        stats = df[column1].describe()  
        # Calcula las estadísticas descriptivas de la columna 'column1' usando el método 'describe()' de pandas. Devuelve un resumen con valores como conteo, únicos, media, etc.

        # Traducir las etiquetas de las estadísticas al español
        traduccion = {  # Crea un diccionario que mapea las etiquetas de las estadísticas originales en inglés a sus equivalentes en español.
            'count': 'conteo',  # Traduce 'count' como 'conteo'.
            'unique': 'valores únicos',  # Traduce 'unique' como 'valores únicos'.
            'top': 'más frecuente',  # Traduce 'top' como 'más frecuente' (el valor más común).
            'freq': 'frecuencia',  # Traduce 'freq' como 'frecuencia' (la cantidad de veces que aparece el valor más común).
            'mean': 'media',  # Traduce 'mean' como 'media' (el promedio).
            'std': 'desviación estándar',  # Traduce 'std' como 'desviación estándar' (medida de dispersión).
            'min': 'mínimo',  # Traduce 'min' como 'mínimo' (el valor más bajo).
            '25%': '25%',  # Mantiene '25%' sin cambios, representando el primer cuartil.
            '50%': 'mediana',  # Traduce '50%' como 'mediana' (el valor central).
            '75%': '75%',  # Mantiene '75%' sin cambios, representando el tercer cuartil.
            'max': 'máximo'  # Traduce 'max' como 'máximo' (el valor más alto).
        }
        
        # Renombrar las etiquetas
        stats = stats.rename(index=traduccion)  
        # Renombra las etiquetas estadísticas en el resumen utilizando el diccionario de traducción creado anteriormente.

        return stats  # Devuelve las estadísticas descriptivas con las etiquetas traducidas.
