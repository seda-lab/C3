import csv
import sys



job_to_code = {}
for fname in ["../db_24_0_text/Occupation Data.txt"]:
	with open(fname, 'r') as csvfile:
		csvreader = csv.reader(csvfile, delimiter='\t', quotechar='"')
		header = next(csvreader);
		hmap = { h:i for i,h in enumerate(header) }
		
		for row in csvreader:
			job_to_code[ row[1].lower() ] = row[0]

dwp_jobs = set()
for fname in ["../sheffield_data/jr_skills_percents_Nov19.csv"]:
	with open(fname, 'r') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		header = next(csvreader);
		hmap = { h:i for i,h in enumerate(header) }
		
		for row in csvreader:
			dwp_jobs.add( row[0].lower() )
	
with open("dwp_onet_jobs.csv", 'w') as csvfile:
	csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
	row = ["DWP", "ONET", "SOC-CODE"]	
	csvwriter.writerow(row)	
	
	for dwp_j in dwp_jobs:
		for t in dwp_j.split():
			for onet_j in job_to_code:
				for s in onet_j.split():
					if s == t:
						csvwriter.writerow([dwp_j, onet_j, job_to_code[onet_j]])	

	
				
			
