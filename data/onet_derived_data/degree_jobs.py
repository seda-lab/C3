import pandas as pd
import os
import glob
import csv
import sys
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import SpectralClustering
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score

from scipy import stats


code_to_job = {}
job_to_code = {}
for fname in ["../db_24_0_text/Occupation Data.txt"]:
	with open(fname, 'r') as csvfile:
		csvreader = csv.reader(csvfile, delimiter='\t', quotechar='"')
		header = next(csvreader);
		hmap = { h:i for i,h in enumerate(header) }
		
		for row in csvreader:
			code_to_job[ row[0] ] = row[1]

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


threshold=50
use_jobs = {}
imps = []
for c in code_to_dist:
	degree_importance = sum( [ code_to_dist[c][i] for i in range(6,13)] )
	use_jobs[c] = degree_importance
	imps.append(degree_importance)
	
with open("degree_jobs.txt".format(threshold), 'w') as outfile:
	outfile.write("O*NET-SOC Code\tTitle\tImportance\n")
	for c in sorted( use_jobs, key=use_jobs.get, reverse=True ):
		outfile.write("{}\t{}\t{}\n".format(c, code_to_job[c], use_jobs[c]))
	


attribute_to_vector = {}
attributes = set();
jobs = set();
for fname in ["../db_24_0_text/Work Context.txt", "../db_24_0_text/Work Activities.txt", "../db_24_0_text/Knowledge.txt", "../db_24_0_text/Skills.txt","../db_24_0_text/Abilities.txt" ]:
	with open(fname, 'r') as csvfile:
		csvreader = csv.reader(csvfile, delimiter='\t', quotechar='"')
		header = next(csvreader);
		hmap = { h:i for i,h in enumerate(header) }

		for row in csvreader:
			attribute = row[ hmap['Element Name'] ];
			job = row[ hmap['O*NET-SOC Code'] ];
			if job == "15-2091.00": continue
			jobs.add(job)
			attributes.add(attribute);

			if row[ hmap['Scale ID'] ] == "IM" or row[ hmap['Scale ID'] ] == "CX":
				if attribute not in attribute_to_vector:
					attribute_to_vector[ attribute ] = {}
				attribute_to_vector[ attribute ][ job ] = float( row[ hmap['Data Value'] ] )

jobs = sorted(jobs)
degree_importance = [ use_jobs[c] for c in jobs ]
attrib_to_degree = {}
for a in attribute_to_vector:
	skill_importance = [ attribute_to_vector[ a ][ c ] for c in jobs  ]
	attrib_to_degree[a] = stats.pearsonr(skill_importance, degree_importance)[0]

with open("degree_skills.txt".format(threshold), 'w') as outfile:
	outfile.write("Attribute\tCorrelation\n")
	for c in sorted( attrib_to_degree, key=attrib_to_degree.get, reverse=True ):
		outfile.write("{}\t{}\n".format(c, attrib_to_degree[c]))
	

