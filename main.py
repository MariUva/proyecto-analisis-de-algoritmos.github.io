from flask import Flask, render_template, request, send_file
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from io import BytesIO
from src.statistics.conteoFrecuencia import analizar_abstracts, generar_nube_palabras, ruta_csv
from src.data.data_processing import load_data  # Asegúrate de tener esta importación
import networkx as nx



# Carga las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Definir ruta_csv a nivel de `main.py`
ruta_csv = os.getenv("RUTA_CSV", "./data/bases_datos/data_unido.csv")

@app.route('/')

def index():
    # Página principal con opciones de análisis
    return render_template('index.html')

@app.route('/totales')
def graficar_totales():
    # Asegúrate de que `ruta_csv` esté definida o cargada correctamente
    if not ruta_csv:
        return "Error: La ruta del archivo CSV no está definida.", 500

    conteo_total = analizar_abstracts(ruta_csv)
    categorias = list(conteo_total.keys())
    total_por_categoria = [sum(conteo.values()) for conteo in conteo_total.values()]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(categorias, total_por_categoria, color='lightgreen')
    ax.set_title("Totales por Categoría")
    ax.set_xlabel("Categorías")
    ax.set_ylabel("Total Frecuencia")
    ax.tick_params(axis='x', rotation=45, labelsize=8)

    img = BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)
    return send_file(img, mimetype='image/png')

@app.route('/nube_palabras')
def mostrar_nube_palabras():
      # Verifica si ruta_csv está definida y es válida
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
    # Asegúrate de que `ruta_csv` esté definida o cargada correctamente
    if not os.path.isfile(ruta_csv):
        return "Error: La ruta del archivo CSV no está definida o no es válida.", 500

    conteo_total = analizar_abstracts(ruta_csv)
    # Llama a una función para mostrar resultados de abstracts
    # Aquí podrías renderizar en una nueva plantilla si se desea mostrar los datos
    return render_template('resultado.html', resultado=conteo_total, tipo="Análisis de Abstracts")

@app.route('/analisis_issn')
def graficar_nodos_aristas_route():
    if not os.path.isfile(ruta_csv):
        return "Error: La ruta del archivo CSV no está definida o no es válida.", 500

    df = load_data(ruta_csv)
    valores_mas_frecuentes = df.iloc[:, 4].value_counts().head(10)
    img = graficar_nodos_aristas(valores_mas_frecuentes, df)
    return send_file(img, mimetype='image/png')

def graficar_nodos_aristas(valores_mas_frecuentes, df):
    G = nx.Graph()
    node_colors = []

    for valor in valores_mas_frecuentes.index:
        frecuencia = valores_mas_frecuentes[valor]
        datos_filtrados = df[df.iloc[:, 4] == valor]
        total_citas = datos_filtrados.iloc[:, 11].sum()
        pais_frecuente = datos_filtrados.iloc[:, 10].mode()[0]

        if valor not in G:
            G.add_node(valor, label=valor)
            node_colors.append("lightblue")

        if pais_frecuente not in G:
            G.add_node(pais_frecuente, label=pais_frecuente)
            node_colors.append("lightgreen")
        G.add_edge(valor, pais_frecuente, label="País")

        cita_label = f"{total_citas} citas"
        if cita_label not in G:
            G.add_node(cita_label, label=cita_label)
            node_colors.append("lightcoral")
        G.add_edge(valor, cita_label, label="Citas")

    pos = nx.spring_layout(G, seed=42, k=0.5)
    fig, ax = plt.subplots(figsize=(12, 10))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color=node_colors,
            font_size=10, font_weight="bold", edge_color="gray", ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['label'] for u, v, d in G.edges(data=True)}, font_size=8)
    plt.title("Gráfico de Nodos y Aristas: Valores Frecuentes, País y Citas")

    img = BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)
    return img



if __name__ == '__main__':
    app.run(debug=True)
