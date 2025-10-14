import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import torch




# Define the objective function
def func(x, k1,k2,k3,Imax,I0,kd):
    L,I,Imax,kd,I0=x
    if not 0 < k1 <10 or not 0 < k2 or not 0 < k3:
        return np.ones_like(L) * 1e10  # 返回一个大的值
    x1 = np.sqrt((k2*I+1)*(k2*I+1)+ 8 * L * (k2*k2*k3*I*I + k1))
    return (Imax * ((L / 2) * ((x1 - (k2*I+1)) / (x1 + (k2*I+1))) * (kd)/ (1 + (L / 2) * ((x1 - (k2*I+1)) / (x1 + (k2*I+1))) * (kd))) + I0)





def cal(LBDName, SperLBDData,I0_val,Imax_val):

    L = SperLBDData["LBD"].dropna(axis=0)
    I = SperLBDData["inducer"].dropna(axis = 0)
    Imax = pd.Series([Imax_val]*len(L))
    I0 = pd.Series([I0_val]*len(L))
    RPU = SperLBDData["RPU"].dropna(axis = 0)
    # P1 = np.log10(RPU)
    kd = SperLBDData['kd'].dropna(axis=0)
    # bounds = ([0,0,Imax_val,kd,I0],[np.inf,np.inf,Imax_val,kd,I0])
    print(type(L))
    print(type(RPU))
    func_fit = lambda x,k1,k2,k3 : func(x,k1,k2,k3,Imax,I0,kd)
    params, pcov = curve_fit(func_fit, (L,I,Imax,kd,I0), RPU, p0=[0.1,0.1,0.1], maxfev = 5000000)

    k1,k2,k3 = params
    print('k1= %.15f' % k1)
    print('k2= %.15f' % k2)
    print('k3= %.15f' % k3)
    return [k1,k2,k3]
    # Compute the fitted curve
    # P1_fit = func((L,I), k1,k2,k3)

    # # Calculate the sum of squared residuals
    # residuals = P1 - P1_fit
    # ssr = np.sum(residuals ** 2)
    # print('Sum of squared residuals: %.4f' % ssr)







            
