import statsmodels.api as sm
from statsmodels.stats import outliers_influence
from statsmodels.compat import lzip
import statsmodels.stats.api as sms

import pandas
from patsy import dmatrices
import pprint


df = sm.datasets.get_rdataset("Guerry", "HistData").data


vars = ['Department', 'Lottery', 'Literacy', 'Wealth', 'Region']

df = df[vars]
df = df.dropna()


y, X = dmatrices('Lottery ~ Literacy + Wealth + Region', data=df, return_type='dataframe')

#print(y)
print(X)
print(X.iloc[:, 0])
print(X.iloc[:, 1])

mod = sm.OLS(y, X) 
res = mod.fit() 

print(res.summary())

print(res.params)

print(res.cov_params())

print(sm.stats.linear_rainbow(res))

print('----------------------')

pprint.pprint(dir(res))
pprint.pprint(dir(res.model))

#pprint.pprint(res.__dict__)

#print(sm.stats.linear_rainbow.__doc__)
#print(sm.OLS.__doc__)


print('Durbin Watson: ', sm.stats.stattools.durbin_watson(res.resid, axis=0))


#sm.graphics.plot_partregress('Lottery', 'Wealth', ['Region', 'Literacy'], data=df, obs_labels=False)


name = ['Lagrange multiplier statistic', 'p-value', 
        'f-value', 'f p-value']

test = sms.het_breuschpagan(res.resid, res.model.exog)
pprint.pprint(lzip(name, test))





print(outliers_influence.variance_inflation_factor(X.values, 5))