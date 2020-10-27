import EpidemicControl
import sys
import random
import math

def rounding(m, x, y, n, M, N, B):
    print("Given budget "+str(B))
    Y = {} #rounded values of y variables
    X = {} #rounded values of x variables
    Xrounds = []
    #print(x)
    #print(y)
    #m.optimize()
    #round iY values deterministically
    fracyvalues = {}
    nonfracyvalues = {}
    fracxvalues = {}
    nonfracxvalues = {}
    for key, gv in y.items():
        val = gv.X
        if val == 1.0 or val == 0.0:
           nonfracyvalues[key] = val
        else:
           fracyvalues[key] = val
           #print("y "+str(val))
        if val >= 0.5:
           Y[key] = 1
        else:
           Y[key] = 0

    #round X values probabilistically; pick the rounding that is most practical for the instance; difference from the factor used to obtain theoretical guarantee 
    best = n*1000 #test
    best_i = -1
    best_p = n*1000
    current_rval = 2 *math.log(4*n*M*N)
    current_r = 'r1'
    best_rs = 'r1'
    
    for i in range(0, 1000):
        if i == 201:
           current_rval = math.log(n)
           current_r = 'r2'
        elif i == 401:
           current_rval = 8
           current_r = 'r3'
        elif i == 601:
           current_rval = 4
           current_r = 'r4'
        elif i == 801:
           current_rval = 2
           current_r = 'r5'
        Xrounds.append({})
        picked = 0
        for key, gv in x.items():
            v = gv.X
            if v == 1.0 or v == 0.0:
               nonfracxvalues[key] = v
            else:
               fracxvalues[key] = v
            r = random.random()
            val = gv.X * current_rval
            if val > 1:
               val = 1
            if r < val:
               Xrounds[i][key] = 1
               picked += 1
            else:
               Xrounds[i][key] = 0
        #print("picked "+str(i)+" "+str(picked)+", current best "+str(best_p))
        if picked-B < best:#  and picked >= 0.8*B:
           best_i = i
           best = picked-B
           best_p = picked
           best_rs = current_r

    for key in Xrounds[best_i].keys():
        X[key] = Xrounds[best_i][key]
    
    nodesPicked = [] #nodes picked at each time t
    budget = 0
    for key in X.keys():
        if X[key] == 1:
           budget += 1
           nodesPicked.append(key)

    Infected = {}
    infections = 0.0
    for key in Y.keys():
        if Y[key] == 1:
           infections += 1
           cols = key.split(",")
           j = int(cols[1])
           u = cols[0]
           if j not in Infected:
              Infected[j] = set([u])
           else:
              Infected[j].add(u)

    objValue = m.objVal
    #objValue = infections/M

    #print(fracyvalues)
    #print(nonfracyvalues)
    #print(fracxvalues)
    #print(nonfracxvalues)
    print("====================")
    print("#frac y vs nonfrac y", len(fracyvalues), len(nonfracyvalues))
    print("#frac x vs nonfrac x", len(fracxvalues), len(nonfracxvalues))
    return nodesPicked, Infected, budget, infections, objValue, current_r
             
     
    
    
