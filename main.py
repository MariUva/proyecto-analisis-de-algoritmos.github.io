from src.data.data_processing import load_data
from src.statistics.statistics import descriptive_statistics

def main():
    # Especificar la ruta de tu archivo CSV
    file_path = 'data/APPLIED AND ENGINEERING.csv'
    
    # Cargar los datos
    df = load_data(file_path)
    
    # Mostrar opciones al usuario
    print("Seleccione el tipo de análisis:")
    print("1. Análisis Unidimensional (una variable)")
    print("2. Análisis Bidimensional (dos variables)")

    choice = input("Ingrese su opción (1 o 2): ")
    
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

    else:
        print("Opción no válida. Por favor, seleccione 1 o 2.")

if __name__ == "__main__":
    main()
