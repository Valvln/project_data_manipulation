"""Data processing and cleaning functions

This module provides functions for cleaning, transforming, and analyzing
the education data after it has been loaded.
"""

import pandas as pd
import numpy as np
from src.config import NUMERIC_COLUMNS


def clean_and_interpolate(df):
    """
    Pulisce i dati e gestisce i valori NaN con interpolazione.
    
    Processo:
    1. Ordina per Paese e Anno
    2. Interpola linearmente i valori mancanti entro ogni paese
    3. Usa forward fill e backward fill per i rimanenti NaN
    
    Args:
        df (pd.DataFrame): DataFrame con dati grezzi
        
    Returns:
        pd.DataFrame: DataFrame pulito senza NaN
    """
    print("\n" + "="*60)
    print("Cleaning and interpolating data...")
    print("="*60 + "\n")
    
    # Copia per non modificare l'originale
    df = df.copy()
    
    print(f"Missing values BEFORE cleaning:")
    print(df[NUMERIC_COLUMNS].isna().sum())
    
    # Ordina per Paese e Anno
    df = df.sort_values(by=['Country Name', 'Year']).reset_index(drop=True)
    
    # Step 1: Interpolazione lineare per paese
    print("\n  - Applying linear interpolation within each country...")
    df[NUMERIC_COLUMNS] = (
        df.groupby('Country Name')[NUMERIC_COLUMNS]
        .transform(lambda group: group.interpolate(method='linear'))
    )
    
    # Step 2: Forward fill + backward fill per rimanenti NaN
    print("  - Applying forward fill and backward fill...")
    df[NUMERIC_COLUMNS] = (
        df.groupby('Country Name')[NUMERIC_COLUMNS]
        .ffill()
        .bfill()
    )
    
    print(f"\nMissing values AFTER cleaning:")
    remaining_na = df[NUMERIC_COLUMNS].isna().sum()
    print(remaining_na)
    
    if remaining_na.sum() == 0:
        print("\n✓ All missing values successfully handled!")
    else:
        print(f"\n⚠ Warning: {remaining_na.sum()} NaN values remain")
    
    return df


def detect_outliers_iqr(df, column, country_name=None):
    """
    Rileva outlier usando il metodo Interquartile Range (IQR).
    
    Metodo: Un valore è considerato outlier se:
        - Valore < Q1 - 1.5*IQR  (outlier basso)
        - Valore > Q3 + 1.5*IQR  (outlier alto)
    
    Args:
        df (pd.DataFrame): DataFrame con i dati
        column (str): Nome della colonna da analizzare
        country_name (str, optional): Se specificato, analizza solo questo paese
        
    Returns:
        pd.DataFrame: Dataframe con i soli outlier rilevati
    """
    if country_name is None:
        # Analizza il dataset completo
        data_subset = df[column]
    else:
        # Analizza solo il paese specificato
        data_subset = df[df['Country Name'] == country_name][column]
    
    Q1 = data_subset.quantile(0.25)
    Q3 = data_subset.quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    # Trova outlier
    if country_name is None:
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    else:
        outliers = df[
            (df['Country Name'] == country_name) &
            ((df[column] < lower_bound) | (df[column] > upper_bound))
        ]
    
    return outliers, lower_bound, upper_bound


def get_correlation_matrix(df):
    """
    Calcola la matrice di correlazione tra le variabili numeriche.
    
    Args:
        df (pd.DataFrame): DataFrame con i dati
        
    Returns:
        pd.DataFrame: Matrice di correlazione (Pearson)
    """
    return df[NUMERIC_COLUMNS].corr()


def get_summary_statistics(df, by_country=False):
    """
    Calcola statistiche descrittive per le variabili numeriche.
    
    Args:
        df (pd.DataFrame): DataFrame con i dati
        by_country (bool): Se True, calcola statistiche per ogni paese
        
    Returns:
        pd.DataFrame: Statistiche descrittive
    """
    if by_country:
        return df.groupby('Country Name')[NUMERIC_COLUMNS].describe()
    else:
        return df[NUMERIC_COLUMNS].describe()


def get_missing_data_summary(df):
    """
    Fornisce un report dettagliato sui dati mancanti.
    
    Args:
        df (pd.DataFrame): DataFrame con i dati
        
    Returns:
        pd.DataFrame: Report sui dati mancanti per colonna e paese
    """
    print("\n" + "="*60)
    print("Missing Data Summary")
    print("="*60 + "\n")
    
    # Valori mancanti per colonna
    print("Missing values by column:")
    missing_by_col = df[NUMERIC_COLUMNS].isna().sum()
    print(missing_by_col)
    
    # Percentuale
    print("\nPercentage of missing values by column:")
    pct_missing = (df[NUMERIC_COLUMNS].isna().sum() / len(df) * 100).round(2)
    print(pct_missing)
    
    # Valori mancanti per paese e anno
    print("\n\nMissing values by country and year:")
    for country in sorted(df['Country Name'].unique()):
        country_data = df[df['Country Name'] == country]
        years_with_missing = country_data[country_data[NUMERIC_COLUMNS].isna().any(axis=1)]['Year'].tolist()
        if years_with_missing:
            print(f"  {country}: Years {sorted(years_with_missing)}")
    
    return missing_by_col, pct_missing


def detect_trends(df, indicator, country_name):
    """
    Analizza il trend (incremento/decremento) di un indicatore per un paese.
    
    Args:
        df (pd.DataFrame): DataFrame con i dati
        indicator (str): Nome dell'indicatore
        country_name (str): Nome del paese
        
    Returns:
        dict: Statistiche del trend (slope, direction, change_pct)
    """
    country_data = df[df['Country Name'] == country_name].sort_values('Year')
    
    if len(country_data) < 2:
        return None
    
    years = country_data['Year'].values
    values = country_data[indicator].values
    
    # Calcola slope usando regressione lineare semplice
    coefficients = np.polyfit(years, values, 1)
    slope = coefficients[0]
    
    # Direzione
    direction = "↑ Crescente" if slope > 0 else "↓ Decrescente" if slope < 0 else "→ Stabile"
    
    # Cambio percentuale
    start_value = values[0]
    end_value = values[-1]
    change_pct = ((end_value - start_value) / abs(start_value) * 100) if start_value != 0 else 0
    
    return {
        'country': country_name,
        'indicator': indicator,
        'slope': round(slope, 4),
        'direction': direction,
        'change_pct': round(change_pct, 2),
        'start_value': round(start_value, 2),
        'end_value': round(end_value, 2),
        'years': int(years[-1] - years[0])
    }


def get_all_trends(df, indicator):
    """
    Calcola trends per un indicatore su tutti i paesi.
    
    Args:
        df (pd.DataFrame): DataFrame con i dati
        indicator (str): Nome dell'indicatore
        
    Returns:
        list: Lista di dizionari con trend per ogni paese
    """
    trends = []
    for country in sorted(df['Country Name'].unique()):
        trend = detect_trends(df, indicator, country)
        if trend:
            trends.append(trend)
    
    return trends
