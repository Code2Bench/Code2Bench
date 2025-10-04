
import scipy
import numpy as np

def mean_confidence_interval(data, confidence=0.95):
    # Compute the confidence interval around the mean

    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t._ppf((1 + confidence) / 2.0, n - 1)
    return m, m - h, m + h