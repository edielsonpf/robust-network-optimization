try:
    import matplotlib.pyplot as plt
except:
    raise
import networkx as nx
import numpy as np
# import math
from gurobipy import tuplelist
from optimizer.bpbackup import bpBackup


#matplotlib inline
#import numpy as np
# import pandas as pd
# import statsmodels.api as sm
# import sympy as sp
# import pymc
# import matplotlib.gridspec as gridspec
# from mpl_toolkits.mplot3d import Axes3D
# from scipy import stats
# from scipy.special import gamma

from sympy.interactive import printing
printing.init_printing()


def MonteCarloTest(options, num_nodes,num_scenarios,p,epsilon,mip_gap, time_limit):
    
    # Simulate data
    #np.random.seed(123)
    print('\nGenerating random scenarios...')
    nobs = num_nodes*(num_nodes-1)
    Y = np.random.binomial(1, p, (num_scenarios,nobs))
    #mu, sigma = 2, 0.4 #
    #Y = np.random.normal(mu,sigma,(num_scenarios,nobs))
    print(Y)
    print('Done!\n')
    # Plot the data
#     fig = plt.figure(figsize=(7,3))
#     gs = gridspec.GridSpec(1, 2, width_ratios=[5, 1]) 
#     ax1 = fig.add_subplot(gs[0])
#     ax2 = fig.add_subplot(gs[1])
#      
#     ax1.plot(range(nobs), Y[0], 'x')
#     ax2.hist(-Y[0], bins=2)
#      
#     ax1.yaxis.set(ticks=(0,1), ticklabels=('Failure', 'Success'))
#     ax2.xaxis.set(ticks=(-1,0), ticklabels=('Success', 'Failure'));
#     
#     ax1.set(title=r'Bernoulli Trial Outcomes $(\theta=0.3)$', xlabel='Trial', ylim=(-0.2, 1.2))
#     ax2.set(ylabel='Frequency')
#      
#     fig.tight_layout()
    
    #Generates a complete indirect graph 
    H = nx.complete_graph(num_nodes)
    # transforms the indirect graph in directed one
    G = H.to_directed()
    
    #Generates a list with all links (edges) in the graph
    links = G.edges()
    #Generates a list with all nodes (vertex) in the graph
    nodes = G.nodes() 
    
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
            
    #print(capacity)
    #optimization
    print('Creating model...')
    links = tuplelist(links)
    BackupNet = bpBackup(nodes,links,capacity,epsilon,num_scenarios)
    print('Done!\n')
    print('Solving...\n')
    solution = BackupNet.optimize(mip_gap,time_limit)
    
    #print(solution)