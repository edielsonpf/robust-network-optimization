try:
    import matplotlib.pyplot as plt
except:
    raise
import networkx as nx
import numpy as np
import scipy.stats as stats

from optimizer.backup import Backup
from optimizer.pbackup import PathBackup
from optimizer.bfpbackup import BFPBackup


import math
from gurobipy import tuplelist

def BackupModelTest(plot_options, num_nodes,p,invstd,mip_gap, time_limit):
    
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

def BackupPathModelTest(plot_options,num_nodes,p,invstd,mip_gap,time_limit,cutoff):
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
    if plot_options == 1:
        option=1
        plotGraph(G, option, pos)

def BackupBFPModelTest(plot_options,num_nodes,scenario, num_scenarios,p,epsilon,mip_gap, time_limit):
        
    if scenario == 0:
        print('Scenario based on a full connected and directed graph with %s nodes.' %(num_nodes))
        print('\nGenerating %s random scenarios...' %(num_scenarios))
        nobs = num_nodes*(num_nodes-1)
        p2=p+0.075
        print('Failure probability for impotance sample: %g' %p2)
        #Y = np.random.binomial(1, p, (num_scenarios,nobs))
        Y=stats.binom.rvs(1,p2,size=(num_scenarios,nobs))
    #     print(Y)
        print('Done!\n')
        
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
        
        #importance sample
        ImpSamp={}
        for i,j in links:
            for k in range(num_scenarios):
                sum_failue=0
                for s,d in links:
                    sum_failue=sum_failue+capacity[k,s,d]
                #print('f(%g)=%g' % (sum_failue,stats.binom.pmf(sum_failue,len(links),p)))
                #print('h(%g)=%g' % (sum_failue,stats.binom.pmf(sum_failue,len(links),p2)))
                ImpSamp[k,i,j]=stats.binom.pmf(sum_failue,len(links),p)/stats.binom.pmf(sum_failue,len(links),p2)
                #print('f(x)/h(x)=%g' %ImpSamp[k,i,j])
            #print(len(ImpSamp))
            
                
    elif scenario == 1:
        print('Scenario based on 14-node NSFNET (1991) with 14 nodes.')
        
        nodes = [i+1 for i in range(14)]
    
        links=[(1,2),(1,3),(1,4),(2,1),(2,3),(2,8),(3,1),(3,2),(3,7),(4,1),(4,5),(4,9),(5,4),(5,6),(5,7),
               (6,5),(6,8),(7,3),(7,5),(7,10),(7,13),(8,2),(8,6),(8,11),(9,4),(9,12),(9,14),(10,7),
               (10,11),(11,8),(11,10),(11,12),(11,14),(12,9),(12,11),(12,13),(13,7),(13,12),(13,14),(14,9),(14,11),(14,13)]
        
        print('Number of links: %g' %(len(links)))
        G=nx.DiGraph()
        
        G.add_nodes_from(nodes)
        G.add_edges_from(links)
        
        print('\nGenerating %s random scenarios...' %(num_scenarios))
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
            
    if plot_options == 1:    
        #Plot Initial Graph
        plotGraph(G,option=None,position=None)
                        
    ################################
    #
    #    Optimization
    #
    ################################
    print('Creating model...')
    links = tuplelist(links)
    BackupNet = BFPBackup(ImpSamp,nodes,links,capacity,epsilon,num_scenarios)
    print('Done!\n')
    print('Solving...\n')
    OptCapacity,BackupLinks = BackupNet.optimize(mip_gap,time_limit,None)
    
    print('\n[solution] Capacity assigned per backup link:\n' )
    ChoosenLinks={}
    for i,j in links:
        if OptCapacity[i,j] > 0.0001:
            print('C[%s,%s]: %g' % (i,j, OptCapacity[i,j]))
            ChoosenLinks[i,j]=1
        else:
            ChoosenLinks[i,j]=0    
    
    n={}
    aux=0
    cont=0
    for i,j in links:
        n[i,j]=0
        for s,d in links:
            if (BackupLinks[i,j,s,d] > 0.0001) & (ChoosenLinks[i,j] == 1):
                n[i,j] =(n[i,j]+BackupLinks[i,j,s,d])
        if((n[i,j] > 0) & ChoosenLinks[i,j] == 1):
            aux=aux+n[i,j]
            cont=cont+1
    print('\n[solution] Average nij: %g\n' % (aux/cont))
    
    ##############################
    #    Survivability
    ##############################
    for i,j in links:
        if OptCapacity[i,j] > 0.0001:
            Reliability = 0
            for k in range(num_scenarios):
                Psd=0
                for s,d in links:
                    Psd=Psd+BackupLinks[i,j,s,d]*capacity[k,s,d]
                if Psd > OptCapacity[i,j]:
                    Reliability=Reliability+1
            print('[solution][1]Reliability[%s,%s] = %g' %(i,j,(1.0*Reliability/num_scenarios)))    

    num_scenarios = 1000000
    print('\nGenerating %s random scenarios for survivability test...' %(num_scenarios))
    nobs = len(links)
    Y = np.random.binomial(1, p, (num_scenarios,nobs))
    capacity={}
    Aux=1
    for k in range(num_scenarios):
        AuxCount = 0
        for s,d in links:
            #generating capacity for each s,d link
            capacity[k,s,d] = Aux*Y[k,AuxCount]
            AuxCount = AuxCount+1
    print('Done!\n')
    
    
    for i,j in links:
        if OptCapacity[i,j] > 0.0001:
            Reliability = 0
            for k in range(num_scenarios):
                Psd=0
                for s,d in links:
                    Psd=Psd+BackupLinks[i,j,s,d]*capacity[k,s,d]
                if Psd > OptCapacity[i,j]:
                    Reliability=Reliability+1
            print('[solution][2]Reliability[%s,%s] = %g' %(i,j,1.0*Reliability/num_scenarios)) 



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