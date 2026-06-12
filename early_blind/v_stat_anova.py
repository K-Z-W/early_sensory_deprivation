import os 
import numpy as np 
import scipy.stats as ss 
import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.multivariate.manova import MANOVA
from sklearn.preprocessing import StandardScaler


def v_anova1(data, idg):
    # one-way ANOVA
    # data: subjects x vertices
    # idg: factor-Group 

    n_sub, n_ver = np.shape(data)
    g  = len(np.unique(idg))

    df_b = g - 1
    df_w = n_sub - g

    data_M = data.mean(axis=0)

    # every group mean
    data_mg = np.zeros((g,n_ver))
    ss_b = np.zeros(n_ver)
    ss_w = np.zeros(n_ver)
    for i in range(g):
        g_index = idg==np.unique(idg)[i]
        gn = sum(g_index)
        data_mg[i,:] = data[g_index,:].mean(axis=0)
        vb = ((data_mg[i,:] - data_M)**2) * gn
        ss_b += vb
        for s in range(gn):
            Xs = data[g_index,:]
            vw = (Xs[s,:] - data_mg[i,:])**2 
            ss_w += vw

    ms_b = ss_b / df_b
    ms_w = ss_w / df_w

    f   = ms_b / ms_w 
    p   = 1 - ss.f.cdf(f, df_b, df_w)

    return f, p


def v_anova_rm(data, idg, idt):
    # one-way or two-way (idg is all ones) repeated measure ANOVA
    # two-way factors: one is between-subject, th other is within-subject factor
    # data: subjects x vertices

    n_sub, n_ver = np.shape(data)
    g = len(np.unique(g))
    t = len(np.unique(idt))

    df_g = g - 1
    df_t = t - 1
    df_s = n_sub - g
    df_gt= (g - 1) * (t - 1)
    df_e = (n_sub - g) * (t - 1)

    X_all = data.copy()
    mX = np.zeros((g,t,n_ver))
    for i in range(g):
        for j in range (t):
            g_index = idg==np.unique(idg)[i]
            t_index = idt==np.unique(idt)[j]
            mX[i,j,:] = X_all[g_index & t_index, :].mean(axis=0)

    mX_all = X_all.mean(axis=0)

    mX_g  = np.zeros((g, n_ver))   
    ss_g  = np.zeros(n_ver)
    ss_s  = np.zeros(n_ver)

    for i in range(g):
        g_index = idg==np.unique(idg)[i]  
        gn = sum(g_index)     
        mX_g[i,:] = X_all[g_index,:].mean(axis=0)
        vg = ((mX_g[i,:] - mX_all)**2) * (t * gn)
        ss_g += vg

        mX_sg = np.zeros((gn, n_ver))
        for j in range(t):
            t_index = idt==np.unique(idt)[j]
            mX_sg += X_all[g_index & t_index,:]
        mX_sg = mX_sg / t

        for s in range(gn):
            vs = ((mX_sg[s,:] - mX_g[i,:])**2) * t
            ss_s += vs 

    mX_t = np.zeros((t, n_ver))
    ss_t = np.zeros(n_ver)
    tn   = np.zeros(t)
    for j in range(t):
        t_index = idt==np.unique(idt)[j] 
        tn[j] = sum(t_index)
        mX_t[j,:] = X_all[t_index,:].mean(axis=0)
        vt = ((mX_t[j,:] - mX_all)**2) * n_sub 
        ss_t += vt

    ss_gt = np.zeros(n_ver)
    for i in range(g):
        gn = sum(idg==np.unique(idg)[i])
        for j in range(t):
            vgt = ((mX[i,j,:] - mX_g[i,:] - mX_t[j,:] + mX_all)**2) * gn
            ss_gt += vgt 

    ss_e = np.zeros(n_ver)
    for i in range(g):
        g_index = idg==np.unique(idg)[i]
        gn = sum(g_index & t_index)

        mX_sg = np.zeros((gn, n_ver))
        for j in range(t):
            t_index = idt==np.unique(idt)[j] 
            mX_sg += X_all[g_index & t_index,:]
        mX_sg = mX_sg / t

        for j in range(t):
            for s in range(sn):
                Xs = X_all[g_index & t_index, :]
                ve = (Xs[s,:] - mX[i,j,:] - mX_sg[s,:] + mX_g[i,:])**2
                ss_e += ve

    if g > 1:
        ms_g = ss_g / df_g
        ms_gt= ss_gt/ df_gt

    ms_t = ss_t / df_t
    ms_s = ss_s / df_s 
    ms_e = ss_e / df_e 

    if g > 1:
        f_g = ms_g / ms_s
        f_gt= ms_gt/ ms_e
        p_g = 1 - ss.f.cdf(f_g, df_g, df_s) 
        p_gt= 1 - ss.f.cdf(f_gt,df_gt,df_e)

    f_t = ms_t / ms_e
    f_s = ms_s / ms_e
    p_t = 1 - ss.f.cdf(f_t, df_t, df_e)
    p_s = 1 - ss.f.cdf(f_s, df_s, df_e)

    if p > 1:
        pmap = np.zeros((4, n_ver))
        pmap[0,:] = p_g 
        pmap[1,:] = p_t
        pmap[2,:] = p_gt 
        pmap[3,:] = p_s 

        fmap = np.zeros((4, n_ver))
        fmap[0,:] = f_g
        fmap[1,:] = f_t
        fmap[2,:] = f_gt 
        fmap[3,:] = f_s
    
    else:
        pmap = np.zeros((2, n_ver))
        pmap[0,:] = p_t
        pmap[1,:] = p_s 

        fmap = np.zeros((2, n_ver))
        fmap[0,:] = f_t
        fmap[1,:] = f_s

    return fmap, pmap


def v_anova2(data, idp, idq):
    # two-way ANOVA
    # data: subjects x vertices

    n_sub, n_ver = np.shape(data)
    p = len(np.unique(idp))
    q = len(np.unique(idq))            

    df_a = p - 1
    df_b = q - 1 
    df_ab= (p-1)*(q-1)
    df_e = n_sub - (p*q)

    X_all = data.copy()
    mX = np.zeros((p,q,n_ver))
    for i in range(p):
        p_index = idp==np.unique(idp)[i]
        for j in range(q):
            q_index = idq==np.unique(idq)[j]
            mX[i,j,:] = X_all[p_index & q_index,:].mean(axis=0)
        
    mX_all = X_all.mean(axis=0)

    mX_a = np.zeros((p, n_ver))
    ss_a = np.zeros(n_ver)
    for i in range(p):
        p_index = idp==np.unique(idp)[i]
        pn = sum(p_index)
        mX_a[i,:] = X_all[p_index,:].mean(axis=0) 
        va = ((mX_a[i,:] - mX_all)**2) * pn
        ss_a += va
    
    mX_b = np.zeros((q, n_ver))
    ss_b = np.zeros(n_ver)
    for j in range(q):
        q_index = idq==np.unique(idq)[j]
        qn = sum(q_index)
        mX_b[j,:] = X_all[q_index,:].mean(axis=0)
        vb = ((mX_b[j,:] - mX_all)**2) * qn
        ss_b += vb

    ss_ab = np.zeros(n_ver)
    ss_e  = np.zeros(n_ver)
    for i in range(p):
        p_index = idp==np.unique(idp)[i]
        for j in range(q):
            q_index = idq==np.unique(idq)[j]
            pq_index = p_index & q_index
            sn = sum(pq_index)

            vab = ((mX[i,j,:] - mX_a[i,:] - mX_b[j,:] + mX_all)**2) * sn
            ss_ab += vab 

            for s in range(sn):
                Xab = X_all[pq_index,:]
                ve = (Xab[s,:] - mX[i,j,:])**2
                ss_e += ve 

    ms_a = ss_a / df_a
    ms_b = ss_b / df_b 
    ms_ab= ss_ab/ df_ab
    ms_e = ss_e / df_e

    f_a = ms_a / ms_e
    f_b = ms_b / ms_e
    f_ab= ms_ab/ ms_e

    p_a = 1 - ss.f.cdf(f_a, df_a, df_e)
    p_b = 1 - ss.f.cdf(f_b, df_b, df_e)
    p_ab= 1 - ss.f.cdf(f_ab,df_ab,df_e)

    fmap = np.zeros((3, n_ver))
    pmap = np.zeros((3, n_ver))

    fmap[0,:] = f_a 
    fmap[1,:] = f_b 
    fmap[2,:] = f_ab 
    pmap[0,:] = p_a 
    pmap[1,:] = p_b 
    pmap[2,:] = p_ab 

    return fmap, pmap


def v_aov(data, x):

    data_use = data[:,x]
    grp = ['g1']*17 + ['g2']*18 + ['g1']*16 + ['g2']*22
    sit = ['s1']*(17+18) + ['s2']*(16+22)

    df_aov = pd.DataFrame({'score':data_use, 'group':grp, 'site':sit})
    #aov = pg.anova(df_aov, dv='score', between=['group','site'])
  
    formula = 'score ~ group + site + group:site'
    model = ols(formula, df_aov).fit()
    aov = anova_lm(model, typ=2)

    return aov['F'][0], aov['PR(>F)'][0], aov['F'][1], aov['PR(>F)'][1], aov['F'][2], aov['PR(>F)'][2]

def type2_anova_matrixized(matrix, factor_A, factor_B):
    """
    Performs matrixized Type-II ANOVA on a given matrix where rows represent observations,
    and columns represent different dependent variables, with two factors (A and B).
    
    Parameters:
    - matrix: 2D numpy array where each column is a dependent variable.
    - factor_A: 1D numpy array representing Factor A for each observation.
    - factor_B: 1D numpy array representing Factor B for each observation.
    
    Returns:
    - F_A_values: F-statistics for Factor A for each column.
    - F_B_values: F-statistics for Factor B for each column.
    """
    n, num_columns = matrix.shape  # Number of observations and dependent variables
    
    # Design matrices for Factor A, Factor B, and the full model (A + B)
    X_full = np.column_stack((np.ones(n), factor_A, factor_B))  # Full model: Intercept + Factor A + Factor B
    X_B = np.column_stack((np.ones(n), factor_B))               # Model with Factor B only
    X_A = np.column_stack((np.ones(n), factor_A))               # Model with Factor A only

    # Solve for the regression coefficients using matrix multiplication (least squares)
    beta_full = np.linalg.inv(X_full.T @ X_full) @ X_full.T @ matrix
    beta_A_given_B = np.linalg.inv(X_B.T @ X_B) @ X_B.T @ matrix
    beta_B_given_A = np.linalg.inv(X_A.T @ X_A) @ X_A.T @ matrix

    # Predicted values for each model
    y_pred_full = X_full @ beta_full  # Full model predictions
    y_pred_A_given_B = X_B @ beta_A_given_B  # Factor A after adjusting for B
    y_pred_B_given_A = X_A @ beta_B_given_A  # Factor B after adjusting for A

    # Residual sum of squares (RSS) for each model
    RSS_full = np.sum((matrix - y_pred_full) ** 2, axis=0)  # Full model RSS
    RSS_A_given_B = np.sum((matrix - y_pred_A_given_B) ** 2, axis=0)  # Factor A given B RSS
    RSS_B_given_A = np.sum((matrix - y_pred_B_given_A) ** 2, axis=0)  # Factor B given A RSS

    # Calculate sum of squares for Factor A and Factor B
    SSA = RSS_A_given_B - RSS_full  # Sum of squares for Factor A (adjusted for B)
    SSB = RSS_B_given_A - RSS_full  # Sum of squares for Factor B (adjusted for A)
    SS_residual = RSS_full  # Residual sum of squares (from the full model)

    # Degrees of freedom
    df_A = 1  # Factor A has 1 degree of freedom
    df_B = 1  # Factor B has 1 degree of freedom
    df_residual = n - 3  # n - number of parameters in the full model (intercept + 2 factors)

    # Mean squares for Factor A, Factor B, and the residuals
    MS_A = SSA / df_A
    MS_B = SSB / df_B
    MS_residual = SS_residual / df_residual

    # F-statistics for Factor A and Factor B
    F_A = MS_A / MS_residual
    F_B = MS_B / MS_residual

    p_A = ss.f.sf(F_A, df_A, df_residual)
    p_B = ss.f.sf(F_B, df_B, df_residual)

    return F_A, F_B, p_A, p_B

def v_mancova(matrix, factor_A, factor_B, covs):

    n_samples, n_dependent_vars = np.shape(matrix)
    n_cov_samples, n_covariates = np.shape(covs)

    if n_samples != n_cov_samples:
        Exception("wrong axis")
    
    # Create a DataFrame
    data = pd.DataFrame(matrix, columns=[f'Value_{i+1}' for i in range(n_dependent_vars)])
    data['Factor1'] = factor_A
    data['Factor2'] = factor_B
    str_list_covs = []
    for i in range(n_covariates):
        data[f'Covariate{i}'] = covs[:,i]
        str_list_covs.append(f'Covariate{i}')
    
    # Standardize the covariates (important for MANCOVA)
    scaler = StandardScaler()
    data[str_list_covs] = scaler.fit_transform(data[str_list_covs])
    
    # Define the formula for MANCOVA
    dependent_formula = ' + '.join([f'Value_{i+1}' for i in range(n_dependent_vars)])
    covariate_formula = ' + '.join([f'Covariate{i+1}' for i in range(n_covariates)])
    
    formula = f'{dependent_formula} ~ Factor1 + Factor2 + Factor1:Factor2 + {covariate_formula}'
    print(formula)
    
    # Perform MANCOVA
    manova = MANOVA.from_formula(formula, data=data)
    result = manova.mv_test()
    
    # Extract F-values and p-values for Factor1, Factor2, and Covariates
    f_values = []
    p_values = []
    
    # Iterate through each factor and covariate
    for term in ['Factor1', 'Factor2']:
        # Get the results for each term
        term_result = result[term].iloc[0]  # Extract the row for the term
        f_values.append(term_result['F Value'])
        p_values.append(term_result['Pr > F'])
    
    # Convert to two rows (vectors)
    f_values = np.array(f_values)
    p_values = np.array(p_values)
    
    return f_values, p_values