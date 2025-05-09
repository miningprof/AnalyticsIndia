import numpy as np
from scipy import stats
import pandas as pd

def calculate_descriptive_stats(data_series):
    if not isinstance(data_series, pd.Series):
        data_series = pd.Series(data_series)
    
    if data_series.empty or pd.api.types.is_numeric_dtype(data_series) == False:
        return {
            'Mean': np.nan,
            'Median': np.nan,
            'Variance (Population)': np.nan,
            'Std. Deviation (Population)': np.nan,
            'Minimum': np.nan,
            'Maximum': np.nan,
            'Count': len(data_series),
            'Error': 'Data is empty or non-numeric'
        }

    stats_results = {
        'Mean': np.mean(data_series),
        'Median': np.median(data_series),
        'Variance (Population)': np.var(data_series, ddof=0),
        'Std. Deviation (Population)': np.std(data_series, ddof=0),
        'Minimum': np.min(data_series),
        'Maximum': np.max(data_series),
        'Count': len(data_series)
    }
    return stats_results
