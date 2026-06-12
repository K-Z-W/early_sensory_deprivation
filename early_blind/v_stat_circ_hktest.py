import os
import numpy as np
import scipy.stats as ss 
import pycircstat as circ 
import pandas as pd
from scipy import special

def v_hkt(alpha, idp, idq, fn=['A','B'], f_only=False, chi_only=False): 
    # two-way anova of angles
    # alpha: subjects x vertices

    if (f_only==True)&(chi_only==True):
        raise Exception('f_only and chi_only are conflictive')

    n_sub, n_ver = np.shape(alpha)
    p = len(np.unique(idp))
    q = len(np.unique(idq))
    df = pd.DataFrame({fn[0]: idp, fn[1]: idq, 'fill':np.zeros(n_sub)})
    n = n_sub
    gr = df.groupby(fn)
    cn_multi = gr.count().unstack(fn[1])

    tr = n * circ.descriptive.resultant_vector_length(alpha, axis=0)
    kk = np.apply_along_axis(circ.distributions.kappa, 1, tr[:, np.newaxis]/n).squeeze()

    df_alpha = pd.DataFrame(alpha)
    df_alpha[fn[0]] = idp
    df_alpha[fn[1]] = idq

    # both factors
    gr = df_alpha.groupby(fn)
    cn = gr.count()
    cr = gr.agg(circ.descriptive.resultant_vector_length) * cn
    cn = cn.unstack(fn[1])
    cr = cr.unstack(fn[1])

    # 1st factor
    gr = df_alpha.groupby(fn[0])
    pn = gr.count().iloc[:,:-1]
    pr = gr.agg(circ.descriptive.resultant_vector_length).iloc[:,:-1] * pn
    pm = gr.agg(circ.descriptive.mean).iloc[:,:-1]   

    # 2nd factor
    gr = df_alpha.groupby(fn[1])
    qn = gr.count().iloc[:,:-1]
    qr = gr.agg(circ.descriptive.resultant_vector_length).iloc[:,:-1] * qn
    qm = gr.agg(circ.descriptive.mean).iloc[:,:-1]

    #------ F map (for Kappa > 2)---------------------------------
    ## effect of 1st factor
    eff_1_sum = np.zeros(n_ver)
    for i in range(p):
        eff_1_sum += (pr**2).iloc[i]/cn_multi.sum(axis=1).iloc[i]
    eff_1 = eff_1_sum - tr ** 2 / n
    df_1 = p - 1
    ms_1 = eff_1 / df_1

    ## effect of 2nd factor
    eff_2_sum = np.zeros(n_ver)
    for j in range(q):
        eff_2_sum += (qr**2).iloc[j]/cn_multi.sum(axis=0).iloc[j]
    eff_2 = eff_2_sum - tr ** 2 / n
    df_2 = q - 1
    ms_2 = eff_2 / df_2

    ## total effect
    eff_t = n - tr ** 2 / n
    df_t = n - 1
    m = cn_multi.values.mean()

    ## correction factor for improved F statistic
    beta = 1 / (1 - 1 / (5 * kk) - 1 / (10 * (kk ** 2)))

    ## residual effects
    eff_r_structure = cr**2./cn
    eff_r_structure_split = np.zeros((p*q, n_ver))
    k = 0
    for i in range(p):
        for j in range(q):
            # eff_r_structure_split[k,:] = eff_r_structure.filter(like=str(np.unique(idp)[i]), axis=0).filter(like=str(np.unique(idp)[j]))
            eff_r_structure_split[k,:] = eff_r_structure.loc[np.unique(idp)[i], (slice(None), np.unique(idq)[j])]
            k += 1

    eff_r = n - eff_r_structure_split.sum(axis=0)
    df_r = p*q*(m-1)
    ms_r = eff_r / df_r

    ## interaction
    eff_i = eff_r_structure_split.sum(axis=0) - (qr**2./qn).sum(axis=0) - (pr**2./pn).sum(axis=0) + tr**2/n
    df_i = (p-1)*(q-1)
    ms_i = eff_i/df_i

    ## F 
    FI = ms_i / ms_r
    pFI = 1 - ss.f.cdf(FI,df_i,df_r)

    F1 = beta * ms_1 / ms_r
    pF1 = 1 - ss.f.cdf(F1,df_1,df_r)

    F2 = beta * ms_2 / ms_r
    pF2 = 1 - ss.f.cdf(F2,df_2,df_r)
    #-------------------------------------------------

    #---------- chi2 map (for Kappa <= 2)-------------
    rr = special.iv(1,kk) / special.iv(0,kk)
    f = 2/(1-rr**2)

    chi_1 = f * ((pr**2./pn).sum(axis=0) - tr**2/n)
    df_1 = 2*(p-1)
    p1 = 1 - ss.chi2.cdf(chi_1, df=df_1)

    chi_2 = f * ((qr**2./qn).sum(axis=0)- tr**2/n)
    df_2 = 2*(q-1)
    p2 = 1 - ss.chi2.cdf(chi_2, df=df_2)

    chi_I = f * (eff_r_structure_split.sum(axis=0) - (qr**2./qn).sum(axis=0) - (pr**2./pn).sum(axis=0) + tr**2/n)
    df_i = (p-1) * (q-1)
    pI = ss.chi2.sf(chi_I, df=df_i)
    #--------------------------------------------------
    if (f_only==True) & (chi_only==False):
        smap = np.zeros((3, n_ver)) 
        smap[0,:]  = F1
        smap[1,:]  = F2
        smap[2,:]  = FI

        pmap = np.zeros((3, n_ver))
        pmap[0,:]  = pF1
        pmap[1,:]  = pF2
        pmap[2,:]  = pFI
        
    elif (f_only==False) & (chi_only==True):
        smap = np.zeros((3, n_ver)) 
        smap[0,:]  = chi_1
        smap[1,:]  = chi_2
        smap[2,:]  = chi_I

        pmap = np.zeros((3, n_ver))
        pmap[0,:]  = p1
        pmap[1,:]  = p2
        pmap[2,:]  = pI
        
    else:
        smap = np.zeros((3, n_ver)) 
        smap[0,kk>2]  = F1[kk>2]
        smap[0,kk<=2] = chi_1[kk<=2]
        smap[1,kk>2]  = F2[kk>2]
        smap[1,kk<=2] = chi_2[kk<=2]
        smap[2,kk>2]  = FI[kk>2]
        smap[2,kk<=2] = chi_I[kk<=2]

        pmap = np.zeros((3, n_ver))
        pmap[0,kk>2]  = pF1[kk>2]
        pmap[0,kk<=2] = p1[kk<=2]
        pmap[1,kk>2]  = pF2[kk>2]
        pmap[1,kk<=2] = p2[kk<=2]
        pmap[2,kk>2]  = pFI[kk>2]
        pmap[2,kk<=2] = pI[kk<=2]
   
    return smap, pmap, kk
