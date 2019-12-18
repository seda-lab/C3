import os
import glob
import csv
import sys
from collections import Counter
import numpy as np
import scipy.stats as stats

from get_all_jobs import *

code_to_job = get_code_to_job();

code_to_dist = {}	
for fname in ["../db_24_0_text/Education, Training, and Experience.txt"]:
	with open(fname, 'r') as csvfile:
		csvreader = csv.reader(csvfile, delimiter='\t', quotechar='"')
		header = next(csvreader);
		hmap = { h:i for i,h in enumerate(header) }
		
		for row in csvreader:
			measurement = row[ hmap['Scale ID'] ];
			job = row[ hmap['O*NET-SOC Code'] ];

			if measurement == "RL":
				if job not in code_to_dist:
					code_to_dist[ job ] = {}
				code_to_dist[ job ][ int(row[ hmap['Category'] ]) ] = float( row[ hmap['Data Value'] ] )

use_jobs = {}
imps = []
for c in code_to_dist:
	degree_importance = sum( [ code_to_dist[c][i] for i in range(6,13)] )
	use_jobs[c] = degree_importance
	imps.append(degree_importance)
	
with open("degree_jobs.txt", 'w') as outfile:
	outfile.write("O*NET-SOC Code\tTitle\tImportance\n")
	for c in sorted( use_jobs, key=use_jobs.get, reverse=True ):
		outfile.write("{}\t{}\t{}\n".format(c, code_to_job[c], use_jobs[c]))
	

jobs, attributes, attribute_to_vector = get_all_jobs();
jobs = sorted(jobs)

degree_importance = [ use_jobs[c] for c in jobs ]
attrib_to_degree = {}
for a in attribute_to_vector:
	skill_importance = [ attribute_to_vector[ a ][ c ] for c in jobs  ]
	attrib_to_degree[a] = stats.pearsonr(skill_importance, degree_importance)[0]

with open("degree_attributes.txt", 'w') as outfile:
	outfile.write("Attribute\tCorrelation\n")
	for c in sorted( attrib_to_degree, key=attrib_to_degree.get, reverse=True ):
		outfile.write("{}\t{}\n".format(c, attrib_to_degree[c]))
	

