from src.data.data_processing import load_data  # Importa la función 'load_data' desde el módulo 'data_processing', que se utiliza para cargar el archivo CSV.
from src.statistics.statistics import descriptive_statistics  # Importa la función 'descriptive_statistics' desde el módulo 'statistics', que se utiliza para generar estadísticas descriptivas.
from src.statistics.conteoFrecuencia import analizar_abstracts  # Importa la función 'analizar_abstracts' desde el módulo 'conteoFrecuencia', utilizada para analizar abstracts en el CSV.

def main():  # Define la función principal 'main' que manejará la lógica del programa.
    
    # Especificar la ruta de tu archivo CSV
    file_path = 'data/APPLIED AND ENGINEERING.csv'  # Especifica la ruta donde se encuentra el archivo CSV que se va a analizar.
    
    # Cargar los datos
    df = load_data(file_path)  # Llama a la función 'load_data' para cargar el archivo CSV en un DataFrame de pandas.
    
    # Mostrar opciones al usuario
    print("Seleccione el tipo de análisis:")  # Imprime el mensaje solicitando al usuario seleccionar un tipo de análisis.
    print("1. Análisis Unidimensional (una variable)")  # Opción 1: Análisis unidimensional de una variable.
    print("2. Análisis Bidimensional (dos variables)")  # Opción 2: Análisis bidimensional de dos variables.
    print("3. Análisis de aparición de variables en Abstracts")  # Opción 3: Análisis de abstracts (resúmenes).

    choice = input("Ingrese su opción (1, 2 o 3): ")  # Solicita al usuario que ingrese su elección de análisis y guarda la entrada en la variable 'choice'.
    
    if choice == "1":  # Si el usuario elige la opción 1 (análisis unidimensional):
        # Pedir la columna para el análisis unidimensional
        column = input("Ingrese el nombre de la columna para el análisis unidimensional: ")  # Solicita al usuario el nombre de la columna que desea analizar.
        result = descriptive_statistics(df, column)  # Llama a la función 'descriptive_statistics' para calcular estadísticas de la columna seleccionada.
        print(f"\nEstadísticas descriptivas para {column}:")  # Imprime el nombre de la columna analizada.
        print(result)  # Muestra las estadísticas descriptivas generadas.

    elif choice == "2":  # Si el usuario elige la opción 2 (análisis bidimensional):
        # Pedir las dos columnas para el análisis bidimensional
        column1 = input("Ingrese el nombre de la primera columna: ")  # Solicita al usuario el nombre de la primera columna.
        column2 = input("Ingrese el nombre de la segunda columna: ")  # Solicita al usuario el nombre de la segunda columna.
        result = descriptive_statistics(df, column1, column2)  # Llama a la función 'descriptive_statistics' con dos columnas para generar estadísticas bidimensionales.
        print(f"\nEstadísticas descriptivas para {column1} y {column2}:")  # Imprime los nombres de las columnas analizadas.
        print(result)  # Muestra las estadísticas descriptivas generadas para las dos columnas.

    elif choice == "3":  # Si el usuario elige la opción 3 (análisis de abstracts):
        # Llamar al análisis de abstracts usando la función existente
        analizar_abstracts(file_path)  # Llama a la función 'analizar_abstracts' para realizar el análisis de los abstracts en el archivo CSV.

    else:  # Si el usuario ingresa una opción inválida (distinta de 1, 2 o 3):
        print("Opción no válida. Por favor, seleccione 1, 2 o 3.")  # Imprime un mensaje de error indicando que la opción no es válida.

if __name__ == "__main__":  # Comprueba si el script se está ejecutando como el programa principal.
    main()  # Llama a la función 'main' para iniciar el programa.
