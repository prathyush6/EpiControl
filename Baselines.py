import networkx as nx
import sys
import collections
from collections import OrderedDict
from operator import itemgetter
import operator

#pick top B nodes as per degree
def degreebaseline(H, B): #H is the original graph
    degreeMap = {}

    for node in H.nodes():
        degreeMap[node] = H.degree(node)
    d = OrderedDict(sorted(degreeMap.items(), key=itemgetter(1), reverse=True))
    topNodes = set([])

    #obtain top B nodes
    i = 0
    for key in d:
        if i >= B:
           break
        topNodes.add(key)
        i = i+1
    return topNodes

#pick top B nodes as per eigenvector centrality
def eigenbaseline(H, B): #H is the original graph
    centrality = nx.eigenvector_centrality(H, max_iter = 1000)
    sorted_list = sorted(centrality.items(), key=operator.itemgetter(1), reverse = True)
    sorted_centrality = collections.OrderedDict(sorted_list)

    topNodes = set([])

    #obtain top B nodes
    i = 0
    for node in sorted_centrality.keys():
        if i >= B:
           break
        topNodes.add(node)
        i = i+1
    return topNodes                                         

if __name__ == "__main__": 
   H = nx.Graph()
   dataset = sys.argv[1]
   B = int(sys.argv[2])

   fr = open(dataset, 'r')
   lines = fr.readlines()
   for line in lines:
       cols = line.strip().split()
       v1 = cols[0]
       v2 = cols[1]
       H.add_edge(v1, v2)

   N = len(H.nodes()) # number of nodes in the graph
   print("Nodes "+str(N))
   print("Edges "+str(len(H.edges()))) 

   topNodes_d = degreebaseline(H, B)
   fname1 = "bter_deg_"+str(B)+".csv"
   fp = open(fname1, 'w')
   for node in topNodes_d:
       fp.write(str(node)+"\n")
   fp.close()
   print("top nodes degree "+str(topNodes_d))
   topNodes_es = eigenbaseline(H, B)
   fname2 = "bter_eig_"+str(B)+".csv"
   fq = open(fname2, 'w')
   for node in topNodes_es:
       fq.write(str(node)+"\n")
   fq.close()
   print("top nodes eigen "+str(topNodes_es))
