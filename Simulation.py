import networkx as nx
#import matplotlib.pyplot as plt
import random
import sys

def generateDendogram(): 
    G = nx.Graph()
    filename= sys.argv[1]
    print(filename)
    G=nx.read_adjlist(filename)
    
    #create a random edge subgraph
    Gp = nx.Graph()

    s = -1 #super source

    sources = []
    
    while(len(sources) == 0):
         for node in G.nodes():
             r = random.random()
             p = 0.01
             if r <= p:
               sources.append(node)

    #connect sources to the super source
    for node in sources:
        G.add_edge(s, node)

    p = 0.3  #probability for an edge in contact graph to be picked
    for edge in G.edges():
        r = random.random()
        v1 = int(edge[0])
        v2 = int(edge[1])
        if r <= p:
           Gp.add_edge(v1, v2)

    source = s
    T = nx.bfs_tree(Gp, source)
    
    level = nx.single_source_shortest_path_length(T,source)

    for edge in Gp.edges():
        v1 = int(edge[0])
        v2 = int(edge[1])
        if v1 in level and v2 in level:
           if level[v1] > level[v2]:
              T.add_edge(v2, v1)
           elif level[v2] > level[v1]:
              T.add_edge(v1, v2)

    nodes = []
    for node in T.nodes():
        nodes.append(node)
        
    #compute the levels of nodes in the random subgraph
    levels = {}
    for node in nodes:
        l = level[node]
        if l in levels:
           levels[l].add(node)
        else:
           levels[l] = set([node])
   
    fw = open('DiseaseInfo', 'w')
    for key in sorted(levels.keys()):
        if key == 0:
           continue
        row = ""
        print(key)
        for element in levels[key]:
            row += str(element)+","
        row = row[:-1]
        fw.write(row+"\n")
    return source, levels

def generateDendograms(G, p, exps): # to generate simulations of the disease spread with no information; p edge prob; sp source prob
    N = len(G)

    s = -1 #super source
    #each node has a prob p to become source
   
    sources = [] 
    while(len(sources) <= 0):
         for node in G.nodes():
             r = random.random()
             sp = exps/float(N)
             if r <= sp:
               sources.append(node)
    print("#sources ", len(sources))

    Gp = nx.Graph()

    #each edge is picked with prob p
    for edge in G.edges():
        r = random.random()
        v1 = edge[0]
        v2 = edge[1]
        if r <= p:
           Gp.add_edge(v1, v2)
    
    Gp.add_node(s) 
    for node in sources:
        Gp.add_edge(s, node)  
 
    
    T = nx.bfs_tree(Gp, s)
    #level = nx.single_source_shortest_path_length(T,s)
    T.remove_node(s)
    H = nx.Graph()

    for node in sources:
        H.add_node(node)
 
    nodeset = set()
    for node in T.nodes():
        nodeset.add(node)
    
    for edge in T.edges():
        v1 = edge[0]
        v2 = edge[1]
        H.add_edge(v1, v2)
      
    #print("done here")
    for edge in Gp.edges():
        v1 = edge[0]
        v2 = edge[1]
        if v1 in nodeset and v2 in nodeset:
           H.add_edge(v1, v2)
    #print("done here")    
    #paths = {}
    #pcount = 0
    #for node in H.nodes():
    #    if node in sources:
    #       continue
    #    temp = []
    #    #print(node)
    #    for node1 in sources:
            #print("source "+str(node1))
            #pathlist = nx.all_simple_paths(H, node1, node)
    #        for path in nx.all_simple_paths(H, node1, node):
    #            temp.append(path)
    #            pcount += 1
                #print(path)
                #print(pcount)
    #    paths[node] = temp
    
    #return T, sources, paths, level, inedges
    #graph, source = Simulation.generateDendograms(H, p, exps)
    print("#infections ", len(H.nodes()))
    print("#edges ", len(H.edges()))
    #print("#paths ", pcount)
    return H, sources
   

def generateDendogramsTest(G, p, exps, vaccNodes): # to generate simulations of the disease spread with no information; p edge prob; sp source prob
    N = len(G)

    s = -1 #super source
    #each node has a prob p to become source

    sources = []
    while(len(sources) <= 0):
         for node in G.nodes():
             r = random.random()
             sp = exps/float(N)
             if r <= sp:
               sources.append(node)
    print("#sources ", len(sources))

    Gp = nx.Graph()

    #each edge is picked with prob p
    for edge in G.edges():
        r = random.random()
        v1 = edge[0]
        v2 = edge[1]
        if r <= p:
           Gp.add_edge(v1, v2)

    Gp.add_node(s)
    for node in sources:
        Gp.add_edge(s, node)


    T = nx.bfs_tree(Gp, s)
    #level = nx.single_source_shortest_path_length(T,s)
    T.remove_node(s)
    H = nx.Graph()

    for node in sources:
        H.add_node(node)
    
    nodeset = set()
    for node in T.nodes():
        nodeset.add(node)

    for edge in T.edges():
        v1 = edge[0]
        v2 = edge[1]
        H.add_edge(v1, v2)

    #print("done here")
    for edge in Gp.edges():
        v1 = edge[0]
        v2 = edge[1]
        if v1 in nodeset and v2 in nodeset:
           H.add_edge(v1, v2)

    print("#infections ", len(H.nodes()))
    print("#edges ", len(H.edges()))
    #print("#paths ", pcount)
    return H, sources

#used only for categorizing the probabilities for each graph
def generateDendogramsprob(graphname, sp, p): # to generate simulations of the disease spread with no information; p edge prob; sp source prob
    #print(sp)
    G = nx.Graph()
    G = nx.read_adjlist(graphname)

    levels = {}
    s = -1 #super source
    #G.add_node(s)

    #each node has a prob p to become source
    sources = []
    for node in G.nodes():
        r = random.random()
        if r <= sp:
           sources.append(node)
    print("# Sources ", len(sources))

    #add the sources to the super source
    for node in sources:
        G.add_edge(s, node)

    Gp = nx.Graph()

    #each edge is picked with prob p
    for edge in G.edges():
        r = random.random()
        v1 = int(edge[0])
        v2 = int(edge[1])
        if r < p and s != v1 and s != v2:
           Gp.add_edge(v1, v2)
        elif s == v1 or s == v2:
           Gp.add_edge(v1, v2)

    T = nx.bfs_tree(Gp, s)
    T.remove_node(s)
    #print("# nodes ", len(T.nodes()))
    
    return T


def generateDendograms1(graphname, diseaseInfo, L): #all nodes with levels <= L are infected; those at 0 are sources
    G = nx.Graph()
    #pirint(graph)
    G=nx.read_adjlist(graphname)

    fp = open(diseaseInfo, 'r')
    lines = fp.readlines()
    levels = {}
    infected = {}
    l = 0
    for line in lines:
        if l > L:
           break
        cols = line.strip().split(",")
        levels[l] = set([])
        for node in cols:
            levels[l].add(node)
            if l < L:
               G.remove_node(node) #remove
               infected.add(node)
        l = l+1

    s = -1
    nodes = []
    for node in G.nodes():
        nodes.append(node)

    #print(l)
    #print(levels[l-1])

    sources = []
    if L >= 0:
       for node in levels[L]:
           sources.append(node)
    else:
       for node in G.nodes():
           r = random.random()
           if r <= 0.002:
              sources.append(node)
    for node in sources:
        G.add_edge(s, node)

    Gp = nx.Graph()

    p = 0.15
    for edge in G.edges():
        r = random.random()
        v1 = int(edge[0])
        v2 = int(edge[1])
        if r < p and s != v1 and s != v2:
           Gp.add_edge(v1, v2)
        elif s == v1 or s == v2:
           Gp.add_edge(v1, v2)


    T = nx.bfs_tree(Gp, s)
    level = nx.single_source_shortest_path_length(T,s)

    #print(level)
    T.remove_node(s)
    level.pop(s)

    for edge in Gp.edges():
    #print(edge)
        v1 = int(edge[0])
        v2 = int(edge[1])
        if v1 in level and v2 in level:
           if level[v1] > level[v2]:
              T.add_edge(v2, v1)
           elif level[v2] > level[v1]:
              T.add_edge(v1, v2)

    paths = {}
    #print(sources)
    for node in T:
        temp = []
        for node1 in sources:
            for path in nx.all_simple_paths(T, source = int(node1), target = node):
                temp.append(path)

    for key in level.keys():
        offset = L
        if L < 0:
           offset = 0
        level[key] = level[key] -1 + L

    for node in infected:
        level[node] = levels[node]
    
    return T, paths, level

if __name__ == "__main__":
   filename = sys.argv[1]
   p = float(sys.argv[2])
   exps= int(sys.argv[3])
   M = int(sys.argv[4])
   nodefile = sys.argv[5]
   outfile = sys.argv[6]

   H = nx.Graph()
   fr = open(filename, 'r')
   lines = fr.readlines()
   for line in lines:
       cols = line.strip().split()
       v1 = cols[0]
       v2 = cols[1]
       H.add_edge(v1, v2)

   #fp = open(nodefile, 'r')
   #lines = fp.readlines()
   fr = open(outfile, 'a')
   print("No. of nodes before "+str(len(H.nodes())))
   
   avginf_b = 0.0
   strout = ""
   
   for i in range(0, M):
       print("Simulation "+str(i+1)+"\n")
       G, sources = generateDendograms(H, p, exps)
       print(len(G.nodes()))
       strout += str(float(len(G.nodes())/25.00))+","
       avginf_b += len(G.nodes())
       print("----------------------\n")
   avginf_b = avginf_b/M
   nodes_b = len(H.nodes())
   strout = strout[:-1]
   fr.write(strout+"\n")
   #print("Average infections before "+str(avginf_b))
   #print("Total population "+str(nodes_b))
  
   #fr = open(outfile, 'a')
   B = [20,40,60,100,120,140]    
   for b in B:
       print("Budget "+str(b))
       H_t = nx.Graph()
       for edge in H.edges():
           v1 = edge[0]
           v2 = edge[1]
           H_t.add_edge(v1, v2)
       fp = open(nodefile+"_"+str(b)+".csv", 'r')
       lines = fp.readlines()
 
       for line in lines:
           H_t.remove_node(line.strip())
       print("No. of nodes after "+str(len(H.nodes())))
       avginf_a = 0.0

       #fr = open(outfile, 'a')
       strout = ""
       for i in range(0, M):
           print("Simulation "+str(i+1)+"\n")
           G, sources = generateDendograms(H_t, p, exps)
           print(len(G.nodes()))
           strout += str(float(len(G.nodes())/25.00))+","
           avginf_a += len(G.nodes())
           print("----------------------\n")
       strout = strout[:-1]
       fr.write(strout+"\n")
       #fr.close()
       avginf_a = avginf_a/M
       nodes_a = len(H_t.nodes())
       print("Average infections before "+str(avginf_b))
       print("Total population "+str(nodes_b))
       print("Average infections after "+str(b)+" interventions "+str(avginf_a))
       print("Total population "+str(nodes_a))
    
