import numpy as np
import networkx as nx
import time
try:
    import matplotlib.pyplot as plt
except:
    raise

import multiprocessing
from multiprocessing import Pool
import json
###################################################
#
#            Auxiliary functions
#
###################################################
    
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

def plotGraph(G,option,position=None):
    """Plot a graph G with specific position.

    Parameters
    ----------
    G : NetworkX graph
    option : if 1, edges with weight greater then 0 are enlarged. The opposite happens for option equal to 0.
    position : nodes position 
    
    Returns
    -------
    position: nodes position generated during plot (or same positions if supplied).

    """
    if option == 1:
        elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] > 0]
        esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <= 0]
    else:
        elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <= 0]
        esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] > 0]
        
    
    if position == None:
        position=nx.spring_layout(G) # positions for all nodes
    
    # nodes
    nx.draw_networkx_nodes(G,position,node_size=500)
        
    # edges
    nx.draw_networkx_edges(G,position,edgelist=elarge,width=2)
    nx.draw_networkx_edges(G,position,edgelist=esmall,width=2,alpha=0.5,edge_color='b',style='dashed')
    
    # labels
    nx.draw_networkx_labels(G,position,font_size=20,font_family='sans-serif')
    
    plt.axis('off')
    #plt.savefig("weighted_graph.png") # save as png
    plt.show() # display
    
    return position

def GeometricMean(A, max_it):
    
    #number of rows in the matrix X
    m = 1
    n = len(A)
    
    print('[Geometric Mean] Number of lines: %s'%m)
    print('[Geometric Mean] Number of columns: %s' %n)
    
    r = np.zeros(m)
    
    t=0
        
    while t < max_it:
        max_x = np.asscalar(np.max(A))
        #get the minimum value at row i
        min_x = np.asscalar(np.min(A))
        #calculate the geometric mean
        r=np.nan_to_num(1.0*np.sqrt(1.0/(max_x*min_x)))
        
        #scale matrix X based on R
        A=r*A 
                    
        t=t+1
    
    X={}
    for i in range(len(A)):
        X[i]=A[i]
    
    return X


def GetFullConnectedNetwork(num_nodes):
    #Generates a complete indirect graph 
    H = nx.complete_graph(num_nodes)
    # transforms the indirect graph in directed one
    G = H.to_directed()
    
    #Generates a list with all links (edges) in the graph
    links = G.edges()
    #Generates a list with all nodes (vertex) in the graph
    nodes = G.nodes()
    
    #Check the number of links
    num_links = len(links)
    
    return G,links,nodes,num_links


def GetFSNETNetwork():
    
    num_nodes=14
        
    nodes = [i+1 for i in range(num_nodes)]

    links=[(1,2),(1,3),(1,4),(2,1),(2,3),(2,8),(3,1),(3,2),(3,7),(4,1),(4,5),(4,9),(5,4),(5,6),(5,7),
           (6,5),(6,8),(7,3),(7,5),(7,10),(7,13),(8,2),(8,6),(8,11),(9,4),(9,12),(9,14),(10,7),(10,11),
           (11,8),(11,10),(11,12),(11,14),(12,9),(12,11),(12,13),(13,7),(13,12),(13,14),(14,9),(14,11),(14,13)]
    
  
    G=nx.DiGraph()
    
    G.add_nodes_from(nodes)
    G.add_edges_from(links)
    
    #Check the number of links
    num_links = len(links)
    
    return G,links,nodes,num_links

def GetSprintNetwork():
    
    num_nodes=36
        
    nodes = [i+1 for i in range(num_nodes)]

    links=[(1,2),(1,3),
           (2,1),(2,3),(2,10),
           (3,1),(3,2),(3,4),
           (4,3),(4,5),(4,11),
           (5,4),(5,6),(5,7),
           (6,5),(6,8),(6,9),
           (7,5),(7,8),(7,13),
           (8,6),(8,7),(8,9),
           (9,6),(9,8),
           (10,2),(10,11),(10,19),
           (11,4),(11,10),(11,12),(11,17),
           (12,11),(12,13),(12,15),
           (13,7),(13,12),(13,16),
           (14,15),(14,18),(14,23),
           (15,12),(15,14),(15,16),
           (16,13),(16,15),(16,24),
           (17,11),(17,18),(17,19),(17,21),
           (18,14),(18,17),(18,20),
           (19,10),(19,17),(19,21),
           (20,18),(20,21),(20,22),
           (21,17),(21,19),(21,20),(21,26),(21,27),
           (22,20),(22,23),(22,26),
           (23,15),(23,22),(23,25),
           (24,16),(24,25),(24,28),
           (25,23),(25,24),(25,31),
           (26,21),(26,22),(26,27),
           (27,21),(27,26),(27,33),(27,34),
           (28,24),(28,29),(28,30),
           (29,28),(29,30),(29,31),
           (30,28),(30,29),
           (31,25),(31,29),(31,32),
           (32,31),(32,34),
           (33,27),(33,36),
           (34,27),(34,32),(34,35),
           (35,34),(35,36),
           (36,33),(36,35)]
    
  
    G=nx.DiGraph()
    
    G.add_nodes_from(nodes)
    G.add_edges_from(links)
    
    #Check the number of links
    num_links = len(links)
    
    return G,links,nodes,num_links      


def GetRingNetwork(num_nodes):
    
    nodes = [i for i in range(num_nodes)]

    links=[]
    for node in nodes:
        if node == num_nodes-1:
            links.append((node,0))
            links.append((0,node))
        else:    
            links.append((node,node+1))
            links.append((node+1,node))
            
    G=nx.DiGraph()
    
    G.add_nodes_from(nodes)
    G.add_edges_from(links)
    
    #Check the number of links
    num_links = len(links)
    
    return G,links,nodes,num_links