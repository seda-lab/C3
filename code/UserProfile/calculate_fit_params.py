import csv
import sys
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from utils import *

threshold = 50;

attributes = get_attributes()	
A = len(attributes)
degree_jobs = get_degree_jobs(threshold=threshold);
J = len(degree_jobs)
minset = get_minset();
minset_idx = [ attributes.index(m) for m in minset ]

estimate = np.zeros( (A,J) )
data = get_degree_ja_matrix().transpose()
xdata = data[minset_idx, :].transpose()


Rsquared = {}
coeffs = {}
pred = {}
for sid, s in enumerate(attributes):
	if sid not in minset_idx:
		ydata = data[sid,:]
		reg = LinearRegression().fit(xdata, ydata)
		Rsquared[s] = reg.score(xdata, ydata)
		coeffs[s] = (   reg.intercept_, np.array(list(reg.coef_))  )
		pred[s] = reg;

plt.hist( list(Rsquared.values()), 30, density=True )
plt.xlabel("$R^2$")
plt.ylabel("$P(R^2)$")
plt.savefig("RsquaredHist.png")
plt.close();

		
with open("attributes_rsquared.csv", 'w') as csvfile:
	csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
	row = ["Attribute", "R2"]	
	csvwriter.writerow(row)	
	for s in sorted(Rsquared, key=Rsquared.get, reverse=True):
		csvwriter.writerow([s, Rsquared[s]])
	

with open("fit_params.csv", 'w') as csvfile:
	csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
	row = ["Attribute", "Const"] + minset	
	csvwriter.writerow(row)	
	for s in coeffs:
		csvwriter.writerow([s, coeffs[s][0]] + list(coeffs[s][1]))


