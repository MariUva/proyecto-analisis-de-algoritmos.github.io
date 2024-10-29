import csv
import matplotlib.pyplot as plt
from collections import defaultdict
import re
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.style as style
from wordcloud import WordCloud


# Ruta al archivo CSV
#ruta_csv = r'./data/APPLIED AND ENGINEERING.csv'

ruta_csv = r'./data/bases_datos/data_unido.csv'

# Definir categorías y sinónimos
categorias = {
    "Habilidades": {
        "Abstraction": ["Abstraction"],
        "Algorithm": ["Algorithm", "Algorithms"],
        "Algorithmic thinking": ["Algorithmic thinking", "Algorithmic reasoning"],
        "Coding": ["Coding", "Code", "Programming"],
        "Collaboration": ["Collaboration", "Teamwork", "Cooperation"],
        "Creativity": ["Creativity", "Creative thinking"],
        "Critical thinking": ["Critical thinking", "Critical analysis", "Critical reasoning"],
        "Debug": ["Debug", "Debugging"],
        "Decomposition": ["Decomposition", "Problem decomposition"],
        "Evaluation": ["Evaluation", "Assessment"],
        "Generalization": ["Generalization"],
        "Logic": ["Logic", "Logical reasoning"],
        "Modularity": ["Modularity", "Modular design"],
        "Patterns recognition": ["Patterns recognition", "Pattern matching"],
        "Problem solving": ["Problem solving", "Problem resolution"],
        "Programming": ["Programming", "Coding", "Software development"],
        "Representation": ["Representation", "Modeling"],
        "Reuse": ["Reuse", "Code reuse"],
        "Simulation": ["Simulation", "Modeling and simulation"]
    },
    "Conceptos Computacionales": {
        "Conditionals": ["Conditionals", "If statements", "Condition"],
        "Control structures": ["Control structures", "Control flow"],
        "Directions": ["Directions", "Instructions"],
        "Events": ["Events", "Event-driven"],
        "Functions": ["Functions", "Procedures"],
        "Loops": ["Loops", "Iteration", "For loop", "While loop"],
        "Modular structure": ["Modular structure", "Modularity"],
        "Parallelism": ["Parallelism", "Concurrency"],
        "Sequences": ["Sequences", "Order of operations"],
        "Software/hardware": ["Software", "Hardware"],
        "Variables": ["Variables", "Data variables"]
    },
    "Actitudes": {
        "Emotional": ["Emotional", "Emotions"],
        "Engagement": ["Engagement", "Involvement", "Participation"],
        "Motivation": ["Motivation", "Drive", "Interest"],
        "Perceptions": ["Perceptions", "Perceived value"],
        "Persistence": ["Persistence", "Perseverance"],
        "Self-efficacy": ["Self-efficacy", "Confidence", "Belief in ability"],
        "Self-perceived": ["Self-perceived", "Self-perception"]
    },
    "Propiedades Psicométricas": {
        "Classical Test Theory (CTT)": ["Classical Test Theory", "CTT"],
        "Confirmatory Factor Analysis (CFA)": ["Confirmatory Factor Analysis", "CFA"],
        "Exploratory Factor Analysis (EFA)": ["Exploratory Factor Analysis", "EFA"],
        "Item Response Theory (IRT)": ["Item Response Theory", "IRT"],
        "Reliability": ["Reliability"],
        "Structural Equation Model (SEM)": ["Structural Equation Model", "SEM"],
        "Validity": ["Validity", "Construct validity"]
    },
    "Herramientas de Evaluación": {
        "Beginners Computational Thinking test (BCTt)": ["Beginners Computational Thinking test", "BCTt"],
        "Coding Attitudes Survey (ESCAS)": ["Coding Attitudes Survey", "ESCAS"],
        "Collaborative Computing Observation Instrument": ["Collaborative Computing Observation Instrument"],
        "Competent Computational Thinking test (cCTt)": ["Competent Computational Thinking test", "cCTt"],
        "Computational thinking skills test (CTST)": ["Computational thinking skills test", "CTST"],
        "Computational Thinking Assessment for Chinese Elementary Students (CTA-CES)": ["Computational Thinking Assessment", "CTA-CES"],
        "CT Scale (CTS)": ["CT Scale", "CTS"]
    },
    "Diseño de Investigación": {
        "No experimental": ["No experimental", "Non-experimental"],
        "Experimental": ["Experimental", "Controlled experiment"],
        "Longitudinal research": ["Longitudinal research", "Longitudinal study"],
        "Mixed methods": ["Mixed methods", "Mixed research"],
        "Post-test": ["Post-test"],
        "Pre-test": ["Pre-test"],
        "Quasi-experiments": ["Quasi-experiments", "Quasi-experimental"]
    },
    "Nivel de Escolaridad": {
        "Upper elementary school": ["Upper elementary education", "Upper elementary school"],
        "Primary school": ["Primary school", "Primary education", "Elementary school"],
        "Early childhood education": ["Early childhood education", "Kindergarten", "Preschool"],
        "Secondary school": ["Secondary school", "Secondary education"],
        "High school": ["High school", "Higher education"],
        "University": ["University", "College"]
    },
    "Estrategia": {
        "Construct-by-self mind mapping (CBS-MM)": ["Construct-by-self mind mapping", "CBS-MM"],
        "Design-based learning (DBL)": ["Design-based learning", "DBL"],
        "Gamification": ["Gamification"],
        "Flipped classroom": ["Flipped classroom"],
        "Game-based learning": ["Game-based learning"],
        "Inquiry-based learning": ["Inquiry-based learning"],
        "Problem-based learning": ["Problem-based learning"],
        "Project-based learning": ["Project-based learning"],
        "Collaborative learning": ["Collaborative learning", "Team-based learning"],
        "Cooperative learning": ["Cooperative learning", "Teamwork"]
    },
    "Herramienta": {
        "Alice": ["Alice"],
        "Arduino": ["Arduino"],
        "Scratch": ["Scratch", "ScratchJr"],
        "Blockly Games": ["Blockly Games"],
        "Code.org": ["Code.org"],
        "Robot Turtles": ["Robot Turtles"],
        "Minecraft": ["Minecraft"],
        "Py– Learn": ["Py– Learn"],
        "Mimo": ["Mimo"]
}
}
# Función para contar frecuencias
def contar_frecuencias(abstract, categorias):
    frecuencias = defaultdict(int)
    abstract = abstract.lower()
    abstract = re.sub(r'[^\w\s]', ' ', abstract)
    palabras = abstract.split()

    for categoria, variables in categorias.items():
        for variable, sinonimos in variables.items():
            for sinonimo in sinonimos:
                patron = r'\b' + re.escape(sinonimo.lower()) + r'\b'
                for palabra in palabras:
                    if re.search(patron, palabra):
                        frecuencias[variable] += 1
    return frecuencias

# Función para analizar abstracts
def analizar_abstracts(file_path):
    with open(file_path, mode='r', newline='', encoding='utf-8-sig') as archivo:
        lector_csv = csv.DictReader(archivo)
        conteo_total = defaultdict(lambda: defaultdict(int))
        
        for fila in lector_csv:
            resumen = fila.get("Abstract", "")
            if resumen:
                frecuencias = contar_frecuencias(resumen, categorias)
                for variable, conteo in frecuencias.items():
                    for categoria, variables in categorias.items():
                        if variable in variables:
                            conteo_total[categoria][variable] += conteo
    return conteo_total

# Función para agregar gráfico en pestaña
def agregar_grafico_pestana(tab_control, nombre_categoria, conteo):
    tab = ttk.Frame(tab_control)
    tab_control.add(tab, text=nombre_categoria)

    variables = list(conteo.keys())
    frecuencias = list(conteo.values())

    # Ajustar el tamaño de la figura en función del número de variables
    ancho_figura = 5 + len(variables) * 1.5
    ancho_figura = min(ancho_figura, 15)
    
    fig, ax = plt.subplots(figsize=(ancho_figura, 5))
    
    bars = ax.bar(variables, frecuencias, color='skyblue')
    ax.set_title(f'Frecuencia de Aparición - {nombre_categoria}')
    ax.set_xlabel('Variables')
    ax.set_ylabel('Frecuencia')
    ax.tick_params(axis='x', rotation=45, labelsize=8)

    # Mostrar los valores en cada barra
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval + 1, int(yval), ha='center', va='bottom')

    canvas = FigureCanvasTkAgg(fig, master=tab)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Cerrar la figura para evitar la ventana adicional
    plt.close(fig)

# Función para agregar pestaña de totales
def agregar_pestana_totales(tab_control, conteo_total):
    tab_totales = ttk.Frame(tab_control)
    tab_control.add(tab_totales, text="Totales por Categoría")

    fig, ax = plt.subplots(figsize=(8, 5))
    categorias = list(conteo_total.keys())
    total_por_categoria = [sum(conteo.values()) for conteo in conteo_total.values()]

    bars = ax.bar(categorias, total_por_categoria, color='lightgreen')
    ax.set_title("Totales por Categoría")
    ax.set_xlabel("Categorías")
    ax.set_ylabel("Total Frecuencia")
    ax.tick_params(axis='x', rotation=45, labelsize=8)

    # Mostrar los valores en cada barra
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval + 1, int(yval), ha='center', va='bottom')

    canvas = FigureCanvasTkAgg(fig, master=tab_totales)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Cerrar la figura para evitar la ventana adicional
    plt.close(fig)

# Función para crear ventana con pestañas
def crear_ventana_con_pestanas(conteo_total):
    ventana = tk.Toplevel()
    ventana.title("Gráficos por Categoría")
    ventana.geometry('900x600')

    tab_control = ttk.Notebook(ventana)
    tab_control.pack(expand=1, fill="both")

    # Agregar gráficos en cada pestaña
    for categoria, conteo in conteo_total.items():
        agregar_grafico_pestana(tab_control, categoria, conteo)

    # Agregar la pestaña de totales
    agregar_pestana_totales(tab_control, conteo_total)


    # Botón para generar la nube de palabras
    button_nube = ttk.Button(ventana, text="Generar Nube de Palabras", command=lambda: generar_nube_palabras_frecuencia(conteo_total))
    button_nube.pack(pady=10)


    ventana.protocol("WM_DELETE_WINDOW", ventana.destroy)

# Función para abrir la ventana desde el botón
def mostrar_graficos():
    conteo_total = analizar_abstracts(ruta_csv)
    crear_ventana_con_pestanas(conteo_total)


# Función para generar una nube de palabras a partir del conteo de frecuencia
def generar_nube_palabras_frecuencia(conteo_total):
    # Convierte el conteo de frecuencia en un diccionario compatible con WordCloud
    frecuencias = {}
    for categoria, variables in conteo_total.items():
        for variable, conteo in variables.items():
            frecuencias[variable] = conteo

    # Genera la nube de palabras
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(frecuencias)

    # Mostrar la nube de palabras
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

