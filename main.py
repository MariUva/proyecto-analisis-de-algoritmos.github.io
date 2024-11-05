from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import networkx as nx
from wordcloud import WordCloud
from src.data.data_processing import load_data
from src.statistics.statistics import descriptive_statistics
from src.statistics.conteoFrecuencia import analizar_abstracts
from src.union_csv.union_csv import limpiar_columnas_csv, unificar_data

# Carga las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

def verificar_existencia_data(directory_path_csv, nombre_documento_unido):
    # Combina la ruta de la carpeta con el nombre del archivo
    ruta_completa = os.path.join(directory_path_csv, nombre_documento_unido)
    return os.path.isfile(ruta_completa)

@app.route('/')
def index():
    # Página principal con opciones de análisis
    return render_template('index.html')

@app.route('/unir_data', methods=['POST'])
def unir_data_route():
    directory_path_csv = os.getenv('DIRECTORY_CSV')
    nombre_documento_unido = os.getenv('NAME_DATA')
    
    if not verificar_existencia_data(directory_path_csv, nombre_documento_unido):
        limpiar_columnas_csv(directory_path_csv)
        unificar_data(directory_path_csv, nombre_documento_unido)
    return redirect(url_for('index'))

@app.route('/analisis', methods=['POST'])
def realizar_analisis():
    tipo_analisis = request.form.get("tipo_analisis")
    file_path = os.getenv('FILE_PATCH')
    df = load_data(file_path)

    if tipo_analisis == "Análisis Unidimensional":
        columna = request.form.get("columna")
        if columna:
            result = descriptive_statistics(df, columna)
            return render_template('resultado.html', resultado=result, tipo=tipo_analisis)
        else:
            return "Debe ingresar una columna válida", 400

    elif tipo_analisis == "Análisis Bidimensional":
        columna1 = request.form.get("columna1")
        columna2 = request.form.get("columna2")
        if columna1 and columna2:
            result = descriptive_statistics(df, columna1, columna2)
            return render_template('resultado.html', resultado=result, tipo=tipo_analisis)
        else:
            return "Debe ingresar ambas columnas", 400

    elif tipo_analisis == "Análisis de Abstracts":
        conteo_total = analizar_abstracts('data/bases_datos/data_unido.csv')
        return render_template('resultado.html', resultado=conteo_total, tipo=tipo_analisis)

    elif tipo_analisis == "Nube de Palabras Abstract":
        abstracts = " ".join(df['abstract'].dropna())
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(abstracts)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.savefig('static/nube_palabras.png')
        return render_template('resultado.html', image_path='static/nube_palabras.png', tipo=tipo_analisis)

    elif tipo_analisis == "Análisis de ISSN":
        valores_mas_frecuentes = df.iloc[:, 4].value_counts().head(10)
        graficar_nodos_aristas(valores_mas_frecuentes, df)
        plt.savefig('static/grafico_issn.png')
        return render_template('resultado.html', image_path='static/grafico_issn.png', tipo=tipo_analisis)

    return "Análisis no válido", 400

def graficar_nodos_aristas(valores_mas_frecuentes, df):
    # Crear un gráfico de nodos y aristas
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
    plt.figure(figsize=(12, 10))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color=node_colors,
            font_size=10, font_weight="bold", edge_color="gray")
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['label'] for u, v, d in G.edges(data=True)}, font_size=8)
    plt.title("Gráfico de Nodos y Aristas")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
