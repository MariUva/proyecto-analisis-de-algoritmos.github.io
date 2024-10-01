import csv
import matplotlib.pyplot as plt
from collections import defaultdict
import re


# Ruta al archivo CSV
ruta_csv = r'./data/APPLIED AND ENGINEERING.csv'

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

def analizar_abstracts(file_path):
    # Leer el archivo CSV
    with open(file_path, mode='r', newline='', encoding='utf-8-sig') as archivo:
        lector_csv = csv.DictReader(archivo)
        conteo_total = defaultdict(int)

        for fila in lector_csv:
            resumen = fila.get("Abstract", "")
            if resumen:
                frecuencias = contar_frecuencias(resumen, categorias)
                for variable, conteo in frecuencias.items():
                    conteo_total[variable] += conteo

    # Mostrar el resultado
    print("Frecuencia de aparición de variables en los abstracts:")
    for variable, conteo in conteo_total.items():
        print(f"{variable}: {conteo}")

    # Generar el gráfico de barras
    variables = list(conteo_total.keys())
    frecuencias = list(conteo_total.values())


    plt.figure(figsize=(10, 6))

    barras = plt.bar(variables, frecuencias, color='skyblue')  # Genera el gráfico de barras

    for barra in barras:
        yval = barra.get_height()  # Obtiene la altura de cada barra
        plt.text(barra.get_x() + barra.get_width()/2, yval + 2, int(yval), ha='center', va='bottom')  # Muestra el valor

    plt.bar(variables, frecuencias, color='skyblue')
    plt.title('Frecuencia de Aparición de Variables en Abstracts')
    plt.xlabel('Variables')
    plt.ylabel('Frecuencia')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.yticks(range(0, max(frecuencias) + 50, 50))  # Ajusta la escala del eje Y con un intervalo de 50 en 50.
    plt.show()

   