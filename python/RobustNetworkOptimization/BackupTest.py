try:
    import matplotlib.pyplot as plt
except:
    raise
import networkx as nx

from optimizer.backup import Backup
from optimizer.pbackup import PathBackup

import math
from gurobipy import tuplelist

def BackupModelTest():
    #don't stop on plotted figures 
    #plt.ion() 
    
    # Constant definition
    p = 0.025
    invstd = 2.326347874
    
    #Generating graphs
    G=nx.DiGraph()
    
    G.add_edge('1','2',capcity=1)
    G.add_edge('1','3',capcity=1)
    G.add_edge('1','4',capcity=1)
    G.add_edge('2','1',capcity=1)
    G.add_edge('2','3',capcity=1)
    G.add_edge('2','4',capcity=1)
    G.add_edge('3','1',capcity=1)
    G.add_edge('3','2',capcity=1)
    G.add_edge('3','4',capcity=1)
    G.add_edge('4','1',capcity=1)
    G.add_edge('4','2',capcity=1)
    G.add_edge('4','3',capcity=1)
    
    links = G.edges()
    nodes = G.nodes() 
    
    capacity={}
    mean={}
    std={}
    for i,j in links:
        #generating capacity list
        capacity[i,j] = 1
        #generating mean list
        mean[i,j] = p
        std[i,j]=math.sqrt(p*(1-p))
    
    elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['capcity'] >0.5]
    esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['capcity'] <=0.5]
    
    pos=nx.spring_layout(G) # positions for all nodes
    
    # nodes
    nx.draw_networkx_nodes(G,pos,node_size=500)
    
    # edges
    nx.draw_networkx_edges(G,pos,edgelist=elarge,width=2)
    nx.draw_networkx_edges(G,pos,edgelist=esmall,width=2,alpha=0.5,edge_color='b',style='dashed')
    
    # labels
    nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')
    
    plt.axis('off')
    plt.savefig("weighted_graph.png") # save as png
    plt.show() # display
    
    #optimization
    links = tuplelist(links)
    BackupNet = Backup(nodes,links,capacity,mean,std,invstd)
    solution = BackupNet.optimize()
    
    #penalizes the links chosen to be backup links
    for i,j in links:
        if solution[i,j] < 0.1:
            G.remove_edge(i, j)
        
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
    
def BackupPathModelTest():
    #don't stop on plotted figures 
    #plt.ion() 
    
    # Constant definition
    p = 0.025
    invstd = 2.326347874
    
    #Generating graphs
    #G=nx.DiGraph()
    H = nx.complete_graph(4)
    G = H.to_directed()
    
    links = G.edges()
    nodes = G.nodes() 
    
    paths = getAllPaths(G, links)
    
    Psd = {}
    for s,d in links:
        Psd[s,d] = nx.all_simple_paths(G, source=s, target=d)
        #print(list(Psd[s,d]))
   
    Pij = getPaths(G, links)
        
    capacity={}
    mean={}
    std={}
    for i,j in links:
        #generating capacity list
        capacity[i,j] = 1
    
    for pth in paths:
        #generating mean list
        mean[paths.index(pth)] = p
        std[paths.index(pth)]=math.sqrt(p*(1-p))
     
    #elarge=[(u,v) for (u,v) in G.edges(data=True)]
    #esmall=[(u,v) for (u,v) in G.edges(data=True)]
     
    pos=nx.spring_layout(G) # positions for all nodes
     
    # nodes
    nx.draw_networkx_nodes(G,pos,node_size=500)
     
    # edges
    nx.draw_networkx_edges(G,pos,width=2)
    #nx.draw_networkx_edges(G,pos,width=2,alpha=0.5,edge_color='b',style='dashed')
     
    # labels
    nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')
     
    plt.axis('off')
    plt.savefig("weighted_graph.png") # save as png
    plt.show() # display
     
    #optimization
    links = tuplelist(links)
    BackupNet = PathBackup(nodes,links,paths,Psd,Pij,capacity,mean,std,invstd)
    solution = BackupNet.optimize()
     
    #penalizes the links chosen to be backup links
    for i,j in links:
        if solution[i,j] < 0.1:
            G.remove_edge(i, j)
         
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


def getPaths(G,links):
    P={}
    for i,j in links:
        #print('Link: '+ str([i,j]))
        Pij=list()
        for s,d in links:
            #print('Paths in: '+ str([s,d]))
            for path in nx.all_simple_paths(G, source=s, target=d):
                #print(path)
                #print([i,j])
                #print(set(path).issubset([i, j])) # => True
                if set([i, j]).issubset(path):
                    if (list(path).index(j) == list(path).index(i)+1):
                        #print('True')
                        #print(path)
                        Pij.append(path) # => True
                    #else:
                        #print('False')
        #print(Pij)
        P[i,j]=Pij
    return P 

def getAllPaths(G,links):
    P=list()
    for i,j in links:
        for path in nx.all_simple_paths(G, source=i, target=j):
            P.append(path)
    return tuple(P)     