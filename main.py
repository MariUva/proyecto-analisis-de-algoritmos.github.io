import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from src.data.data_processing import load_data
from src.statistics.statistics import descriptive_statistics
from src.statistics.conteoFrecuencia import analizar_abstracts

def centrar_ventana(ventana, ancho, alto):
    # Obtener el ancho y alto de la pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    
    # Calcular las coordenadas x e y para centrar la ventana
    x = (ancho_pantalla // 2) - (ancho // 2)
    y = (alto_pantalla // 2) - (alto // 2)
    
    # Asignar la geometría centrada
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def realizar_analisis(tipo_analisis, df):
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
        analizar_abstracts('data/APPLIED AND ENGINEERING.csv')
        messagebox.showinfo("Análisis de Abstracts", "Análisis de abstracts completado.")

def main():
    # Cargar los datos
    file_path = 'data/APPLIED AND ENGINEERING.csv'
    df = load_data(file_path)

    # Crear la ventana principal
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
    options = ["Análisis Unidimensional", "Análisis Bidimensional", "Análisis de Abstracts"]
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

if __name__ == "__main__":
    main()
