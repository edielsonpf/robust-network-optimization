import networkx as nx

from NetworkOptimization.PathBackupModel import PathBackup
from NetworkOptimization.Tools import plotGraph, getAllPaths, getLinkPaths

import math
from gurobipy import tuplelist

def PathBackupModelExample(plot_options,num_nodes,p,invstd,mip_gap,time_limit,cutoff):
    ""
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
    Aux = 1
    for s,d in links:
        #generating capacity for each s,d link
        capacity[s,d] = Aux
        if capacity[s,d] > 0:
            G.add_weighted_edges_from([(s,d,capacity[s,d])])
        else:
            G.add_weighted_edges_from([(s,d,capacity[s,d])])
            
    
    if plot_options == 1:
    ##############################################
    #            Plot Initial Graph
    ##############################################  
        pos = plotGraph(G, option=None, position=None)
        
    #######################################
    #        Optimization Model
    #######################################
    
    #Find all possible paths in the graph for all source -> destination pairs
    paths = getAllPaths(G,cutoff)
 
    #Find all possible paths for each source (s) -> destination (d) pair
    Psd = {}
    for s,d in links:
        Psd[s,d] = nx.all_simple_paths(G, s, d,cutoff)
    
    #Find all s->d paths that uses the i->j link
    Pij={}
    for i,j in links:
        for s,d in links:
            Pij[i,j,s,d] = getLinkPaths(G,i,j,s,d,cutoff)
    
    capacity={}
    mean={}
    std={}
    
    AuxCount = 0
    Aux=1
    for s,d in links:
        #generating capacity for each s,d link
        capacity[s,d] = Aux
        #Generate mean for each s,d link based on Binomial distribution 
        mean[s,d] = Aux*p
        #Generate std for each s,d link based on Binomial distribution 
        std[s,d]=math.sqrt(Aux*p*(1-(Aux*p)))
        AuxCount = AuxCount+1
        
    #optimization
    links = tuplelist(links)
    # Creating a backup network model
    BackupNet = PathBackup(nodes,links,paths,Psd,Pij,capacity,mean,std,invstd)
    # Find a optimal solution
    solution = BackupNet.optimize(mip_gap,time_limit)
         
    #Remove links not chosen as backup link
    for i,j in links:
        if solution[i,j] < 0.1:
            G.remove_edge(i, j)
    
    ##############################################
    #            Plot Solution
    ##############################################     
    if plot_options == 1:
        option=1
        plotGraph(G, option, pos)
        
        
if __name__ == '__main__':
    #constant for choosing to plot (1) or not to plot (0) the graphs
    PlotOptions = 0
    
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
    
    #constant for backup model and backup model with paths
    #definition of the Phi-standard inverse of (1-epsilon) 
    invstd = 2.326347874

    #definition of the graph depth (cutoff) when looking for paths, i.e. path extension
    # Example: CutoffList = [None, 2, 1], will test for no limit, max path extension of  2 and 1
    CutoffList = [1,2,None]
 
    for cutoff in CutoffList:
        print('Normal-based backup model with paths: cutoff = %g' % cutoff)  
        PathBackupModelExample(PlotOptions,NumNodes,p,invstd,MipGap,TimeLimit,cutoff)