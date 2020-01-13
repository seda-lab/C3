import csv
import numpy as np
from utils import *
from dummy_user import get_dummy_user
from infer_user import infer_user
from scipy.spatial.distance import cosine
from scipy.spatial.distance import euclidean

def best_matching_jobs(user):
	
	jobs = get_jobs();
	degree_jobs = set(get_degree_jobs())
	attributes = get_attributes();
	ja = get_ja_matrix();

	uarray = np.array([ user[a] for a in attributes ]);
	similarity = {}
	for jid, j in enumerate(jobs):
		if j in degree_jobs:
			similarity[ code_to_job(j) ] = cosine(uarray, ja[jid, :])

	return [ (j,similarity[j]) for j in sorted(similarity, key=similarity.get) ]

def best_matching_jobs_noinference(user):
	
	jobs = get_jobs();
	degree_jobs = set(get_degree_jobs())
	attributes = get_attributes();
	minset = get_minset();
	minset_idx = [ attributes.index(m) for m in minset ]
	ja = get_ja_matrix();

	uarray = np.array([ user[a] for a in minset ]);
	similarity = {}
	for jid, j in enumerate(jobs):
		if j in degree_jobs:
			similarity[ code_to_job(j) ] = cosine(uarray, ja[jid, minset_idx])

	return [ (j,similarity[j]) for j in sorted(similarity, key=similarity.get) ]
	
		
if __name__ == "__main__":
	##dummy user
	dummy="Computer Network Architects"
	du = get_dummy_user(dummy) 
	user = infer_user(du)
	
	print("For the dummy user (", dummy, ")")
	print("The top 5 job matches are:")
	for s in best_matching_jobs(user)[:5]:
		print(s)
		

