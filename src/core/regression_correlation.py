import numpy as np
from scipy import stats

def linear_regression(x, y):
    if not isinstance(x, (np.ndarray, list, tuple)) or not isinstance(y, (np.ndarray, list, tuple)):
        return None
    x_arr = np.asarray(x)
    y_arr = np.asarray(y)

    valid_indices = ~ (np.isnan(x_arr) | np.isnan(y_arr))
    x_clean = x_arr[valid_indices]
    y_clean = y_arr[valid_indices]

    if x_clean.size != y_clean.size or x_clean.size < 2 or not np.issubdtype(x_clean.dtype, np.number) or not np.issubdtype(y_clean.dtype, np.number):
        return None
    return stats.linregress(x_clean, y_clean)

def pearson_correlation(x, y):
    if not isinstance(x, (np.ndarray, list, tuple)) or not isinstance(y, (np.ndarray, list, tuple)):
        return np.nan, np.nan
    x_arr = np.asarray(x)
    y_arr = np.asarray(y)

    valid_indices = ~ (np.isnan(x_arr) | np.isnan(y_arr))
    x_clean = x_arr[valid_indices]
    y_clean = y_arr[valid_indices]

    if x_clean.size != y_clean.size or x_clean.size < 2 or not np.issubdtype(x_clean.dtype, np.number) or not np.issubdtype(y_clean.dtype, np.number):
        return np.nan, np.nan
    return stats.pearsonr(x_clean, y_clean)
