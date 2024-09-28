#Calculos estadisticos
import pandas as pd

def generate_statistics(data):
    # Generar estadísticas descriptivas
    stats = data.describe(include='all')
    return stats
