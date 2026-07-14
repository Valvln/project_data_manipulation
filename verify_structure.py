"""
Quick verification script to check project structure and paths
"""

import sys
from pathlib import Path

# Aggiungi la root del progetto al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("\n" + "="*80)
print("PROJECT STRUCTURE VERIFICATION")
print("="*80 + "\n")

# Verifica struttura di cartelle
print("1. DIRECTORY STRUCTURE:")
print("-" * 80)

required_dirs = [
    "src",
    "src/data",
    "src/analysis",
    "src/visualization",
    "data",
    "data/raw",
    "data/processed",
    "notebooks",
    "tests",
    "outputs",
    "outputs/figures",
    "outputs/reports"
]

for dir_path in required_dirs:
    full_path = project_root / dir_path
    exists = "✓" if full_path.exists() else "✗"
    print(f"  {exists} {dir_path}")

# Verifica file di configurazione
print("\n2. CONFIGURATION FILES:")
print("-" * 80)

required_files = [
    "src/config.py",
    "src/__init__.py",
    "src/data/loaders.py",
    "src/data/processors.py",
    "src/visualization/plots.py",
    "requirements.txt",
    ".env.example",
    ".gitignore",
    "README.md"
]

for file_path in required_files:
    full_path = project_root / file_path
    exists = "✓" if full_path.exists() else "✗"
    size = f" ({full_path.stat().st_size} bytes)" if full_path.exists() else ""
    print(f"  {exists} {file_path}{size}")

# Verifica notebook
print("\n3. NOTEBOOKS:")
print("-" * 80)

notebooks = [
    "notebooks/01_data_loading.ipynb",
    "notebooks/02_data_cleaning.ipynb",
    "notebooks/03_exploratory_analysis.ipynb",
    "notebooks/04_final_analysis.ipynb"
]

for nb_path in notebooks:
    full_path = project_root / nb_path
    exists = "✓" if full_path.exists() else "✗"
    size = f" ({full_path.stat().st_size} bytes)" if full_path.exists() else ""
    print(f"  {exists} {nb_path}{size}")

# Verifica file dati (raw)
print("\n4. DATA FILES (raw/):")
print("-" * 80)

try:
    from src.config import DATA_FILES
    
    for key, file_path in DATA_FILES.items():
        exists = "✓" if file_path.exists() else "✗"
        path_str = str(file_path.relative_to(project_root))
        print(f"  {exists} {key}: {path_str}")
except Exception as e:
    print(f"  ✗ Error loading config: {e}")

# Test import moduli
print("\n5. MODULE IMPORTS:")
print("-" * 80)

modules_to_test = [
    ("src.config", "Configuration module"),
    ("src.data.loaders", "Data loaders"),
    ("src.data.processors", "Data processors"),
    ("src.visualization.plots", "Visualization plots"),
]

for module_name, description in modules_to_test:
    try:
        __import__(module_name)
        print(f"  ✓ {module_name}: {description}")
    except Exception as e:
        print(f"  ✗ {module_name}: {str(e)[:60]}")

# Verifica config
print("\n6. CONFIGURATION PARAMETERS:")
print("-" * 80)

try:
    from src.config import (
        PROJECT_ROOT,
        DATA_RAW_DIR,
        DATA_PROCESSED_DIR,
        COUNTRIES_LIST,
        EDUCATION_INDICATORS,
        MIN_YEAR,
        NUMERIC_COLUMNS
    )
    
    print(f"  ✓ Project Root: {PROJECT_ROOT}")
    print(f"  ✓ Data Raw Dir: {DATA_RAW_DIR}")
    print(f"  ✓ Data Processed Dir: {DATA_PROCESSED_DIR}")
    print(f"  ✓ Countries: {len(COUNTRIES_LIST)} countries")
    print(f"  ✓ Indicators: {len(EDUCATION_INDICATORS)} indicators")
    print(f"  ✓ Min Year: {MIN_YEAR}")
    print(f"  ✓ Numeric Columns: {len(NUMERIC_COLUMNS)} columns")
except Exception as e:
    print(f"  ✗ Error loading config: {e}")

print("\n" + "="*80)
print("NEXT STEPS:")
print("="*80)
print("""
1. Ensure all data files are in data/raw/:
   - EdStats_v01.xlsx
   - current_GDP_percap.csv
   - life_expct.csv
   - infant_mortality.csv

2. Install dependencies:
   pip install -r requirements.txt

3. Run notebooks in order:
   jupyter notebook
   - 01_data_loading.ipynb
   - 02_data_cleaning.ipynb
   - 03_exploratory_analysis.ipynb
   - 04_final_analysis.ipynb

4. All paths are dynamic via src/config.py
   No hardcoding needed! 🎉

""" + "="*80 + "\n")
