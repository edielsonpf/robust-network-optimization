try:
    import matplotlib.pyplot as plt
except:
    raise
import networkx as nx
import numpy as np
from gurobipy import tuplelist
from optimizer.bpbackup import bpBackup

def NSFNET(options, num_scenarios,p,epsilon,mip_gap, time_limit):
    nodes = [i+1 for i in range(14)]
    
    links=[(1,2),(1,3),(1,4),(2,1),(2,3),(2,8),(3,1),(3,2),(3,7),(4,1),(4,5),(4,9),(5,4),(5,6),(5,7),
           (6,5),(6,8),(7,3),(7,5),(7,10),(7,13),(8,2),(8,6),(8,11),(9,4),(9,12),(9,14),(10,7),
           (10,11),(11,8),(11,10),(11,12),(11,14),(12,9),(12,11),(12,13),(13,7),(13,12),(13,14),(14,9),(14,11),(14,13)]
    
    print('Number of links: %g' %(len(links)))
    G=nx.Graph()
    
    G.add_nodes_from(nodes)
    G.add_edges_from(links)
    
    print('\nGenerating random scenarios...')
    nobs = len(links)
    Y = np.random.binomial(1, p, (num_scenarios,nobs))
    print('Done!\n')
    
    capacity={}
    Aux=1
    for i in range(num_scenarios):
        AuxCount = 0
        for s,d in links:
            #generating capacity for each s,d link
            capacity[i,s,d] = Aux*Y[i,AuxCount]
            AuxCount = AuxCount+1
            if capacity[i,s,d] > 0:
                G.add_weighted_edges_from([(s,d,capacity[i,s,d])])
            else:
                #G.remove_edge(s,d)
                G.add_weighted_edges_from([(s,d,capacity[i,s,d])])
        
        if options == 1:    
            
            elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] > 0]
            esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <= 0]
            
            pos=nx.spring_layout(G) # positions for all nodes
            
            # nodes
            nx.draw_networkx_nodes(G,pos,node_size=500)
            
            
            # edges
            nx.draw_networkx_edges(G,pos,edgelist=elarge,width=2)
            nx.draw_networkx_edges(G,pos,edgelist=esmall,width=2,alpha=0.5,edge_color='b',style='dashed')
            
            # labels
            nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')
            
            plt.axis('off')
            #plt.savefig("weighted_graph.png") # save as png
            plt.show() # display
            
    #optimization
    print('Creating model...')
    links = tuplelist(links)
    BackupNet = bpBackup(nodes,links,capacity,epsilon,num_scenarios)
    print('Done!\n')
    print('Solving...\n')
    solution = BackupNet.optimize(mip_gap,time_limit)
    
    #print(solution)