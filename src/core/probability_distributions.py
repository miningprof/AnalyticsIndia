from scipy import stats
import numpy as np

def normal_pdf(x, mean, std_dev):
    if std_dev <= 0: return np.nan
    return stats.norm.pdf(x, loc=mean, scale=std_dev)

def normal_cdf(x, mean, std_dev):
    if std_dev <= 0: return np.nan
    return stats.norm.cdf(x, loc=mean, scale=std_dev)

def normal_ppf(q, mean, std_dev):
    if std_dev <= 0 or not (0 < q < 1): return np.nan
    return stats.norm.ppf(q, loc=mean, scale=std_dev)

def normal_rvs(mean, std_dev, size=1):
    if std_dev <= 0: return np.nan if size == 1 else np.full(size, np.nan)
    return stats.norm.rvs(loc=mean, scale=std_dev, size=size)

def binomial_pmf(k, n, p):
    if not (0 <= p <= 1) or n < 0 or k < 0 or k > n: return np.nan
    return stats.binom.pmf(k, n, p)

def binomial_cdf(k, n, p):
    if not (0 <= p <= 1) or n < 0 or k < 0: return np.nan
    return stats.binom.cdf(k, n, p)

def binomial_ppf(q, n, p):
    if not (0 <= p <= 1) or n < 0 or not (0 < q < 1): return np.nan
    return stats.binom.ppf(q, n, p)

def binomial_rvs(n, p, size=1):
    if not (0 <= p <= 1) or n < 0: return np.nan if size == 1 else np.full(size, np.nan)
    return stats.binom.rvs(n, p, size=size)
