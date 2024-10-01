from src.data.data_processing import load_data
from src.statistics.statistics import descriptive_statistics
from src.statistics.conteoFrecuencia import analizar_abstracts  # Importar la función

def main():
    # Especificar la ruta de tu archivo CSV
    file_path = 'data/APPLIED AND ENGINEERING.csv'
    
    # Cargar los datos
    df = load_data(file_path)
    
    # Mostrar opciones al usuario
    print("Seleccione el tipo de análisis:")
    print("1. Análisis Unidimensional (una variable)")
    print("2. Análisis Bidimensional (dos variables)")
    print("3. Análisis de Abstracts")

    choice = input("Ingrese su opción (1, 2 o 3): ")
    
    if choice == "1":
        # Pedir la columna para el análisis unidimensional
        column = input("Ingrese el nombre de la columna para el análisis unidimensional: ")
        result = descriptive_statistics(df, column)
        print(f"\nEstadísticas descriptivas para {column}:")
        print(result)

    elif choice == "2":
        # Pedir las dos columnas para el análisis bidimensional
        column1 = input("Ingrese el nombre de la primera columna: ")
        column2 = input("Ingrese el nombre de la segunda columna: ")
        result = descriptive_statistics(df, column1, column2)
        print(f"\nEstadísticas descriptivas para {column1} y {column2}:")
        print(result)

    elif choice == "3":
        # Llamar al análisis de abstracts usando la función existente
        analizar_abstracts(file_path)

    else:
        print("Opción no válida. Por favor, seleccione 1, 2 o 3.")

if __name__ == "__main__":
    main()
