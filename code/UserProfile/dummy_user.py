import csv
import sys
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from utils import *

def get_dummy_user(jobtitle):

	code = ""
	if job_to_code(jobtitle):
		code = job_to_code(jobtitle);
	else:
		print(jobtitle, "in not in O*Net")
		sys.exit(1);
		
	jobs = get_jobs(); 
	job = jobs.index(code);	
	attributes = get_attributes()	
	ja = get_ja_matrix();

	return { m:ja[job,attributes.index(m)] for m in get_minset()}
	
#print( get_dummy_user("Choreographers") )
	


