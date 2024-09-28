#Analisis de datos
import pandas as pd

def frequency_analysis(data):
    # Implementar análisis de frecuencia
    frequency = data['abstract'].str.split(expand=True).stack().value_counts()
    return frequency
