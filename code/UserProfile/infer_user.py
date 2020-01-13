import csv
import numpy as np
from utils import *
from dummy_user import get_dummy_user

##using coeffs to predict skills
#input is dict: {minset1 : X, minset2 : X, ... }
#output is dict: {minset1 : X, minset2 : X, ... , inferred1 : X, ...}
#Xs are scaled between 0 and 5
def infer_user(userin): 
	coeffs = {}
	with open("fit_params.csv", 'r') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		header = next(csvreader);
		hmap = { h:i for i,h in enumerate(header) }

		for row in csvreader:
			coeffs[ row[0] ] = ( float(row[1]) ,  [float(r) for r in row[2:]] )
		
	uarray = [ userin[a] for a in get_minset() ]; ##has to read in correct order, hence get_minset()
	user = { a:userin[a] for a in userin }
	for s in coeffs:
		user[s] = coeffs[s][0] + np.dot(coeffs[s][1], uarray)
	return user

if __name__ == "__main__":
	##dummy user
	user = get_dummy_user("Choreographers") 
	print(user)
	print( infer_user(user) )



