import networkx as nx

from NetworkOptimization.NormalBackupModel import Backup

import math
from gurobipy import tuplelist

from NetworkOptimization.Tools import plotGraph

def NormalBackupModelTest(plot_options, num_nodes,p,invstd,mip_gap, time_limit):
    
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