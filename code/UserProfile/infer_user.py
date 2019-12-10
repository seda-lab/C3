import csv
import sys
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

attribute_to_vector = {}
attributes = set();
jobs = set();
for fname in ["../../data/db_24_0_text/Work Styles.txt", "../../data/db_24_0_text/Work Context.txt", "../../data/db_24_0_text/Work Activities.txt", "../../data/db_24_0_text/Knowledge.txt", "../../data/db_24_0_text/Skills.txt","../../data/db_24_0_text/Abilities.txt" ]:
	with open(fname, 'r') as csvfile:
		csvreader = csv.reader(csvfile, delimiter='\t', quotechar='"')
		header = next(csvreader);
		hmap = { h:i for i,h in enumerate(header) }

		for row in csvreader:
			attribute = row[ hmap['Element Name'] ].lower();
			job = row[ hmap['O*NET-SOC Code'] ].lower();
			jobs.add(job)
			attributes.add(attribute);

			if row[ hmap['Scale ID'] ] == "IM" or row[ hmap['Scale ID'] ] == "CX":
				if attribute not in attribute_to_vector:
					attribute_to_vector[ attribute ] = {}
				imp = float( row[ hmap['Data Value'] ] );
				attribute_to_vector[ attribute ][ job ] = imp


attributes = sorted( list(attribute_to_vector.keys()) );
for s in attributes:
	if len(attribute_to_vector[s]) != len(jobs):
		for j in jobs:
			if j not in attribute_to_vector[s]:
				attribute_to_vector[s][j] = 0;

jobs = sorted(jobs)
S = len(attributes)
J = len(jobs)

data = []
for s in attributes:
	data.append( [ attribute_to_vector[s][j] for j in jobs ] )
data = np.array(data)		

minset = ["analyzing data or information", "thinking creatively", "active learning", "complex problem solving", 
"mathematical reasoning", "flexibility of closure", "written expression", "speaking", 
"interpreting the meaning of information for others", "establishing and maintaining interpersonal relationships", 
"negotiation", "coordination", "updating and using relevant knowledge", "integrity", "initiative", "self control", 
"achievement/effort", "independence", "leadership", "provide consultation and advice to others", "training and teaching others", 
"organizing, planning, and prioritizing work", "coordinating the work and activities of others", "time management"]
minset_idx = [ attributes.index(m) for m in minset ]

estimate = np.zeros( (S,J) )

x = minset_idx
xdata = data[x,:].transpose()


Rsquared = {}
coeffs = {}
pred = {}
for sid, s in enumerate(attributes):
	if sid not in x:
		ydata = data[sid,:]
		#print(xdata.shape, ydata.shape)
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


