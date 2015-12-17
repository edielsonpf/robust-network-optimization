try:
    import matplotlib.pyplot as plt
except:
    raise
import networkx as nx

from optimizer.backup import Backup
from optimizer.pbackup import PathBackup

import math
from gurobipy import tuplelist

def BackupModelTest(options, num_nodes,p,invstd,mip_gap, time_limit):
    
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
    AuxCount = 0
    Aux=1
    for s,d in links:
        if AuxCount%2 == 0:
            Aux = 2
        else:
            Aux = 1
        #generating capacity for each s,d link
        capacity[s,d] = Aux
        #Generate mean for each s,d link based on Bernouilli distribution 
        mean[s,d] = Aux*p
        #Generate std for each s,d link based on Bernouilli distribution 
        std[s,d]=math.sqrt(Aux*p*(1-(Aux*p)))
        AuxCount = AuxCount+1
    
    if options == 1:
        
        pos=nx.spring_layout(G) # positions for all nodes
        
        # nodes
        nx.draw_networkx_nodes(G,pos,node_size=500)
        
        # edges
        nx.draw_networkx_edges(G,pos,width=2)
        
        # labels
        nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')
        
        plt.axis('off')
        #plt.savefig("weighted_graph.png") # save as png
        plt.show() # display
    
    #optimization
    links = tuplelist(links)
    BackupNet = Backup(nodes,links,capacity,mean,std,invstd)
    solution = BackupNet.optimize(mip_gap,time_limit)
    
    #penalizes the links chosen to be backup links
    for i,j in links:
        if solution[i,j] < 0.1:
            G.remove_edge(i, j)
        
    
    if options == 1:
        
        esmall=[(u,v) for (u,v) in G.edges()]
        
        # nodes
        nx.draw_networkx_nodes(G,pos,node_size=500)
        
        # edges
        nx.draw_networkx_edges(G,pos,edgelist=esmall,width=2,alpha=0.5,edge_color='b',style='dashed')
        
        # labels
        nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')
        
        #plt.ioff() 
        
        plt.axis('off')
        plt.show() # display
    

def BackupPathModelTest(options,num_nodes,p,invstd,mip_gap,time_limit,cutoff):
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
    
    ##############################################
    #            Plot Initial Graph
    ##############################################  
    
    if options == 1:
        #don't stop on plotted figures 
        #plt.ion() 
            
        pos=nx.spring_layout(G) # positions for all nodes
         
        # nodes
        nx.draw_networkx_nodes(G,pos,node_size=500)
         
        # edges
        nx.draw_networkx_edges(G,pos,width=2)
         
        # labels
        nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')
         
        plt.axis('off')
        #plt.savefig("weighted_graph.png") # save as png
        plt.show() # display
        
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
#         if AuxCount%2 == 0:
#             Aux = 2
#         else:
#             Aux = 1
        #generating capacity for each s,d link
        capacity[s,d] = Aux
        #Generate mean for each s,d link based on Bernouilli distribution 
        mean[s,d] = Aux*p
        #Generate std for each s,d link based on Bernouilli distribution 
        std[s,d]=math.sqrt(Aux*p*(1-(Aux*p)))
        AuxCount = AuxCount+1
        
    print(mean)
    print(std)
    
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
    if options == 1:
        esmall=[(u,v) for (u,v) in G.edges()]
         
        # nodes
        nx.draw_networkx_nodes(G,pos,node_size=500)
         
        # edges
        nx.draw_networkx_edges(G,pos,edgelist=esmall,width=2,alpha=0.5,edge_color='b',style='dashed')
         
        # labels
        nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')
         
        plt.axis('off')
        plt.show() # display
    
        #plt.ioff()

def getLinkPaths(G,i,j,s,d,cutoff):
    """Generate all simple paths in the graph G from source = i to target = j that uses 
    edge source = s to target = d.

    A simple path is a path with no repeated nodes.

    Parameters
    ----------
    G : NetworkX graph
    i : starting node for path
    j : ending node for path
    s : starting node for path
    d : ending node for path
    
    Returns
    -------
    path_generator: Paths
       A tuple list with all paths for edge (s,d) that uses (i,j).

    """
    Paths=list()
    for path in nx.all_simple_paths(G, s, d,cutoff):
        if set([i, j]).issubset(path):
            if (list(path).index(j) == list(path).index(i)+1):
                Paths.append(path) # => True
    return Paths 

def getAllPaths(G,cutoff):
    """Generate all simple paths in the graph G from each link (source to target).

    A simple path is a path with no repeated nodes.

    Parameters
    ----------
    G : NetworkX graph

    Returns
    -------
    path_generator: Paths
       A tuple list with all paths for each edge in the graph.

    """
    
    links = G.edges()
    
    Paths=list()
    for i,j in links:
        for path in nx.all_simple_paths(G, i, j,cutoff):
            Paths.append(path)
    return tuple(Paths)     