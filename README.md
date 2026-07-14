# Education Impact Analysis - Data Science Project

## 📊 Descrizione

Analisi dell'impatto dell'educazione sugli indicatori di sviluppo socio-economico. 
Il progetto integra dati della World Bank su:

- **Indicatori Educativi**: Tasso di iscrizione primaria, completamento secondario, spesa educativa
- **Indicatori di Sviluppo**: GDP pro capite, aspettativa di vita, mortalità infantile
- **Paesi Analizzati**: Italia, Germania, USA, Canada, Cina, India, Brasile, Sud Africa, Kenya, Australia
- **Periodo**: 2000-2024

---

## 🏗️ Struttura del Progetto

```
project_data_manipulation/
├── src/                          # Moduli Python riutilizzabili
│   ├── config.py                 # Configurazione centralizzata (PERCORSI DINAMICI!)
│   ├── data/
│   │   ├── loaders.py           # Caricamento dati (Excel, CSV)
│   │   └── processors.py        # Pulizia, interpolazione, analisi
│   └── visualization/
│       └── plots.py             # Funzioni di visualizzazione (Plotly, Matplotlib)
│
├── data/
│   ├── raw/                     # Dati originali (non modificati)
│   │   ├── EdStats_v01.xlsx
│   │   ├── current_GDP_percap.csv
│   │   ├── life_expct.csv
│   │   └── infant_mortality.csv
│   └── processed/               # Dati elaborati (CSV)
│
├── notebooks/                   # Jupyter Notebooks ordinati sequenzialmente
│   ├── 01_data_loading.ipynb           # Carica e unisce i dataset
│   ├── 02_data_cleaning.ipynb          # Pulizia e interpolazione
│   ├── 03_exploratory_analysis.ipynb   # EDA e visualizzazioni
│   └── 04_final_analysis.ipynb         # Analisi finale e conclusioni
│
├── outputs/
│   ├── figures/                 # Grafici esportati
│   └── reports/                 # Report e analisi
│
├── tests/                       # Test unitari
├── requirements.txt             # Dipendenze Python
├── .env.example                 # Variabili d'ambiente
└── README.md                    # Questo file
```

---

## 🔑 Caratteristica Principale: Path Dinamici

**Tutto è gestito tramite `src/config.py`**:

```python
from src.config import DATA_FILES, COUNTRIES_LIST, MIN_YEAR

# Questi path si adattano automaticamente ovunque sia spostato il progetto
print(DATA_FILES['education'])  # ./data/raw/EdStats_v01.xlsx
print(DATA_FILES['gdp'])        # ./data/raw/current_GDP_percap.csv
```

✅ **Vantaggi**:
- Zero hardcoding di percorsi
- Funziona su Windows, Mac, Linux
- Spostare il progetto = Zero cambiamenti
- Facile condividere il codice

---

## 🚀 Quick Start

### 1. Setup Iniziale

```bash
# Clona il repository
cd project_data_manipulation

# Copia .env.example in .env (personalizzare se necessario)
cp .env.example .env

# Installa le dipendenze
pip install -r requirements.txt
```

### 2. Esegui i Notebook in Ordine

```bash
# Start Jupyter
jupyter notebook

# Apri i notebook nella cartella `notebooks/` in questo ordine:
# 1. 01_data_loading.ipynb          ← Carica i dati
# 2. 02_data_cleaning.ipynb         ← Pulisce i dati
# 3. 03_exploratory_analysis.ipynb  ← Esplora i dati
# 4. 04_final_analysis.ipynb        ← Analisi finale
```

---

## 📦 Moduli Disponibili

### `src.data.loaders`

```python
from src.data import load_all_data, load_education_data

# Carica tutti i dataset e li unisce
df = load_all_data()

# Carica solo i dati educativi (formato long)
df_ed = load_education_data()
```

### `src.data.processors`

```python
from src.data import (
    clean_and_interpolate,
    get_correlation_matrix,
    detect_outliers_iqr,
    get_all_trends
)

# Pulisci i dati (gestisce NaN con interpolazione)
df_clean = clean_and_interpolate(df)

# Calcola correlazioni
corr = get_correlation_matrix(df_clean)

# Rileva outlier con metodo IQR
outliers, lower, upper = detect_outliers_iqr(df_clean, 'GDP per Capita')

# Calcola trend per tutti i paesi
trends = get_all_trends(df_clean, 'Secondary Completion Rate (%)')
```

### `src.visualization.plots`

```python
from src.visualization import (
    plot_trends_by_country,
    plot_correlation_heatmap,
    plot_comparison_countries
)

# Crea visualizzazioni interattive
fig = plot_trends_by_country(df_raw)
fig.show()

# Heatmap di correlazione
fig = plot_correlation_heatmap(corr_matrix)
fig.show()

# Confronta paesi specifici
fig = plot_comparison_countries(df, 'Life Expectancy (Years)')
fig.show()
```

---

## 📊 Principali Scoperte

### ✅ Trend Positivi
- **Completamento scolastico**: crescita costante dal 2000 in tutti i paesi
- **Aspettativa di vita**: forte correlazione positiva con istruzione
- **Mortalità infantile**: diminuisce all'aumentare del tasso di istruzione

### ⚠️ Outlier e Anomalie
- **Sud Africa, India, Kenya**: mostrano volatilità dovuta a instabilità economica
- **Cina**: dati educativi lacunosi ma forte crescita nel completamento
- **Spesa educativa**: non sempre correlata linearmente con risultati

### 🎯 Conclusioni
L'investimento in educazione ha effetti misurabili e positivi sul benessere della popolazione,
andando oltre il semplice accesso scolastico.

---

## 🛠️ Sviluppo Futuro

- [ ] Aggiungere test unitari in `tests/`
- [ ] Implementare statistiche avanzate (regressione, clustering)
- [ ] Creare dashboard interattivo (Streamlit)
- [ ] Aggiungere more countries e indicatori
- [ ] Automatizzare l'aggiornamento dei dati dalla World Bank API

---

## 📝 Note Importanti

1. **CSV in `data/processed/`**: Vengono generati automaticamente dai notebook
2. **Path dinamici**: Modifica solo `src/config.py` se necessario
3. **Python version**: 3.8+ consigliato
4. **Jupyter**: Già incluso in requirements.txt

---

## 🎯 Key Features

✨ **Complete ETL Pipeline** — Load, clean, merge 4 World Bank datasets
📊 **Interactive Visualizations** — Plotly-based exploratory analysis
📈 **Statistical Analysis** — Correlation matrices, trend detection, outlier identification
🌍 **Global Insights** — Analysis of 10 countries across 24 years (2000-2023)
🏗️ **Modular Architecture** — Config-driven, reusable src/ modules
🔬 **Reproducible** — Jupyter notebooks documenting each analysis phase

---

## 👤 Autore

Progetto realizzato come analisi data science sull'impatto dell'educazione sulla società.

---

## 📄 Licenza

Dati della World Bank (Public Domain)
Codice: MIT License

---

**Per domande o problemi, controlla il file `src/config.py` per la configurazione!** ✨
