import csv
import sys
import numpy as np

attribute_to_vector = {}
attributes = set();
jobs = set();
for fname in ["db_24_0_text/Work Styles.txt", "db_24_0_text/Work Context.txt", "db_24_0_text/Work Activities.txt", "db_24_0_text/Knowledge.txt", "db_24_0_text/Skills.txt","db_24_0_text/Abilities.txt" ]:
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
				
with open("attributes.txt", 'w') as outfile:
	for a in attributes:
		outfile.write(a + "\n");

with open("jobs.txt", 'w') as outfile:
	for j in jobs:
		outfile.write(j + "\n");
		
with open("job_attribute_matrix.txt", 'w') as outfile:
	csvwriter = csv.writer(outfile, delimiter=" ")
	for j in jobs:
		csvwriter.writerow( [attribute_to_vector[a][j] for a in attributes] )
			


