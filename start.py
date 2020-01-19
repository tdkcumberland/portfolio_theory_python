import numpy as np
import scipy as sp
import pandas as pd
import pandas_datareader.data as pddata
import datetime
import matplotlib.pyplot as plt
import retrieveDumpData as rdd
from scipy import stats, optimize, interpolate

# rdd.oneYearDump_logRet('VTI',fileName='VTI-2019')
# rdd.oneYearDump_logRet('SPEM',fileName='SPEM-2019')
# rdd.oneYearDump_logRet('BAR',fileName='BAR-2019')
# def twoComponentPortfolio(w1,w2, var1, var2, sigma1,sigma2,rho):
#     return  w1**2*var1 +w2**2*var2+2*w1*w2*rho*sigma1*sigma2

SPEM = pd.read_pickle('SPEM-2019')
VTI = pd.read_pickle('VTI-2019')
BAR = pd.read_pickle('BAR-2019')

monthly = [''.join([datetime.datetime.strptime(a, '%Y-%m-%d').strftime("%Y"),datetime.datetime.strptime(a, '%Y-%m-%d').strftime("%m")]) for a in SPEM.index]
yearly = [datetime.datetime.strptime(a, '%Y-%m-%d').strftime("%Y") for a in SPEM.index]
y = pd.concat([VTI.VTI_Ret,SPEM.SPEM_Ret,BAR.BAR_Ret],axis=1)
y['monthly']=monthly
y['yearly'] = yearly
y=y.replace(np.NaN,0)

retMonth = y.groupby(y.monthly).sum()
print(retMonth)
covar = np.dot(retMonth.T,retMonth)
weight = np.matrix(np.array([0.9,0.05,0.05,]))
returns = weight*covar*weight.T
print(returns)
# VTIstd= sp.stats.tstd(retMonth.VTI_Ret)
# SPEMstd= sp.stats.tstd(retMonth.SPEM_Ret)
# VTIvar = VTIstd**2
# SPEMvar = SPEMstd**2
# corr,pval = sp.stats.pearsonr(retMonth.VTI_Ret,retMonth.SPEM_Ret)

# n = 10000
# step = 1./n
# var =[]
# w1 = np.arange(0,1,step)
# w2 = 1 - w1
# var = twoComponentPortfolio(w1,w2,VTIvar,SPEMvar,VTIstd,SPEMstd,corr)

# w1Result = zip(var,w1)
# w2Result = zip(var,w2)
# w1Weight,w2Weight = min(w1Result),min(w2Result)

# fig, ax1 = plt.subplots()
# ax2 = ax1.twinx()
# ax1.plot(w1,var, 'r-')
# ax1.plot(w1Weight[1],w1Weight[0], 'ro')
# ax2.plot(w2,var, 'b-')
# ax2.plot(w2Weight[1],w2Weight[0], 'bo')
# ax2.set_ylabel('VTI', color='r')
# ax1.set_ylabel('SPEM', color='b')
# ax1.set_xlabel('Weight')
# plt.text(w1Weight[1],w1Weight[0], 'VTI weight')
# plt.text(w2Weight[1],w2Weight[0], 'SPEM weight')
# plt.show()

# var=w1**2*var1 +w2**2*var2+2*w1*w2*rho*sigma1*sigma2
# print(VTI[(VTI['dividend amount']!=np.NaN) & (VTI['dividend amount']>0)])

# fig, ax1 = plt.subplots()
# ax2 = ax1.twinx()

# ax1.plot(SPEM.index, SPEM['Ret'], 'r-')
# ax2.plot(VTI.index, VTI['Ret'],'b-')


# ax1.set_ylabel('SPEM', color='r')
# fig.autofmt_xdate(rotation=45)

# plt.show()