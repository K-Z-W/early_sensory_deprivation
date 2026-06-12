import os, sys, glob 
import numpy as np 
import pandas as pd 
import scipy.stats as ss
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

def v_anova2_bs(data, factor_A, factor_B, Covs, factor_names, ss_type=2):
    # two-way between-subject anova
    # data: subjects x vertices

    n_sub, n_ver = np.shape(data)
    n_s_cov, n_c_cov = np.shape(Covs)
    if n_s_cov != n_sub:
        Exception("The number of the Covariates rows is wrong!")
    if len(factor_names) != (n_c_cov+2):
        Exception("The number of factor names is wrong!")
    
    data_var = pd.DataFrame(data)
    col_names = [f'Score{i}' for i in range(1,1+n_ver)]
    data_var.columns = col_names
    data_var[factor_names[0]] = factor_A
    data_var[factor_names[1]] = factor_B
    for k, fac in enumerate(factor_names[2:]):
        data_var[fac] = Covs[:,k]

    formula_covs = ' '
    for fac in factor_names[2:]:
        formula_covs = f'{formula_covs} + {fac}'
        
    anova_results = {
    dv: anova_lm(ols(f'{dv} ~ {factor_names[0]} + {factor_names[1]} + {factor_names[0]}:{factor_names[1]}{formula_covs}', data_var).fit(), typ=ss_type)
    for dv in col_names
    }

    Fv = np.zeros((3,n_ver))
    Pv = np.zeros((3,n_ver))
    for j in range(3):
        Fv[j,:] = np.asarray([anova_results[dv]['F'][j] for dv in col_names])
        Pv[j,:] = np.asarray([anova_results[dv]['PR(>F)'][j] for dv in col_names])

    return Fv, Pv