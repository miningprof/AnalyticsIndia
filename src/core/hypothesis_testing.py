import numpy as np
from scipy import stats

def one_sample_t_test(sample_data, pop_mean, alternative='two-sided'):
    if not isinstance(sample_data, np.ndarray):
        sample_data = np.array(sample_data)
    sample_data = sample_data[~np.isnan(sample_data)]
    if sample_data.size < 2 or not np.issubdtype(sample_data.dtype, np.number):
        return np.nan, np.nan
    return stats.ttest_1samp(sample_data, pop_mean, alternative=alternative)

def z_test_one_sample(sample_data, pop_mean, pop_std, alternative='two-sided'):
    if not isinstance(sample_data, np.ndarray):
        sample_data = np.array(sample_data)
    sample_data = sample_data[~np.isnan(sample_data)]
    if sample_data.size == 0 or pop_std <= 0 or not np.issubdtype(sample_data.dtype, np.number):
        return np.nan, np.nan

    sample_mean = np.mean(sample_data)
    n = len(sample_data)
    z_statistic = (sample_mean - pop_mean) / (pop_std / np.sqrt(n))
    
    if alternative == 'two-sided':
        p_value = 2 * (1 - stats.norm.cdf(np.abs(z_statistic)))
    elif alternative == 'less':
        p_value = stats.norm.cdf(z_statistic)
    elif alternative == 'greater':
        p_value = 1 - stats.norm.cdf(z_statistic)
    else:
        return z_statistic, np.nan
    return z_statistic, p_value

def chi_square_goodness_of_fit(observed_freq, expected_freq=None):
    try:
        observed_freq = np.asarray(observed_freq)
        if expected_freq is not None:
            expected_freq = np.asarray(expected_freq)
        if not np.issubdtype(observed_freq.dtype, np.number) or (expected_freq is not None and not np.issubdtype(expected_freq.dtype, np.number)):
             return np.nan, np.nan
        if np.any(observed_freq < 0) or (expected_freq is not None and np.any(expected_freq <=0)):
            return np.nan, np.nan
        return stats.chisquare(f_obs=observed_freq, f_exp=expected_freq)
    except Exception:
        return np.nan, np.nan
