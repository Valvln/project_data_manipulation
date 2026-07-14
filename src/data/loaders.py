"""Data loading functions for education analysis

This module provides functions to load and preprocess data from various sources,
including World Bank education statistics and development indicators.
All file paths are managed dynamically through config.py.
"""

import pandas as pd
from src.config import (
    DATA_FILES, COUNTRIES_LIST, EDUCATION_INDICATORS,
    INDICATORS_MAP, MIN_YEAR
)


def load_education_data():
    """
    Carica e processa dati educativi da Excel.
    
    Returns:
        pd.DataFrame: DataFrame con indicatori educativi in formato long
                     Colonne: Country name, Country code, Indicator name, Year, Value
    """
    print(f"Loading education data from {DATA_FILES['education']}...")
    
    df = pd.read_excel(DATA_FILES['education'])
    df.columns = df.columns.str.strip()
    
    # Filtra per paesi di interesse
    df = df[df['Country name'].isin(COUNTRIES_LIST)]
    print(f"  - Filtered to {df['Country name'].nunique()} countries")
    
    # Filtra per indicatori di interesse
    df = df[df['Indicator name'].isin(EDUCATION_INDICATORS)]
    print(f"  - Filtered to {len(EDUCATION_INDICATORS)} indicators")
    
    # Converti in formato long (tidy)
    df = df.melt(
        id_vars=['Country name', 'Country code', 'Indicator name', 'Indicator code'],
        var_name='Year',
        value_name='Value'
    )
    
    # Converti Year in numerico
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    
    # Filtra per anni da MIN_YEAR in poi
    df = df[df['Year'] >= MIN_YEAR].reset_index(drop=True)
    print(f"  - Retained data from {MIN_YEAR} onwards")
    
    # Rimuovi colonna Indicator code (non necessaria)
    df = df.drop(columns=['Indicator code'])
    
    print(f"  ✓ Education data loaded: {df.shape[0]} rows")
    return df


def load_gdp_data():
    """
    Carica e processa dati GDP pro capite da CSV.
    
    Returns:
        pd.DataFrame: DataFrame con GDP pro capite
                     Colonne: Country Name, Country Code, Year, GDP per Capita
    """
    print(f"Loading GDP data from {DATA_FILES['gdp']}...")
    
    # Salta le prime 4 righe di metadati della World Bank
    df = pd.read_csv(DATA_FILES['gdp'], sep=',', skiprows=4)
    df.columns = df.columns.str.strip()
    
    # Rimuovi colonne inutili
    cols_to_drop = [col for col in df.columns if col.startswith('Unnamed')]
    df = df.drop(columns=cols_to_drop + ['Indicator Code'])
    
    # Filtra per paesi di interesse
    df = df[df['Country Name'].isin(COUNTRIES_LIST)]
    
    # Converti in formato long
    df = df.melt(
        id_vars=['Country Name', 'Country Code', 'Indicator Name'],
        var_name='Year',
        value_name='GDP per Capita'
    ).drop(columns=['Indicator Name']).reset_index(drop=True)
    
    # Converti Year e GDP in numerici
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['GDP per Capita'] = pd.to_numeric(df['GDP per Capita'], errors='coerce')
    
    # Filtra per anni e rimuovi NaN
    df = df[df['Year'] >= MIN_YEAR].dropna(subset=['GDP per Capita'])
    
    # Arrotonda
    df['GDP per Capita'] = df['GDP per Capita'].round(2)
    
    # Ordina
    df = df.sort_values(by=['Country Name', 'Year']).reset_index(drop=True)
    
    print(f"  ✓ GDP data loaded: {df.shape[0]} rows")
    return df


def load_life_expectancy_data():
    """
    Carica e processa dati aspettativa di vita da CSV.
    Il CSV è in formato wide (anni come colonne): melt per convertire a formato long.
    
    Returns:
        pd.DataFrame: DataFrame con aspettativa di vita
                     Colonne: Country Name, Country Code, Year, Life Expectancy (Years)
    """
    print(f"Loading life expectancy data from {DATA_FILES['life_expectancy']}...")
    
    df = pd.read_csv(DATA_FILES['life_expectancy'], sep=',')
    df.columns = df.columns.str.strip()
    
    # Rinomina colonne chiave
    df = df.rename(columns={
        'REF_AREA': 'Country Code',
        'REF_AREA_LABEL': 'Country Name',
    })
    
    # Filtra per paesi di interesse PRIMA del melt
    df = df[df['Country Name'].isin(COUNTRIES_LIST)]
    
    # Identifica le colonne anno (sono stringhe numeriche: '1960', '1961', ..., '2023')
    year_columns = [col for col in df.columns if col.isdigit()]
    
    # Melt: converte da wide a long
    # Mantiamo Country Code, Country Name e tutte le colonne anno
    id_vars = ['Country Code', 'Country Name']
    df = df.melt(
        id_vars=id_vars,
        value_vars=year_columns,
        var_name='Year',
        value_name='Life Expectancy (Years)'
    )
    
    # Converti Year a numerico
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    
    # Converti Life Expectancy a numerico
    df['Life Expectancy (Years)'] = pd.to_numeric(df['Life Expectancy (Years)'], errors='coerce')
    
    # Filtra per anni e rimuovi NaN
    df = df[(df['Year'] >= MIN_YEAR) & (df['Life Expectancy (Years)'].notna())]
    
    # Arrotonda Life Expectancy
    df['Life Expectancy (Years)'] = df['Life Expectancy (Years)'].round(2)
    
    # Ordina
    df = df.sort_values(by=['Country Name', 'Year']).reset_index(drop=True)
    
    print(f"  ✓ Life expectancy data loaded: {df.shape[0]} rows")
    return df


def load_infant_mortality_data():
    """
    Carica e processa dati mortalità infantile da CSV.
    
    Returns:
        pd.DataFrame: DataFrame con mortalità infantile
                     Colonne: Country Name, Country Code, Year, 
                     Infant Mortality Rate (per 1000 live births)
    """
    print(f"Loading infant mortality data from {DATA_FILES['infant_mortality']}...")
    
    df = pd.read_csv(DATA_FILES['infant_mortality'], sep=',')
    
    # Rinomina colonne chiave
    df = df.rename(columns={
        'REF_AREA': 'Country Code',
        'REF_AREA_LABEL': 'Country Name',
        'TIME_PERIOD': 'Year',
        'OBS_VALUE': 'Infant Mortality Rate (per 1000 live births)'
    })
    
    # Seleziona solo colonne necessarie
    df = df[[
        'Country Code', 'Country Name', 'Year', 
        'Infant Mortality Rate (per 1000 live births)'
    ]]
    
    # Filtra per paesi di interesse
    df = df[df['Country Name'].isin(COUNTRIES_LIST)]
    
    # Converti Year in numerico
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    
    # Filtra per anni e rimuovi NaN
    df = df[df['Year'] >= MIN_YEAR].dropna()
    
    # Converti mortalità infantile in numerico e arrotonda
    df['Infant Mortality Rate (per 1000 live births)'] = (
        pd.to_numeric(
            df['Infant Mortality Rate (per 1000 live births)'], 
            errors='coerce'
        ).round(2)
    )
    
    # Ordina
    df = df.sort_values(by=['Country Name', 'Year']).reset_index(drop=True)
    
    print(f"  ✓ Infant mortality data loaded: {df.shape[0]} rows")
    return df


def load_all_data():
    """
    Carica e unisce tutti i dataset (educazione, GDP, aspettativa di vita, mortalità).
    
    Returns:
        pd.DataFrame: DataFrame unito con tutte le variabili
                     Colonne: Country Name, Country Code, Year, e tutte le metriche
    """
    print("\n" + "="*60)
    print("Loading all datasets...")
    print("="*60 + "\n")
    
    # Carica tutti i dati
    df_ed = load_education_data()
    df_gdp = load_gdp_data()
    df_life = load_life_expectancy_data()
    df_mort = load_infant_mortality_data()
    
    print("\n" + "-"*60)
    print("Transforming education data to wide format...")
    print("-"*60)
    
    # Trasforma dati educativi da long a wide (un indicatore per colonna)
    df_ed = df_ed.pivot_table(
        index=['Country name', 'Country code', 'Year'],
        columns='Indicator name',
        values='Value'
    ).reset_index()
    
    # Rinomina colonne secondo INDICATORS_MAP
    df_ed = df_ed.rename(columns=INDICATORS_MAP | {
        'Country name': 'Country Name',
        'Country code': 'Country Code'
    })
    
    print("\n" + "-"*60)
    print("Merging datasets...")
    print("-"*60)
    
    # Unisci tutti i dataframe tramite merge interno
    # (mantiene solo le righe con dati in tutti i dataset)
    df_final = pd.merge(
        df_ed, df_gdp,
        on=['Country Name', 'Country Code', 'Year'],
        how='inner'
    )
    
    df_final = pd.merge(
        df_final, df_life,
        on=['Country Name', 'Country Code', 'Year'],
        how='inner'
    )
    
    df_final = pd.merge(
        df_final, df_mort,
        on=['Country Name', 'Country Code', 'Year'],
        how='inner'
    )
    
    print(f"\n✓ All datasets merged successfully!")
    print(f"  Final shape: {df_final.shape}")
    print(f"  Date range: {df_final['Year'].min():.0f} - {df_final['Year'].max():.0f}")
    print(f"  Countries: {df_final['Country Name'].nunique()}")
    print(f"  Years: {df_final['Year'].nunique()}")
    print(f"  Total records: {df_final.shape[0]}")
    
    return df_final
