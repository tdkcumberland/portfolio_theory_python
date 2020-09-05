import numpy as np
import scipy as sp
import pandas as pd
import pandas_datareader.data as pddata
import datetime
import matplotlib.pyplot as plt
import retrieveDumpData as rdd
from scipy import stats, optimize, interpolate
from numpy.linalg import inv, pinv

pd.options.display.float_format = '{:,.4f}'.format

tickers = ['VTI', 'BAR']#, 'VCE.TRT', 'VGK', 'SCHH']#, 'REM', 'BND', 'VAB.TRT']
columns = [ticker + '_Ret' for ticker in tickers]
weight = np.matrix(np.array([0.5,0.5]))#,0.2,0.2,0.2]))

# for ticker in tickers:
#     rdd.oneYearDump_logRet(ticker,fileName=ticker+'-2020', startDate=datetime.datetime(2000, 1,1), endDate=datetime.datetime(2020, 6, 30))

# rdd.oneYearDump_logRet('VAB.TRT',fileName='VAB.TRT'+'-2000', startDate=datetime.datetime(2007, 1,1), endDate=datetime.datetime(2019, 12, 31))

# def negative_sharpe_n_minus_1_stock(weight):
#     weight2 = sp.append(weight, 1-sum(weight))
#     return -sharpe()

def objFunction(weight, ret, target_ret):
    stock_mean = np.mean(ret, axis = 0)
    port_mean = np.dot(weight, stock_mean)
    cov = np.cov(ret.T)
    port_var = np.dot(np.dot(weight, cov), weight.T)
    penalty = 2000*abs(port_mean-target_ret)
    return np.sqrt(port_var) + penalty


a = []
for ticker in tickers:
    _tmp = pd.read_pickle(ticker +'-2020')
    a.append(_tmp.iloc[:,8])
    #print(a)
y = pd.concat(a,axis=1)

monthly = [''.join([datetime.datetime.strptime(a, '%Y-%m-%d').strftime("%Y"),datetime.datetime.strptime(a, '%Y-%m-%d').strftime("%m")]) for a in y.index]
y['monthly']=monthly
y=y.replace(np.NaN,0)
retMonth = y.groupby(y.monthly).sum()
# print(retMonth)
covar = np.dot(retMonth.T,retMonth)
print(covar)
returns = weight*covar*weight.T
# print(returns)

out_mean,out_std,out_weight=[],[],[]
stockMean = np.mean(retMonth, axis=0)
# print(stockMean)
n_stock = len(tickers)
for r in np.linspace(np.min(stockMean), np.max(stockMean), num=100):
    weight = np.ones([n_stock])/n_stock
    # print(weight)
    b_ = [(0,1) for i in range(n_stock)]
    c_ = ({'type':'eq', 'fun': lambda weight : sum(weight) - 1.})
    result = sp.optimize.minimize(objFunction, weight, args=(retMonth, r), method='SLSQP', constraints=(c_),bounds=b_)
    if not result.success:
        BaseException(result.message)
    out_mean.append(round(r,4))
    std_=round(np.std(np.sum(retMonth*result.x, axis=1)), 6)
    out_std.append(std_)
    out_weight.append(result.x)

# print(out_weight)
print(out_weight[-1])

# print(out_std, out_mean)

plt.title('Efficient Frontier')
plt.xlabel('Standard Deviation of the Portfolio (Risk)')
plt.ylabel('Return of the Portfolio')
# plt.figtext(0.5,0.75, str(n_stock) + ' stock are used: ')
# plt.figtext(0.5,0.75, ' ' + str(tickers))
# plt.figtext(0.5,0.65, 'Time period')
plt.plot(out_std,out_mean, '--')
plt.show()