import pandas as pd

def descriptive_statistics(df, column1, column2=None):
    if column2:
        # Análisis bidimensional
        return df.groupby([column1, column2]).size().reset_index(name='counts')
    else:
        # Análisis unidimensional
        return df[column1].describe()
