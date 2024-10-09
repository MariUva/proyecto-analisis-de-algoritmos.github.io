import csv
import time
import re  # Importar la librería de expresiones regulares
from MetodosDeOrdenamiento import MetodosDeOrdenamiento

# Ruta del archivo CSV
ruta_csv = './data/bases_datos/data_unido.csv'

# Instancia de la clase MetodosDeOrdenamiento
metodos = MetodosDeOrdenamiento()

# Lista de métodos de ordenamiento
metodos_disponibles = [
    metodos.tim_sort,
    metodos.comb_sort,
    metodos.selection_sort,
    metodos.tree_sort,
    metodos.pigeonhole_sort,
    metodos.bucket_sort,
    metodos.quick_sort,
    metodos.heap_sort,
    metodos.bitonic_sort,
    metodos.gnome_sort,
    metodos.binary_insertion_sort,
    metodos.radix_sort  # Asegúrate de incluir radix_sort
]

# Columnas que deben ser convertidas a enteros
columnas_numericas = ['ISSN', 'Publication Date', 'Volume', 'Issue', 'First Page']

# Función para extraer números de cadenas que tienen letras y números combinados
def extraer_numero(valor):
    match = re.search(r'\d+', valor)  # Buscar un número dentro de la cadena
    if match:
        return int(match.group())  # Retorna el número encontrado como entero
    return None  # Si no se encuentra número, retornar None

# Abrir y leer el archivo CSV
with open(ruta_csv, mode='r', newline='', encoding='utf-8-sig') as archivo:
    lector_csv = csv.DictReader(archivo)

    # Guardar los nombres de las columnas sin el BOM
    columnas = [nombre_col.strip() for nombre_col in lector_csv.fieldnames]

    # Mostrar columnas disponibles
    print("Columnas disponibles:")
    for i, columna in enumerate(columnas):
        print(f"{i + 1}. {columna}")

    # Solicitar al usuario que elija una columna por número
    columna_elegida = int(input("Elige el número de la columna que deseas ver: ")) - 1

    # Validar la elección de la columna
    if 0 <= columna_elegida < len(columnas):
        columna_nombre = columnas[columna_elegida]
        print(f"\nHas elegido la columna: {columna_nombre}\n")

        # Reiniciar el puntero del archivo CSV y volver a inicializar el lector
        archivo.seek(0)
        lector_csv = csv.DictReader(archivo)

        # Guardar los valores de la columna en un array
        array_column = []

        for fila in lector_csv:
            valor_celda = fila[columna_nombre].strip() if fila[columna_nombre] else 'N/A'

            # Si es la columna 'Author', tomar solo el primer autor
            if columna_nombre == 'Author' and valor_celda != 'N/A':
                primer_autor = valor_celda.split(',')[0].strip()
                array_column.append(primer_autor)

            # Si es una columna numérica, convertir el valor a entero
            elif columna_nombre in columnas_numericas and valor_celda != 'N/A':
                # Omitir valores como "N.PAG"
                if valor_celda == 'N.PAG':
                    continue

                # Intentar extraer números de valores como "S30"
                numero_extraido = extraer_numero(valor_celda)
                if numero_extraido is not None:
                    array_column.append(numero_extraido)
                else:
                    # Omitir las filas que no tengan números válidos
                    continue

            else:
                array_column.append(valor_celda)

        # Filtrar solo valores numéricos en columnas numéricas
        if columna_nombre in columnas_numericas:
            array_column = [x for x in array_column if isinstance(x, int)]

        # Imprimir el tamaño del arreglo filtrado siempre
        print(f"\nTamaño del arreglo filtrado: {len(array_column)}")

        # Mostrar los nombres de los métodos disponibles
        print("\nMétodos de ordenamiento disponibles:")
        for num, metodo in enumerate(metodos_disponibles, 1):
            print(f"{num}. {metodo.__name__}")

        # Solicitar al usuario que elija un método de ordenamiento
        metodo_elegido = int(input("Elige el número del método de ordenamiento que deseas aplicar: ")) - 1

        # Validar la elección del método de ordenamiento
        if 0 <= metodo_elegido < len(metodos_disponibles):
            metodo_ordenamiento = metodos_disponibles[metodo_elegido]

            print(f"\nAplicando {metodo_ordenamiento.__name__} a los datos de la columna {columna_nombre}...\n")

            # Aplicar el método de ordenamiento elegido
            inicio_tiempo = time.time()
            array_ordenado = metodo_ordenamiento(array_column)
            fin_tiempo = time.time()

            # Mostrar el array ordenado
            print("Datos ordenados:")
            for valor in array_ordenado:
                print(valor)

            # Mostrar el tiempo que tardó en ordenar
            tiempo_total = fin_tiempo - inicio_tiempo
            print(f"\nTiempo total con {metodo_ordenamiento.__name__}: {tiempo_total:.30f} segundos")
            print(f"Tamaño final del arreglo: {len(array_ordenado)}")  # Tamaño del array ordenado
        else:
            print("Número de método de ordenamiento inválido.")
    else:
        print("Número de columna inválido.")