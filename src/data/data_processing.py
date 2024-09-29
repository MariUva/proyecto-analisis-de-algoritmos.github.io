import pandas as pd

def load_data(file_path):
    # Cargar el archivo CSV
    df = pd.read_csv(file_path)
    
    # Renombrar columnas si es necesario, para facilitar su uso
    df.columns = [
        'article_title', 'author', 'journal_title', 'issn', 'isbn', 'publication_date',
        'volume', 'issue', 'first_page', 'page_count', 'accession_number', 'doi',
        'publisher', 'doctype', 'subjects', 'keywords', 'abstract', 'plink'
    ]
    
    # Extraer el año de la fecha de publicación
    df['year'] = pd.to_datetime(df['publication_date'], errors='coerce').dt.year
    
    return df
