# EpiControl

Requirements:
Gurobi 9.0.1
Python 2.7.17

How to run:
python ApproxGuarantees.py network_file output_file p exps M initial_budget deg_threshold freq_threshold output_prefix noBs
where,
network_file : edge list representation of the graph
output_file : output file that displays details of the saaround and the baselines results
p : infection probability
exps : expected number of sources in the epidemic
M : number of sampled subgraphs
initial_budget : given initial budget
deg_threshold : threshold on degree for nodes to be considered for vaccination (e.g. only select nodes with at least 2 neighbors)
freq_threshold : threshold on frequency of nodes getting infected over the samples (e.g. only select nodes that are infected in atleast a fraction (0.1) of samples)
output_prefix : outputfile prefix which will be used to generate outputfiles with nodes selected for each budget 
noBs : number of budget values (e.g. if initial_budget = 10  and noBs = 5, then we run the program for the following set of budgets: {10, 20, 30, 40, 50})

Output_file format:
A CSV file in which each line in the file consits of the following information:
given_budget,used_no_vaccines,no_action,saaRound_obj,degree_obj,evc_obj

given_budget : the budget given as input to the program
used_no_vaccines : budget used by saaRound algorithm (budget can be violated, and we show theoretical guarantees on the violation in paper)
no_action : average no. of infections (over the samples) if no interventions are performed
saaRound_obj : average no. of infections after intervening on set of nodes picked by saaRound
degree_obj: average no. of infections if degree baseline is used
evc_obj: average no. of infections if eigenvector centrality baseline is used

Paper link: https://dl.acm.org/doi/abs/10.5555/3398761.3398899
