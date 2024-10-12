import csv
import time
import re  # Importar la librería de expresiones regulares
import sys  # Para aumentar el límite de recursión
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from MetodosDeOrdenamiento import MetodosDeOrdenamiento

# Aumentar el límite de recursión
sys.setrecursionlimit(10000)  # Puedes ajustar este número según sea necesario

# Ruta al archivo CSV
ruta_csv = './data/bases_datos/data_unido.csv'

# Instancia de la clase MetodosDeOrdenamiento
metodos = MetodosDeOrdenamiento()

# Lista de métodos de ordenamiento para texto y números
metodos_texto = [
    metodos.tim_sort,
    metodos.comb_sort,
    metodos.selection_sort,
    metodos.quick_sort,
    metodos.heap_sort,
    metodos.bitonic_sort,
    metodos.gnome_sort,
    metodos.binary_insertion_sort
]

metodos_numericos = [
    metodos.tim_sort,
    metodos.comb_sort,
    metodos.selection_sort,
    metodos.quick_sort,
    metodos.heap_sort,
    metodos.bitonic_sort,
    metodos.gnome_sort,
    metodos.binary_insertion_sort,
    metodos.pigeonhole_sort,
    metodos.bucket_sort,
    metodos.radix_sort,
    metodos.tree_sort
]

# Columnas que deben ser convertidas a enteros
columnas_numericas = ['ISSN', 'Publication Date', 'Volume', 'Issue', 'First Page', 'Year']

# Función para extraer números de cadenas que tienen letras y números combinados
def extraer_numero(valor):
    match = re.search(r'\d+', valor)  # Buscar un número dentro de la cadena
    if match:
        return int(match.group())  # Retorna el número encontrado como entero
    return None  # Si no se encuentra número, retornar None

# Función para analizar la columna seleccionada
def analizar_columna(columna_elegida, columna_nombre, archivo):
    resultados = []

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
            if valor_celda == 'N.PAG':
                continue
            numero_extraido = extraer_numero(valor_celda)
            if numero_extraido is not None:
                array_column.append(numero_extraido)
            else:
                continue

        else:
            array_column.append(valor_celda)

    # Filtrar solo valores numéricos en columnas numéricas
    if columna_nombre in columnas_numericas:
        array_column = [x for x in array_column if isinstance(x, int)]
        metodos_ordenamiento = metodos_numericos
    else:
        metodos_ordenamiento = metodos_texto

    # Aplicar cada método de ordenamiento y medir el tiempo
    for metodo_ordenamiento in metodos_ordenamiento:
        inicio_tiempo = time.time()
        array_ordenado = metodo_ordenamiento(array_column[:])  # Crear una copia para cada ordenamiento
        fin_tiempo = time.time()
        tiempo_total = fin_tiempo - inicio_tiempo
        resultados.append((columna_nombre, metodo_ordenamiento.__name__, len(array_column), tiempo_total))

    return resultados

# Función para mostrar gráficos en Tkinter
def mostrar_graficos(resultados, columna_nombre):
    ventana = tk.Tk()
    ventana.title(f"Resultados de Ordenamiento - Columna: {columna_nombre}")
    ventana.geometry('800x600')

    # Crear un frame para el gráfico y la tabla
    frame_grafico = tk.Frame(ventana)
    frame_grafico.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    frame_tabla = tk.Frame(ventana)
    frame_tabla.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    # Crear el gráfico de barras
    fig, ax = plt.subplots(figsize=(10, 6))

    metodos = [r[1] for r in resultados]
    tiempos = [r[3] for r in resultados]

    # Cambiar color de las barras
    colores = ['#FF5733', '#33FF57', '#3357FF', '#FF33A6', '#FF5733', '#33FFB5', '#FF8C33']
    colores = colores[:len(metodos)]  # Ajustar la lista de colores si hay más métodos que colores

    ax.bar(metodos, tiempos, color=colores)
    ax.set_title(f'Tiempo de Ejecución por Método de Ordenamiento - Columna: {columna_nombre}')
    ax.set_ylabel('Tiempo (segundos)')
    ax.set_xlabel('Métodos')

    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Crear la tabla con Treeview
    columnas = ("columna", "metodo", "elementos", "tiempo")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show='headings')

    # Definir los encabezados
    tabla.heading("columna", text="Columna evaluada")
    tabla.heading("metodo", text="Método utilizado")
    tabla.heading("elementos", text="Número de elementos")
    tabla.heading("tiempo", text="Tiempo de ejecución (segundos)")

    # Definir el tamaño de las columnas
    tabla.column("columna", width=150, anchor=tk.CENTER)
    tabla.column("metodo", width=200, anchor=tk.CENTER)
    tabla.column("elementos", width=150, anchor=tk.CENTER)
    tabla.column("tiempo", width=200, anchor=tk.CENTER)

    # Insertar los resultados en la tabla
    for resultado in resultados:
        tabla.insert("", "end", values=resultado)

    tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Agregar scrollbar
    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    ventana.mainloop()

# Función principal
with open(ruta_csv, mode='r', newline='', encoding='utf-8-sig') as archivo:
        lector_csv = csv.DictReader(archivo)

        # Guardar los nombres de las columnas
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

            # Analizar la columna y obtener los resultados
            resultados = analizar_columna(columna_elegida, columna_nombre, archivo)

            # Mostrar gráficos con los resultados
            mostrar_graficos(resultados, columna_nombre)

        else:
            print("Número de columna inválido.")