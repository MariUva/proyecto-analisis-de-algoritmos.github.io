import pandas as pd

from src.data.data_processing import unify_data
from src.analysis.analysis import frequency_analysis
from src.statistics.statistics import generate_statistics

def main():
    # Paso 1: Unificar datos
    unified_data = unify_data()
    
    # Paso 2: Generar estadísticas
    stats = generate_statistics(unified_data)
    print(stats)
    
    # Paso 3: Análisis de frecuencias
    frequency_results = frequency_analysis(unified_data)
    print(frequency_results)

if __name__ == "__main__":
    main()
