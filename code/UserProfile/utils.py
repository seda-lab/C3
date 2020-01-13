import numpy as np
import csv

def get_attributes():
	attributes = []
	with open("attributes.txt", 'r') as infile:
		for line in infile:
			attributes.append( line.strip() );
	return attributes

def get_jobs():
	jobs = []
	with open("jobs.txt", 'r') as infile:
		for line in infile:
			jobs.append( line.strip() );
	return jobs

code_to_job_dict = {}
job_to_code_dict = {}
with open("../../data/db_24_0_text/Occupation Data.txt", 'r') as infile:
	csvreader=csv.reader(infile, delimiter="\t");
	next(csvreader)
	for row in csvreader:
		code_to_job_dict[ row[0] ] = row[1]
		job_to_code_dict[row[1]] = row[0]

def job_to_code(job): 
	if job in job_to_code_dict:
		return job_to_code_dict[job];
	return None
	
def code_to_job(code): 
	if code in code_to_job_dict:
		return code_to_job_dict[code]
	return None
	

def get_ja_matrix():
	return np.loadtxt("job_attribute_matrix.txt")

def get_minset():
	attributes = get_attributes()
	minset = []
	with open("minset.txt", 'r') as infile:
		for line in infile:
			if line.strip() in attributes:
				minset.append( line.strip() );
			else:
				print(line, "is not an O*Net attribute")
	return minset


def get_degree_jobs(threshold=50):
	degree_jobs = []
	with open("degree_jobs.txt", 'r') as infile:
		csvreader = csv.reader(infile, delimiter="\t")
		next(csvreader)
		for row in csvreader:
			if float(row[2]) >= threshold:
				degree_jobs.append( row[0] );
			
	return degree_jobs
	
def get_degree_ja_matrix(threshold=50):
	degree_jobs = get_degree_jobs(threshold);
	jobs = get_jobs();
	ja_matrix = get_ja_matrix();
	X = []	
	for i,j in enumerate(jobs):
		if j in degree_jobs:
			X.append( ja_matrix[i,:] )
	return np.array(X)

