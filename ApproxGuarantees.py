import Simulation
import EpidemicControl
import sys
import networkx as nx
import Rounding
import time
import Baselines

#Compares performance of saaRound with baselines and provides approximation ratio
def compareAlgos(dataset, outputfile, p, exps, M, b, vaccfile, min_deg, freq_th, noBs):
   H = nx.Graph()
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
   G = []
   paths = []
   sources = []

   print("Generating Simulations")
   frequency = {}
   for i in range(0, M):
       print("Simulation ", i+1)
       graph, source = Simulation.generateDendograms(H, p, exps)
       G.append(graph)
       sources.append(source)
       for node in graph.nodes(): 
          if node in frequency:
             frequency[node] += 1
          else:
             frequency[node] = 0
       print("---------------------")

   avgnodes = 0
   for i in range(0, M):
       avgnodes += len(G[i].nodes)
   avgnodes = float(avgnodes)/M
   print("Average number of infections "+str(avgnodes))
   print("=====================================================")

   fw = open(outputfile, 'w')


   fw.write("given_budget,used_no_vaccines,no_action,saaRound_obj,degree_obj,evc_obj\n")  

   budgets = []
   for i in range(0, noBs):
       budgets.append(b+ b*i)
  
   for B in budgets:
       lpstart = time.time()
       m, x, y = EpidemicControl.LinearProgram(G, H, sources, B, frequency, min_deg, freq_th)
       nodesPicked, Infected, budget, infections, objValue, rtype = Rounding.rounding(m, x, y, N, M, N, B)

       print("Avg no infections "+str(float(infections)/M))
       fname = vaccfile+"_"+str(p)+"_"+str(exps)+"_"+str(B)+".csv"
       fp = open(fname, 'w')
       for node in nodesPicked:
           fp.write(node+"\n")
       fp.close()
       
       print("Budget "+str(budget))
       print("No of infections after intervention "+str(infections))
       avginfections = float(infections)/M
       print("Average no of infections "+str(avginfections))
       average_ai = EpidemicControl.ILinearProgram(G, sources, budget, nodesPicked)
       print("Actual average no of infections "+str(average_ai))
       
       lpend = time.time()
       lptime = lpstart-lpend
       print("SAAROUND time "+str(lptime))
       
       print("Degree baseline")
       topNodes_d = Baselines.degreebaseline(H, budget)
       print("top nodes degree "+str(topNodes_d))
       average_d = EpidemicControl.ILinearProgram(G, sources, budget, topNodes_d)
       print("Degree baseline average "+str(average_d))
    
       print("Eigenscore baseline")
       topNodes_es = Baselines.eigenbaseline(H, budget)
       average_es = EpidemicControl.ILinearProgram(G, sources, budget, topNodes_es)  
       print("Eigenscore baseline average "+str(average_es))

       fw.write(str(B)+","+str(budget)+","+str(avgnodes)+","+str(objValue)+","+str(average_d)+","+str(average_es)+"\n")
       

   fw.close()


if __name__ == "__main__":  
   dataset = sys.argv[1] #input the original dataset/graph name
   outputfile = sys.argv[2] #input the output file name for infections in each simulation
   p = float(sys.argv[3])
   exps = float(sys.argv[4])
   M = int(sys.argv[5])
   b = int(sys.argv[6])
   min_deg = int(sys.argv[7])
   freq_th = int(sys.argv[8])
  
   vaccfile = sys.argv[9]
   noBs = int(sys.argv[10])


   compareAlgos(dataset, outputfile, p, exps, M, b, vaccfile, min_deg, freq_th, noBs)
