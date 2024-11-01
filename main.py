from src.data.data_processing import load_data  # Para cargar el archivo CSV.
from src.statistics.statistics import descriptive_statistics  # Para generar estadísticas descriptivas.
from src.statistics.conteoFrecuencia import analizar_abstracts, crear_ventana_con_pestanas  # Para analizar abstracts en el CSV.
from src.union_csv.union_csv import limpiar_columnas_csv, unificar_data  # Para limpiar columnas y unificar CSVs.
#from dotenv import load_dotenv  # Para cargar las variables de entorno.
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import time
from dotenv import load_dotenv
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import networkx as nx


# Carga las variables de entorno desde el archivo .env
load_dotenv()

def centrar_ventana(ventana, ancho, alto):
    # Centra la ventana en la pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    x = (ancho_pantalla // 2) - (ancho // 2)
    y = (alto_pantalla // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def realizar_analisis(tipo_analisis, df):
    # Función para realizar los análisis basados en la selección del usuario
    if tipo_analisis == "Análisis Unidimensional":
        ventana_unidimensional = tk.Toplevel()
        ventana_unidimensional.title("Análisis Unidimensional")
        centrar_ventana(ventana_unidimensional, 300, 150)

        label = ttk.Label(ventana_unidimensional, text="Ingrese el nombre de la columna:")
        label.pack(pady=10)

        columna_entry = ttk.Entry(ventana_unidimensional)
        columna_entry.pack(pady=10)

        def procesar_unidimensional():
            column = columna_entry.get()
            if column:
                result = descriptive_statistics(df, column)
                messagebox.showinfo(f"Estadísticas descriptivas para {column}", str(result))
                ventana_unidimensional.destroy()
            else:
                messagebox.showerror("Error", "Debe ingresar una columna válida.")

        button = ttk.Button(ventana_unidimensional, text="Procesar", command=procesar_unidimensional)
        button.pack(pady=10)

    elif tipo_analisis == "Análisis Bidimensional":
        ventana_bidimensional = tk.Toplevel()
        ventana_bidimensional.title("Análisis Bidimensional")
        centrar_ventana(ventana_bidimensional, 300, 200)

        label1 = ttk.Label(ventana_bidimensional, text="Ingrese el nombre de la primera columna:")
        label1.pack(pady=10)

        columna1_entry = ttk.Entry(ventana_bidimensional)
        columna1_entry.pack(pady=10)

        label2 = ttk.Label(ventana_bidimensional, text="Ingrese el nombre de la segunda columna:")
        label2.pack(pady=10)

        columna2_entry = ttk.Entry(ventana_bidimensional)
        columna2_entry.pack(pady=10)

        def procesar_bidimensional():
            column1 = columna1_entry.get()
            column2 = columna2_entry.get()
            if column1 and column2:
                result = descriptive_statistics(df, column1, column2)
                messagebox.showinfo(f"Estadísticas descriptivas para {column1} y {column2}", str(result))
                ventana_bidimensional.destroy()
            else:
                messagebox.showerror("Error", "Debe ingresar ambas columnas.")

        button = ttk.Button(ventana_bidimensional, text="Procesar", command=procesar_bidimensional)
        button.pack(pady=10)

 
    elif tipo_analisis == "Análisis de Abstracts":

       #conteo_total = analizar_abstracts('data/APPLIED AND ENGINEERING.csv')  # Llama a la función para obtener el conteo

       conteo_total = analizar_abstracts('data/bases_datos/data_unido.csv')  # Llama a la función para obtener el conteo
       crear_ventana_con_pestanas(conteo_total)  # Muestra la ventana con los gráficos
        

    elif tipo_analisis == "Nube de Palabras Abstract":
        generar_nube_palabras(df) 
    
    
    elif tipo_analisis == "Analisis de ISSN":
        # Ejecutar la función de gráfico de nodos y aristas para ISSN
        valores_mas_frecuentes = df.iloc[:, 4].value_counts().head(10)
        graficar_nodos_aristas(valores_mas_frecuentes, df)
        messagebox.showinfo("Análisis de ISSN", "El análisis de ISSN se ha completado y el gráfico se ha generado.")



def generar_nube_palabras(df):
    abstracts = " ".join(df['abstract'].dropna())  # Suponiendo que la columna de abstracts se llama 'abstract'
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(abstracts)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()     #analizar_abstracts('data/APPLIED AND ENGINEERING.csv')
        #messagebox.showinfo("Análisis de Abstracts", "Análisis de abstracts completado.")

def unir_data(nombre_archivo, directory_path_csv):
    # Función que unifica la data de varios CSV en uno solo
    limpiar_columnas_csv(directory_path_csv)
    unificar_data(directory_path_csv, nombre_archivo)
    time.sleep(3)  # Simulación del proceso de unificación


def graficar_nodos_aristas(valores_mas_frecuentes, df):
    # Crear un gráfico de nodos y aristas
    G = nx.Graph()
    node_colors = []  # Lista para almacenar los colores de los nodos

    for valor in valores_mas_frecuentes.index:
        frecuencia = valores_mas_frecuentes[valor]
        datos_filtrados = df[df.iloc[:, 4] == valor]
        total_citas = datos_filtrados.iloc[:, 11].sum()
        pais_frecuente = datos_filtrados.iloc[:, 10].mode()[0]

        # Nodo ISSN (Azul claro) - solo añadir si no existe ya en el grafo
        if valor not in G:
            G.add_node(valor, label=valor)
            node_colors.append("lightblue")

        # Nodo país (Verde claro) - solo añadir si no existe ya en el grafo
        if pais_frecuente not in G:
            G.add_node(pais_frecuente, label=pais_frecuente)
            node_colors.append("lightgreen")
        G.add_edge(valor, pais_frecuente, label="País")

        # Nodo citas (Rojo claro) - solo añadir si no existe ya en el grafo
        cita_label = f"{total_citas} citas"
        if cita_label not in G:
            G.add_node(cita_label, label=cita_label)
            node_colors.append("lightcoral")
        G.add_edge(valor, cita_label, label="Citas")

    # Aumentar espacio entre nodos usando k en spring_layout
    pos = nx.spring_layout(G, seed=42, k=0.5)  # Ajustar k para mayor separación

    # Dibujar el gráfico
    plt.figure(figsize=(12, 10))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color=node_colors,
            font_size=10, font_weight="bold", edge_color="gray")
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['label'] for u, v, d in G.edges(data=True)}, font_size=8)
    plt.title("Gráfico de Nodos y Aristas: Valores Frecuentes, País y Citas")
    plt.show()



def main():


    # Cargar los datos desde el archivo CSV
    directory_path_csv = os.getenv('DIRECTORY_CSV')  # Ruta de los CSV desde el .env
    nombre_documento_unido = os.getenv('NAME_DATA')  # Nombre del archivo unido desde el .env

    file_path = os.getenv('FILE_PATCH')  # Ruta del archivo para análisis desde el .env

    existeArchivo = verificar_existencia_data(directory_path_csv,nombre_documento_unido) #Llamada al metodo para verificar si se encuentra el archivo con la data unida

    if existeArchivo:
        print("Los datos ya se encuentra unidos\n")
    else:
        unir_data(nombre_documento_unido,directory_path_csv)#LLamado al metodo para unir toda la data en una sola
    


    # Unir data si es necesario 
    # unir_data(nombre_documento_unido, directory_path_csv)

    # Cargar los datos
    df = load_data(file_path)
    
     # Imprimir el contenido de la columna en la posición 4
    print("Contenido de la columna 4:")
    print(df.iloc[:, 4])

   # Encontrar los 10 valores más frecuentes en la columna 4
    valores_mas_frecuentes = df.iloc[:, 4].value_counts().head(10)
    print("Los 10 valores más frecuentes en la columna 4, con sus repeticiones, citas y país correspondiente:")

    # Recorrer los valores más frecuentes y extraer la información de citas y país correspondiente
    for valor in valores_mas_frecuentes.index:
        frecuencia = valores_mas_frecuentes[valor]
        
        # Filtrar el DataFrame para obtener las filas que corresponden a cada valor frecuente
        datos_filtrados = df[df.iloc[:, 4] == valor]

        # Obtener la suma de citas para este valor (columna 11)
        total_citas = datos_filtrados.iloc[:, 11].sum()

        # Obtener el país más frecuente para este valor (columna 10)
        pais_frecuente = datos_filtrados.iloc[:, 10].mode()[0]

        print(f"{valor}: {frecuencia} veces, Citas: {total_citas}, País: {pais_frecuente}")


    # Crear la ventana principal con Tkinter
    root = tk.Tk()
    root.title("Análisis de Datos")

    # Configurar el tamaño de la ventana y centrarla
    ancho_ventana = 400
    alto_ventana = 200
    centrar_ventana(root, ancho_ventana, alto_ventana)

    # Etiqueta principal
    label = ttk.Label(root, text="Seleccione el tipo de análisis:")
    label.pack(pady=10)

    # Crear el combobox para seleccionar el tipo de análisis
    options = ["Análisis Unidimensional", "Análisis Bidimensional", "Análisis de Abstracts", "Analisis de ISSN"]
    combo = ttk.Combobox(root, values=options)
    combo.set("Seleccione un análisis")
    combo.pack(pady=10)


    # Crear el botón para iniciar el análisis
    def iniciar_analisis():
        seleccion = combo.get()
        if seleccion in options:
            realizar_analisis(seleccion, df)
        else:
            messagebox.showerror("Error", "Seleccione una opción válida")

    button = ttk.Button(root, text="Iniciar Análisis", command=iniciar_analisis)
    button.pack(pady=10)

    # Ejecutar el bucle principal de tkinter
    root.mainloop()


def verificar_existencia_data(directory_path_csv,nombre_documento_unido):
    # Combina la ruta de la carpeta con el nombre del archivo
    ruta_completa = os.path.join(directory_path_csv, nombre_documento_unido)

    # Verifica si el archivo existe y devuelve el boleano con el resultado
    return os.path.isfile(ruta_completa)

if __name__ == "__main__":
    main()
