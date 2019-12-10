import csv
import numpy as np

##dummy user
np.random.seed(123456789)
minset = ["analyzing data or information", "thinking creatively", "active learning", "complex problem solving", 
"mathematical reasoning", "flexibility of closure", "written expression", "speaking", 
"interpreting the meaning of information for others", "establishing and maintaining interpersonal relationships", 
"negotiation", "coordination", "updating and using relevant knowledge", "integrity", "initiative", "self control", 
"achievement/effort", "independence", "leadership", "provide consultation and advice to others", "training and teaching others", 
"organizing, planning, and prioritizing work", "coordinating the work and activities of others", "time management"]
user = np.array([np.random.uniform(1,5) for s in minset])

##read coeffs
coeffs = {}
with open("fit_params.csv", 'r') as csvfile:
	csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
	header = next(csvreader);
	hmap = { h:i for i,h in enumerate(header) }

	for row in csvreader:
		coeffs[ row[0] ] = ( float(row[1]) ,  [float(r) for r in row[2:]] )

for s in coeffs:
	print(s, coeffs[s][0] + np.dot(coeffs[s][1], user) )
