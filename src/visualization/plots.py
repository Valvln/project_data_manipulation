"""Visualization functions for education analysis

This module provides functions to create various plots and visualizations
for exploring and presenting the education data.
"""

import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from src.config import NUMERIC_COLUMNS


def plot_trends_by_country(df, title="Trend degli indicatori educativi (2000-2024)"):
    """
    Crea una facet grid interattiva dei trend per ogni paese.
    
    Args:
        df (pd.DataFrame): DataFrame con dati in formato long (Year, Value, Indicator name)
        title (str): Titolo del grafico
        
    Returns:
        plotly.graph_objects.Figure: Figura interattiva
    """
    fig = px.line(
        df,
        x="Year",
        y="Value",
        color="Indicator name",
        facet_col="Country name",
        facet_col_wrap=5,
        markers=True,
        title=title,
        labels={
            "Value": "Valore",
            "Year": "Anno",
            "Indicator name": "Indicatore",
            "Country name": "Paese"
        }
    )
    
    fig.update_layout(
        title_x=0.5,
        height=1200,
        font=dict(size=10)
    )
    
    return fig


def plot_correlation_heatmap(corr_matrix, title="Correlation Heatmap of Key Indicators"):
    """
    Crea una heatmap interattiva delle correlazioni.
    
    Args:
        corr_matrix (pd.DataFrame): Matrice di correlazione
        title (str): Titolo del grafico
        
    Returns:
        plotly.graph_objects.Figure: Figura interattiva
    """
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        title=title,
        labels=dict(color="Correlazione"),
    )
    
    fig.update_layout(
        title_x=0.5,
        width=1000,
        height=900,
        font=dict(size=12),
        margin=dict(l=60, r=60, t=80, b=60)
    )
    
    return fig


def plot_data_availability(df):
    """
    Crea una heatmap della disponibilità dei dati (NaN) nel tempo.
    
    Args:
        df (pd.DataFrame): DataFrame con dati in formato long
        
    Returns:
        matplotlib.figure.Figure: Figura matplotlib
    """
    # Pivot per ottenere paese x anno
    pivot_data = df.pivot_table(
        index="Country name",
        columns="Year",
        values="Value"
    )
    
    plt.figure(figsize=(14, 8))
    sns.heatmap(
        pivot_data.isnull(),
        cmap="RdYlGn_r",
        cbar_kws={'label': 'Dato Mancante'},
        linewidths=0.5
    )
    
    plt.title("Mappa di disponibilità dei dati nel tempo", fontsize=14, fontweight='bold')
    plt.xlabel("Anno", fontsize=12)
    plt.ylabel("Paese", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return plt.gcf()


def plot_mean_indicators(df_ed):
    """
    Crea un bar chart della media dei tre indicatori per ogni paese.
    
    Args:
        df_ed (pd.DataFrame): DataFrame con dati educativi in formato long
        
    Returns:
        matplotlib.figure.Figure: Figura matplotlib
    """
    mean_values = df_ed.groupby(['Country name', 'Indicator name'])['Value'].mean().reset_index()
    
    plt.figure(figsize=(14, 8))
    sns.barplot(
        data=mean_values,
        x='Country name',
        y='Value',
        hue='Indicator name',
        palette="Set2",
        errorbar=None
    )
    
    plt.title("Media dei tre indicatori educativi per Paese", fontsize=14, fontweight='bold')
    plt.xlabel("Paese", fontsize=12)
    plt.ylabel("Valore medio", fontsize=12)
    plt.legend(title='Indicatore', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return plt.gcf()


def plot_box_distribution(df_ed):
    """
    Crea un box plot interattivo per confrontare la distribuzione degli indicatori.
    
    Args:
        df_ed (pd.DataFrame): DataFrame con dati educativi in formato long
        
    Returns:
        plotly.graph_objects.Figure: Figura interattiva
    """
    fig = px.box(
        df_ed,
        x="Indicator name",
        y="Value",
        color="Indicator name",
        points="all",
        hover_data=["Country name", "Year"],
        title="Distribuzione dei valori degli indicatori educativi",
        labels={
            "Value": "Valore",
            "Indicator name": "Indicatore",
            "Country name": "Paese"
        }
    )
    
    fig.update_layout(
        title_x=0.5,
        xaxis_title="Indicatore",
        yaxis_title="Valore",
        height=700,
        font=dict(size=11),
        showlegend=False
    )
    
    return fig


def plot_country_timeseries(df, country_name, figsize=(14, 8)):
    """
    Crea un time series plot per un paese specifico con tutti gli indicatori.
    
    Args:
        df (pd.DataFrame): DataFrame con tutti gli indicatori
        country_name (str): Nome del paese
        figsize (tuple): Dimensioni della figura
        
    Returns:
        matplotlib.figure.Figure: Figura matplotlib
    """
    country_data = df[df['Country Name'] == country_name].sort_values('Year')
    
    fig, axes = plt.subplots(2, 3, figsize=figsize)
    fig.suptitle(f"Indicatori di sviluppo - {country_name}", fontsize=16, fontweight='bold')
    
    for idx, col in enumerate(NUMERIC_COLUMNS):
        ax = axes[idx // 3, idx % 3]
        ax.plot(country_data['Year'], country_data[col], marker='o', linewidth=2, markersize=4)
        ax.set_title(col, fontsize=11, fontweight='bold')
        ax.set_xlabel("Anno")
        ax.grid(True, alpha=0.3)
        ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    return fig


def plot_comparison_countries(df, indicator, countries=None):
    """
    Crea un line plot comparativo per un indicatore su più paesi.
    
    Args:
        df (pd.DataFrame): DataFrame con tutti gli indicatori
        indicator (str): Nome dell'indicatore da visualizzare
        countries (list, optional): Lista di paesi da confrontare. Se None, usa tutti.
        
    Returns:
        plotly.graph_objects.Figure: Figura interattiva
    """
    if countries is None:
        countries = sorted(df['Country Name'].unique())
    
    data = df[df['Country Name'].isin(countries)].sort_values('Year')
    
    fig = px.line(
        data,
        x='Year',
        y=indicator,
        color='Country Name',
        markers=True,
        title=f"{indicator} - Comparazione tra Paesi",
        labels={
            'Year': 'Anno',
            indicator: 'Valore',
            'Country Name': 'Paese'
        }
    )
    
    fig.update_layout(
        title_x=0.5,
        hovermode='x unified',
        height=600,
        width=1000
    )
    
    return fig


def plot_scatter_relationships(df, x_col, y_col, size_col=None, color_col='Country Name'):
    """
    Crea uno scatter plot per esplorare relazioni tra variabili.
    
    Args:
        df (pd.DataFrame): DataFrame con i dati
        x_col (str): Colonna per asse X
        y_col (str): Colonna per asse Y
        size_col (str, optional): Colonna per dimensione punti
        color_col (str, optional): Colonna per colore punti
        
    Returns:
        plotly.graph_objects.Figure: Figura interattiva
    """
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        size=size_col,
        hover_data=['Country Name', 'Year'],
        title=f"Relazione tra {x_col} e {y_col}",
        labels={
            x_col: x_col,
            y_col: y_col,
        }
    )
    
    fig.update_layout(
        title_x=0.5,
        height=700,
        width=1000
    )
    
    return fig
