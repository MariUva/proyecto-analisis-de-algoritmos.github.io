from flask import Flask, render_template, request, send_file
import os
from dotenv import load_dotenv
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from io import BytesIO
from src.statistics.conteoFrecuencia import analizar_abstracts, generar_nube_palabras, ruta_csv
from src.data.data_processing import load_data  
import networkx as nx
from src.statistics.statistics import descriptive_statistics
from src.union_csv.union_csv import limpiar_columnas_csv, unificar_data, eliminar_duplicados

# Carga las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)


# Configuraciones de rutas
directory_path_csv = os.getenv("DIRECTORY_CSV")
nombre_documento_unido = os.getenv("NAME_DATA")
file_path = os.path.join(directory_path_csv, nombre_documento_unido)

def verificar_existencia_data(directory_path_csv, nombre_documento_unido):
    """Verifica si el archivo unificado ya existe en la ruta especificada."""
    ruta_completa = os.path.join(directory_path_csv, nombre_documento_unido)
    return os.path.isfile(ruta_completa)

def cargar_y_preparar_datos():
    """Carga y prepara los datos; limpia y une si es necesario."""
    if not verificar_existencia_data(directory_path_csv, nombre_documento_unido):
        print("Unificando datos...")
        limpiar_columnas_csv(directory_path_csv)
        unificar_data(directory_path_csv, nombre_documento_unido)
        eliminar_duplicados(directory_path_csv, nombre_documento_unido)
    else:
        print("Los datos ya se encuentran unidos.")
    
    # Cargar los datos en un DataFrame
    return load_data(file_path)

# Cargar los datos al inicio de la aplicación
df = cargar_y_preparar_datos()
conteo_total = analizar_abstracts(file_path) 

@app.route('/')

def index():
    # Página principal con opciones de análisis
    return render_template('index.html')

@app.route('/analisis_unidimensional', methods=['GET', 'POST'])
def analisis_unidimensional():
    if request.method == 'POST':
        columna = request.form['columna']
        df = load_data(ruta_csv)
        if columna in df.columns:
            resultado = descriptive_statistics(df, columna)
            return render_template('resultado.html', resultado=resultado, tipo=f"Análisis Unidimensional para {columna}")
        else:
            return "Error: La columna especificada no existe en el archivo.", 400
    return render_template('unidimensional.html')


@app.route('/totales')
def graficar_totales():

    # Verifica que `conteo_total` tenga contenido
    if not conteo_total:
        return "Error: No se pudo obtener el conteo total.", 500

    categorias = list(conteo_total.keys())
    total_por_categoria = [sum(conteo.values()) for conteo in conteo_total.values()]

    # Configurar el gráfico de totales
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(categorias, total_por_categoria, color='lightgreen')
    ax.set_title("Totales por Categoría")
    ax.set_xlabel("Categorías")
    ax.set_ylabel("Total Frecuencia")
    ax.tick_params(axis='x', rotation=90, labelsize=8)

    # Agregar conteo en cada barra
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom')

    # Guardar el gráfico en un objeto BytesIO en formato PNG
    img = BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)
    return send_file(img, mimetype='image/png')

@app.route('/ver_graficos_categorias')
def ver_graficos_categorias():
    # Pasar `conteo_total` a la plantilla para mostrar todos los gráficos de categoría
    return render_template('resultadoGraficos.html', conteo_total=conteo_total)

@app.route('/grafico_categoria/<categoria>')
def grafico_categoria(categoria):
    conteo = conteo_total.get(categoria, {})

    if not conteo:
        return "No se encontró la categoría solicitada", 404

    # Generar un gráfico individual para la categoría especificada
    img = generar_grafico(categoria, conteo)
    return send_file(img, mimetype='image/png')

def generar_grafico(categoria, conteo):
    variables = list(conteo.keys())
    frecuencias = list(conteo.values())

    # Configurar el gráfico para la categoría específica
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(variables, frecuencias, color='skyblue')
    ax.set_title(f'Frecuencia de Aparición - {categoria}')
    ax.set_xlabel('Variables')
    ax.set_ylabel('Frecuencia')
    ax.tick_params(axis='x', rotation=90, labelsize=8)

    # Agregar conteo en cada barra
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom')


    # Guardar el gráfico en un objeto BytesIO en formato PNG
    img = BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)
    return img

@app.route('/nube_palabras')
def mostrar_nube_palabras():

    if not os.path.isfile(ruta_csv):
        return "Error: La ruta del archivo CSV no está definida o no es válida.", 500

    print("Archivo CSV encontrado. Analizando abstracts...")

    # Obtiene conteo_total usando analizar_abstracts
    conteo_total = analizar_abstracts(ruta_csv)
    print("Conteo de frecuencia calculado.")

    img = generar_nube_palabras(conteo_total)  # Pasa conteo_total, no ruta_csv
    print("Nube de palabras generada.")

    return send_file(img, mimetype='image/png')


@app.route('/analisis_abstracts')
def analisis_abstracts():
    if not os.path.isfile(ruta_csv):
        return "Error: La ruta del archivo CSV no está definida o no es válida.", 500

    conteo_total = analizar_abstracts(ruta_csv)
    # Llama a una función para mostrar resultados de abstracts
    
    return render_template('resultado.html', resultado=conteo_total, tipo="Análisis de Abstracts")

@app.route('/analisis_issn')
def graficar_nodos_aristas_route():
    # Verificar que el archivo CSV existe
    if not os.path.isfile(ruta_csv):
        return "Error: La ruta del archivo CSV no está definida o no es válida.", 500

    # Cargar los datos y obtener los ISSN más frecuentes
    df = load_data(ruta_csv)
    valores_mas_frecuentes = df.iloc[:, 2].value_counts().head(10)  # Usar columna 2 como ISSN
    img = graficar_nodos_aristas(valores_mas_frecuentes, df)
    return send_file(img, mimetype='image/png')

def graficar_nodos_aristas(valores_mas_frecuentes, df):
    """
    Genera un gráfico de nodos y aristas basado en los valores más frecuentes de ISSN,
    mostrando relaciones con el país y el total de citas.
    """
    G = nx.Graph()
    node_colors = []

    # Iterar sobre los ISSN más frecuentes
    for issn in valores_mas_frecuentes.index:
        frecuencia = valores_mas_frecuentes[issn]
        datos_filtrados = df[df.iloc[:, 2] == issn]  # Filtrar datos donde columna 2 (ISSN) coincide

        # Sumar citas y obtener el país más frecuente
        total_citas = datos_filtrados.iloc[:, 11].sum()  # Columna de citas
        pais_frecuente = datos_filtrados.iloc[:, 10].mode()[0]  # Columna de país más frecuente

        # Añadir nodo para el ISSN y su color
        if issn not in G:
            G.add_node(issn, label=issn)
            node_colors.append("lightblue")

        # Añadir nodo para el país frecuente y la arista
        if pais_frecuente not in G:
            G.add_node(pais_frecuente, label=pais_frecuente)
            node_colors.append("lightgreen")
        G.add_edge(issn, pais_frecuente, label="País")

        # Añadir nodo para las citas totales y la arista
        cita_label = f"{total_citas} citas"
        if cita_label not in G:
            G.add_node(cita_label, label=cita_label)
            node_colors.append("lightcoral")
        G.add_edge(issn, cita_label, label="Citas")

    # Configuración de disposición y visualización del gráfico
    pos = nx.spring_layout(G, seed=42, k=0.5)
    fig, ax = plt.subplots(figsize=(12, 10))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color=node_colors,
            font_size=10, font_weight="bold", edge_color="gray", ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['label'] for u, v, d in G.edges(data=True)}, font_size=8)
    plt.title("Gráfico de Nodos y Aristas: ISSN, País y Citas")

    # Guardar la imagen en un objeto BytesIO y devolverla
    img = BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)
    return img


if __name__ == '__main__':
    app.run(debug=True)
