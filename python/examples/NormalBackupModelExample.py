import networkx as nx
from NetworkOptimization.NormalBackupModel import Backup
import math
from gurobipy import tuplelist
from NetworkOptimization.Tools import plotGraph

def NormalBackupModelExample(plot_options, num_nodes,p,invstd,mip_gap, time_limit):
    
    #######################################
    #        Generating graphs
    #######################################
    
    #Generates a complete indirect graph 
    H = nx.complete_graph(num_nodes)
    # transforms the indirect graph in directed one
    G = H.to_directed()
    
    #Generates a list with all links (edges) in the graph
    links = G.edges()
    #Generates a list with all nodes (vertex) in the graph
    nodes = G.nodes() 
    
    capacity={}
    mean={}
    std={}

    Aux=1
    for s,d in links:
        #generating capacity for each s,d link
        capacity[s,d] = Aux
        #Generate mean for each s,d link based on Bernouilli distribution 
        mean[s,d] = Aux*p
        #Generate std for each s,d link based on Bernouilli distribution 
        std[s,d]=math.sqrt(Aux*p*(1-(Aux*p)))
        if capacity[s,d] > 0:
            G.add_weighted_edges_from([(s,d,capacity[s,d])])
        else:
            G.add_weighted_edges_from([(s,d,capacity[s,d])])
    
    if plot_options == 1:
        pos = plotGraph(G, option=0, position=None)
    
    ################################
    #
    #          optimization
    #
    ################################
    links = tuplelist(links)
    BackupNet = Backup(nodes,links,capacity,mean,std,invstd)
    solution = BackupNet.optimize(mip_gap,time_limit)
    
    #penalizes the links chosen to be backup links
    for i,j in links:
        if solution[i,j] < 0.1:
            G.remove_edge(i, j)
       
    
    if plot_options == 1:
        option=1
        plotGraph(G, option, pos)
        
if __name__ == '__main__':
   
    #definition of the number of nodes in the network
    NumNodes = 5
    
    #definition of the link failure probability
    p=0.001
    
    #definition of the desired survivability (epsilon)
    epsilon = 0.01
    
    #Optimization definitions
    #definition of the desired MipGap, or None for optimal
    MipGap = None
    #definition of the time limit, or None for no time limit
    TimeLimit = None
    
    #constant for choosing to plot (1) or not to plot (0) the graphs
    PlotOptions = 0
    
    #constant for backup model and backup model with paths
    #definition of the Phi-standard inverse of (1-epsilon) 
    invstd = 2.326347874

    print('Normal-based backup model')  
    NormalBackupModelExample(PlotOptions, NumNodes,p,invstd,MipGap,TimeLimit)