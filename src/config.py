"""
Configuration module - Manages paths and settings dynamically

This module uses environment variables from .env file for configuration.
Each developer can have their own .env with their own paths.

Important:
- .env is in .gitignore and should NEVER be on GitHub
- Share .env.example instead
- Use os.getenv() to read environment variables
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# ============================================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================================
# Try to load from .env file (local development)
# If .env doesn't exist, uses defaults or system environment variables
env_loaded = load_dotenv()

if env_loaded:
    print("✓ Loaded environment variables from .env file")
else:
    print("ℹ No .env file found - using defaults or system variables")

# ============================================================================
# PROJECT ROOT AND PATHS
# ============================================================================
# Root directory del progetto (genitore di src/)
PROJECT_ROOT = Path(__file__).parent.parent

# Read data directories from environment variables with fallback defaults
_raw_dir_env = os.getenv('DATA_RAW_DIR', './data/raw')
_processed_dir_env = os.getenv('DATA_PROCESSED_DIR', './data/processed')

# Convert to absolute paths if relative
DATA_RAW_DIR = Path(_raw_dir_env)
if not DATA_RAW_DIR.is_absolute():
    DATA_RAW_DIR = PROJECT_ROOT / DATA_RAW_DIR

DATA_PROCESSED_DIR = Path(_processed_dir_env)
if not DATA_PROCESSED_DIR.is_absolute():
    DATA_PROCESSED_DIR = PROJECT_ROOT / DATA_PROCESSED_DIR

# Ensure directories exist
DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# File paths dinamici - I percorsi sono costruiti dinamicamente
# Questo consente di spostare il progetto senza modificare il codice
DATA_FILES = {
    'education': DATA_RAW_DIR / "EdStats_v01.xlsx",
    'gdp': DATA_RAW_DIR / "current_GDP_percap.csv",
    'life_expectancy': DATA_RAW_DIR / "life_expct.csv",
    'infant_mortality': DATA_RAW_DIR / "infant_mortality.csv",
}

# Output directories
FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"

# Lista di paesi da analizzare
COUNTRIES_LIST = [
    'Italy', 'Germany', 'United States', 'Canada', 'China',
    'India', 'Brazil', 'South Africa', 'Kenya', 'Australia'
]

# Indicatori educativi da estrarre
EDUCATION_INDICATORS = [
    'Total net enrolment rate, primary, both sexes (%)',
    'Completion rate, upper secondary education, both sexes (%)',
    'Government expenditure on education as a percentage of GDP (%)'
]

# Mapping per i nomi degli indicatori
INDICATORS_MAP = {
    "Completion rate, upper secondary education, both sexes (%)": 
        "Secondary Completion Rate (%)",
    "Total net enrolment rate, primary, both sexes (%)": 
        "Primary Enrolment Rate(%)",
    "Government expenditure on education as a percentage of GDP (%)": 
        "Education Expenditure (% of GDP)",
}

# Parametri analisi
MIN_YEAR = int(os.getenv('MIN_YEAR', 2000))

# Colonne numeriche per analisi
NUMERIC_COLUMNS = [
    'Primary Enrolment Rate(%)',
    'Secondary Completion Rate (%)',
    'Education Expenditure (% of GDP)',
    'GDP per Capita',
    'Life Expectancy (Years)',
    'Infant Mortality Rate (per 1000 live births)'
]

# ============================================================================
# CONFIGURATION VALIDATION & DEBUG
# ============================================================================

def print_config_summary():
    """Print current configuration for debugging"""
    print("\n" + "="*80)
    print("CONFIGURATION SUMMARY")
    print("="*80 + "\n")
    
    print("📁 DIRECTORIES:")
    print(f"  Project Root:     {PROJECT_ROOT}")
    print(f"  Data Raw:         {DATA_RAW_DIR}")
    print(f"  Data Processed:   {DATA_PROCESSED_DIR}")
    print(f"  Figures Output:   {FIGURES_DIR}")
    print(f"  Reports Output:   {REPORTS_DIR}")
    
    print("\n📊 ANALYSIS PARAMETERS:")
    print(f"  Min Year:         {MIN_YEAR}")
    print(f"  Countries:        {len(COUNTRIES_LIST)}")
    print(f"  Indicators:       {len(EDUCATION_INDICATORS)}")
    print(f"  Numeric Columns:  {len(NUMERIC_COLUMNS)}")
    
    print("\n📝 ENVIRONMENT VARIABLES LOADED:")
    print(f"  DATA_RAW_DIR:     {os.getenv('DATA_RAW_DIR', 'NOT SET (using default)')}")
    print(f"  DATA_PROCESSED_DIR: {os.getenv('DATA_PROCESSED_DIR', 'NOT SET (using default)')}")
    print(f"  MIN_YEAR:         {os.getenv('MIN_YEAR', 'NOT SET (using default)')}")
    print(f"  LOG_LEVEL:        {os.getenv('LOG_LEVEL', 'NOT SET')}")
    
    print("\n✓ Configuration loaded successfully!")
    print("="*80 + "\n")


# Debug: Stampa configurazione quando il file è importato
if __name__ == "__main__":
    print_config_summary()
