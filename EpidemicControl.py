from networkx import nx
import sys
import Simulation
from gurobipy import *
import math
import random

#Single Stage LP
def LinearProgram(G, H, sources, B, frequency, min_deg, freq_th):
   x = {} #x_{u0} is indicator if node u is vaccinated
   y = {} #y_{vj} is indicator if node v is reachable from src(H_j) in sample H_j
   M = len(G) #number of samples 
  
   m = Model('1STAGE-EPICONTROL')
 
   #define x and y variables
   for j in range(0, M):
       for u in G[j]:
           if u not in x:
              x[str(u)] = m.addVar(vtype = GRB.CONTINUOUS, lb = 0.0, ub = 1.0, name = "x["+str(u)+"]")
              if H.degree(u) <= min_deg:
                 m.addConstr(x[str(u)] == 0, name = "C01"+str(u))
              elif frequency[u] <= freq_th *M:
                 m.addConstr(x[str(u)] == 0, name = "C00"+str(u))
           y[str(u)+","+str(j)] = m.addVar(vtype = GRB.CONTINUOUS, lb = 0.0, ub = 1.0, name = "y["+str(u)+","+str(j)+"]")

   #constraints (2) and (4) in paper
   for j in range(0, M):
       for u in G[j]:
           #a node u in sample j can not be infected if it is vaccinated.  
           m.addConstr(y[str(u)+","+str(j)] <= 1 - x[str(u)], name = "C2("+str(j)+","+str(u)+")")
           if u in sources[j]:
              #source s in sample j is infected if it is not vaccinated. And is uninfected if it is vaccinated.
              m.addConstr(y[str(u)+","+str(j)] == 1 - x[str(u)], name = "C4("+str(j)+","+str(u)+")")
 
   #vconstraint (5) : budget 
   m.addConstr(quicksum(x[str(u)] for u in x) <= B, name = "C5,budget")

   #edge constraint
   for j in range(0, M):
       for u in G[j]:
           for w in G[j].neighbors(u):
               m.addConstr(y[str(u)+","+str(j)] >= y[str(w)+","+str(j)] - x[str(u)], name = "C3("+str(j)+","+str(u)+","+str(w)+")")

   #objective function
   m.setObjective(quicksum(y[str(u)+","+str(j)] for j in range(0, M) for u in G[j])/M, GRB.MINIMIZE)
   m.update()
   m.optimize()
   return m, x, y 

#Integer Program
def ILinearProgram(G, sources, B, vaccNodes):
   x = {} #x_{u0} is indicator if node u is vaccinated
   y = {} #y_{vj} is indicator if node v is reachable from src(H_j) in sample H_j
   M = len(G) #number of samples

   m = Model('1STAGE-EPICONTROL')

   #define x and y variables
   for j in range(0, M):
       for u in G[j]:
           if u not in x:
              x[str(u)] = m.addVar(vtype = GRB.BINARY, name = "x["+str(u)+"]")
              
           y[str(u)+","+str(j)] = m.addVar(vtype = GRB.BINARY, name = "y["+str(u)+","+str(j)+"]")

   for node in vaccNodes:
       if str(node) not in x:
          x[str(node)] = m.addVar(vtype = GRB.BINARY, name = "x["+str(node)+"]")
       m.addConstr(x[str(node)] == 1, name = "C5 "+str(node))
   
   #constraints (2) and (4) in paper
   for j in range(0, M):
       for u in G[j]:
           #a node u in sample j can not be infected if it is vaccinated.
           m.addConstr(y[str(u)+","+str(j)] <= 1 - x[str(u)], name = "C2("+str(j)+","+str(u)+")")
           if u in sources[j]:
              #source s in sample j is infected if it is not vaccinated. And is uninfected if it is vaccinated.
              m.addConstr(y[str(u)+","+str(j)] == 1 - x[str(u)], name = "C4("+str(j)+","+str(u)+")")


   #edge constraint
   for j in range(0, M):
       for u in G[j]:
           for w in G[j].neighbors(u):
               m.addConstr(y[str(u)+","+str(j)] >= y[str(w)+","+str(j)] - x[str(u)], name = "C3("+str(j)+","+str(u)+","+str(w)+")")

   m.addConstr(quicksum(x[u] for u in x) <= B, name = "C5,budget")
   #objective function
   m.setObjective(quicksum(y[str(u)+","+str(j)] for j in range(0, M) for u in G[j])/M, GRB.MINIMIZE)
   m.update()
   m.optimize()
   
   return m.objVal

#main function
if __name__ == "__main__":
   dataset = sys.argv[1] #input the original dataset/graph name
   outputfile = sys.argv[2] #input the output file name

   H = nx.Graph()
   H = nx.read_adjlist(dataset)
   N = len(H.nodes()) # number of nodes in the graph
 
   #M = int(sys.argv[3]) #input the number of simulations
   B = int(sys.argv[3]) #input the budget 
   
   G = []
   paths = []
   levels = [] 
   sources = []
   inedges = []
 
   #generate M simulations 
   print("Generating Simulations")
   exps = 3 #expected number of sources = 10
   p = 0.11
   for i in range(0, 2):
       print("Simulation ", i+1)
       graph, path, source = Simulation.generateDendograms(H, p, exps)
       G.append(graph)
       paths.append(path)
       sources.append(source)
      
   m, x, y = LinearProgram(G, H, sources, B)
   
   

