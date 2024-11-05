from flask import Flask, render_template, request, send_file
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from io import BytesIO
from src.statistics.conteoFrecuencia import analizar_abstracts, generar_nube_palabras, ruta_csv

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
    # Verifica si `ruta_csv` está definida y es válida
    if not os.path.isfile(ruta_csv):
        return "Error: La ruta del archivo CSV no está definida o no es válida.", 500

    # Obtiene `conteo_total` usando `analizar_abstracts`
    conteo_total = analizar_abstracts(ruta_csv)
    img = generar_nube_palabras(conteo_total)  # Pasa `conteo_total`, no `ruta_csv`
    return send_file(img, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
