import numpy as np
import networkx as nx
import time
try:
    import matplotlib.pyplot as plt
except:
    raise

import multiprocessing
from multiprocessing import Pool

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

def GetRandScenarios(RandSeed, FailureProb,NumScenarios, NumLinks, Links, CapPerLink):    
     
    if RandSeed != None:
#         print('My seed: %g' %RandSeed)
        np.random.seed(RandSeed)
    
    Y = np.random.binomial(1, FailureProb, (NumScenarios,NumLinks))
     
    Scenarios={}
    for k in range(NumScenarios):
        Index=0
        for s,d in Links:
            Scenarios[k,s,d]=CapPerLink[Index]*Y[k,Index]
            Index=Index+1
    return Scenarios

def GetRandScenariosThread(RandSeed, FailureProb,NumScenarios, StartIndex, NumLinks, Links, CapPerLink):    
     
    if RandSeed != None:
#         print('My seed: %g' %RandSeed)
        np.random.seed(RandSeed)
    
    Y = np.random.binomial(1, FailureProb, (NumScenarios,NumLinks))
     
    Scenarios={}
    for k in range(NumScenarios):
        Index=0
        for s,d in Links:
            Scenarios[StartIndex+k,s,d]=CapPerLink[Index]*Y[k,Index]
            Index=Index+1
    return Scenarios

def GetRandScenariosPar(FailureProb,NumScenarios, NumLinks, Links, CapPerLink):    
    
    nb_processes = multiprocessing.cpu_count ()
    print('Number of available processors: %g' %nb_processes)
    
    p = Pool(nb_processes)
     
    Dividend = NumScenarios/nb_processes
    Rest=NumScenarios-(nb_processes*Dividend)
    NewDivision=[0 for k in range(nb_processes)]
    args = [0 for k in range(nb_processes)]
    start=0
    for k in range(nb_processes):
        NewDivision[k]=Dividend
        if k == 0:
            NewDivision[k]=NewDivision[k]+Rest
            start=0
        else:
            start=start+NewDivision[k-1]
        RandSeed = int(np.random.exponential(time.clock()))
        args[k]=(RandSeed, FailureProb, NewDivision[k], start, NumLinks, Links, CapPerLink)

    # launching multiple evaluations asynchronously *may* use more processes
    multiple_results = [p.apply_async(GetRandScenariosThread, (args[k])) for k in range(nb_processes)]
    
    Scenarios={}
    for res in multiple_results:
        Scenarios.update(res.get(timeout=120))
    
    return Scenarios 

def GetNumFailures(Scenario, Links):    
    NumFailures=0
    for s,d in Links:
        NumFailures = NumFailures + Scenario[s,d]
    return NumFailures

def GetBufferedFailureProbPar(FailureProb, Scenarios, NumScenarios, Links, CapPerLink, BackupLinks, CapPerBackupLink, OptBackupLinks):    

#     info('function GetRandScenariosPar')
    
    nb_processes = multiprocessing.cpu_count ()
    print('Number of available processors: %g' %nb_processes)
    
    p = Pool(nb_processes)
    
    Dividend = NumScenarios/nb_processes
    Rest=NumScenarios-(nb_processes*Dividend)
    NewDivision=[0 for k in range(nb_processes)]
    args = [0 for k in range(nb_processes)]
    start=0
    for k in range(nb_processes):
        NewDivision[k]=Dividend
        if k == 0:
            NewDivision[k]=NewDivision[k]+Rest
            start=0
        else:
            start=start+NewDivision[k-1]
        
        RandSeed = int(np.random.exponential(time.clock()))
        args[k]=(RandSeed, FailureProb, NewDivision[k], Links, CapPerLink, BackupLinks, CapPerBackupLink, OptBackupLinks) 
                    
    # launching multiple evaluations asynchronously *may* use more processes
    multiple_results = [p.apply_async(ThreadGetBufferedFailureProb, (args[k])) for k in range(nb_processes)]
    
    P={}
    for i,j in BackupLinks:
        P[i,j]=0
    Counter=0
    for res in multiple_results:
        AvgP = res.get(timeout=240)
        for i,j in BackupLinks:
            P[i,j]=P[i,j] + 1.0*AvgP[i,j]
        Counter=Counter+1
    
    for i,j in BackupLinks:
        P[i,j]=1.0*P[i,j]/Counter
        
    p.close()
    p.join()
    
    return P

def GetBufferedFailureProb(Scenarios, NumScenarios, Links, BackupLinks, CapPerBackupLink, OptBackupLinks):    
    
    P={}
    for i,j in BackupLinks:
        P[i,j] = 0
        for k in range(NumScenarios):
            Psd=0
            for s,d in Links:
                Psd=Psd+OptBackupLinks[i,j,s,d]*Scenarios[k,s,d]
            if Psd > CapPerBackupLink[i,j]:
                P[i,j]=P[i,j]+1
        P[i,j]=1.0*P[i,j]/NumScenarios
    return P

def ThreadGetBufferedFailureProb(RandSeed, FailureProb, NumScenarios, Links, CapPerLink, BackupLinks, CapPerBackupLink, OptBackupLinks):    
    
    Scenarios = GetRandScenarios(RandSeed, FailureProb, NumScenarios, len(Links), Links, CapPerLink)
        
    P={}
    for i,j in BackupLinks:
        P[i,j] = 0
        for k in range(NumScenarios):
            Psd=0
            for s,d in Links:
                Psd=Psd+OptBackupLinks[i,j,s,d]*Scenarios[k,s,d]
            if Psd > CapPerBackupLink[i,j]:
                P[i,j]=P[i,j]+1
        P[i,j]=1.0*P[i,j]/NumScenarios
    return P