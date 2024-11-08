from collections import defaultdict
import csv
import re
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from io import BytesIO


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
    palabras = set(abstract.split())  # Convertimos a set para búsquedas más rápidas

    for categoria, variables in categorias.items():
        for variable, sinonimos in variables.items():
            for sinonimo in sinonimos:
                if sinonimo.lower() in palabras:
                    frecuencias[variable] += 1
    return frecuencias
# Función para analizar abstracts
def analizar_abstracts(file_path):
    conteo_total = defaultdict(lambda: defaultdict(int))
    with open(file_path, mode='r', newline='', encoding='utf-8-sig') as archivo:
        lector_csv = csv.DictReader(archivo)
        for fila in lector_csv:
            resumen = fila.get("Abstract", "")
            if resumen:
                frecuencias = contar_frecuencias(resumen, categorias)
                for variable, conteo in frecuencias.items():
                    for categoria, variables in categorias.items():
                        if variable in variables:
                            conteo_total[categoria][variable] += conteo
    return conteo_total

# Funciones para generar gráficos
def generar_grafico(categoria, conteo):
    variables = list(conteo.keys())
    frecuencias = list(conteo.values())

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(variables, frecuencias, color='skyblue')
    ax.set_title(f'Frecuencia de Aparición - {categoria}')
    ax.set_xlabel('Variables')
    ax.set_ylabel('Frecuencia')
    ax.tick_params(axis='x', rotation=45, labelsize=8)

    img = BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)
    return img

def graficar_totales(conteo_total):
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
    return img

def generar_nube_palabras(conteo_total):
    frecuencias = {variable: count for categoria, variables in conteo_total.items() for variable, count in variables.items()}
    wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=100).generate_from_frequencies(frecuencias)

    img = BytesIO()
    wordcloud.to_image().save(img, format='PNG')
    img.seek(0)
    return img