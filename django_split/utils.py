from __future__ import division

import scipy
import scipy.stats

def overlapping(interval_a, interval_b):
    al, ah = interval_a
    bl, bh = interval_b

    if al > ah:
        raise ValueError("Interval A bounds are inverted")

    if bl > bh:
        raise ValueError("Interval B bounds are inverted")

    return ah >= bl and bh >= al

def compute_normal_ppf(data_points):
    mean, var = scipy.mean(data_points), scipy.var(data_points)
    return scipy.stats.norm(mean, var).ppf

def compute_binomial_rate_ppf(hits, total):
    if total == 0:
        return lambda p: 0

    distribution = scipy.binom((hits / total), total)

    return lambda p: distribution.ppf(p) / total

def compute_poisson_daily_rate_ppf(start_date, end_date, hits):
    days = (end_date - start_date).days
    return scipy.poisson(hits / days).ppf
