import os
import glob
import csv
import sys
from collections import Counter
import numpy as np
import scipy.stats as stats
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
from get_all_jobs import *
import math

	
code_to_job = get_code_to_job();
jobs, attributes, attribute_to_vector = get_all_jobs();
jobs = sorted(jobs)
attributes = sorted(attributes)

job_threshold = 50;
attribute_threshold = 0;
rca_threshold = 1;
edge_threshold = 0.7
visible_edge_threshold = 0.7

degree_jobs = set();
with open("degree_jobs.txt", 'r') as csvfile:
	csvreader = csv.reader(csvfile, delimiter='\t', quotechar='"')
	header = next(csvreader);
	for row in csvreader:
		if float(row[2]) >= job_threshold:
			degree_jobs.add( row[0] );

degree_attributes = set();
with open("degree_attributes.txt", 'r') as csvfile:
	csvreader = csv.reader(csvfile, delimiter='\t', quotechar='"')
	header = next(csvreader);
	for row in csvreader:
		if float(row[1]) > attribute_threshold:
			degree_attributes.add( row[0] );

print(len(degree_jobs), len(degree_attributes))

norm = 0
for j in degree_jobs:
	for s in degree_attributes:
		norm += attribute_to_vector[s][j]

jvec = Counter()
for j in degree_jobs:
	for s in degree_attributes:
		jvec[j] += attribute_to_vector[s][j]
	
svec = Counter();			
for s in degree_attributes:
	for j in degree_jobs:
		svec[s] += attribute_to_vector[s][j]

rca = {}	
B = nx.Graph()	
for j in degree_jobs:
	rca[j] = {}
	for s in degree_attributes:			
		rca[j][s] = (attribute_to_vector[s][j]/jvec[j])/(svec[s]/norm);
		if rca[j][s] > rca_threshold:
			B.add_node(j, bipartite=0)
			B.add_node(s, bipartite=1)
			B.add_edge(j, s, weight=1)

G  = bipartite.weighted_projected_graph(B, [j for j in jobs if B.has_node(j)] )
print(len(G.nodes()), len(G.edges()))
#ews = []
for u, v in G.edges():
	G[u][v]["weight"] = G[u][v]["weight"] / max( B.degree[u], B.degree[v] )
#	ews.append( G[u][v]["weight"])
#plt.hist(ews, bins=100, density=True, alpha=0.5, cumulative=True)
#plt.savefig("attribute_ews.png");
#plt.show();
#plt.close();	

H = nx.Graph();
elist = []
nlist = set();
for u, v in G.edges():
	if G[u][v]["weight"]  > edge_threshold:
		H.add_edge(u, v, weight=G[u][v]["weight"])
	if G[u][v]["weight"]  > visible_edge_threshold:
		elist.append( (u,v) )
		nlist.add(u)
		nlist.add(v)
nlist = list(nlist)

plt.figure(figsize=(40,40))		
pos = nx.spring_layout(H, seed=123456, k=4/math.sqrt(H.size()))
nx.draw_networkx_nodes(H, pos=pos, node_size=30, nodelist=nlist)
nx.draw_networkx_edges(H, pos=pos, edgelist=elist, alpha=0.5)
nx.draw_networkx_labels(H, pos=pos, labels={ n:code_to_job[n] for n in nlist } )
plt.savefig("DegreeJobNetwork.png")


