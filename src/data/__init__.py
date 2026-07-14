"""Data loading and processing module"""
from .loaders import (
    load_education_data,
    load_gdp_data,
    load_life_expectancy_data,
    load_infant_mortality_data,
    load_all_data
)
from .processors import (
    clean_and_interpolate,
    detect_outliers_iqr,
    get_correlation_matrix,
    get_summary_statistics,
    get_missing_data_summary,
    detect_trends,
    get_all_trends
)

__all__ = [
    'load_education_data',
    'load_gdp_data',
    'load_life_expectancy_data',
    'load_infant_mortality_data',
    'load_all_data',
    'clean_and_interpolate',
    'detect_outliers_iqr',
    'get_correlation_matrix',
    'get_summary_statistics',
    'get_missing_data_summary',
    'detect_trends',
    'get_all_trends'
]
