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

def GetRandScenarios(RandSeed, FailureProb,NumScenarios, NumLinks, Links, CapPerLink):    
    """Generate random failure scenarios based on Binomial distribution.

    Parameters
    ----------
    RandSeed : Random seed (necessary for multiprocessing calls).
    FailureProb: Failure probability for each edge (link) in the graph.
    NumScenarios : Number of scenarios to be generated.
    NumLinks: Number of edges (links) on each scenario.
    Links: Graph edges (links)
    CapPerLink: Edge (link) capacity (weight) 
    
    Returns
    -------
    Scenarios: Group of scenarios with random failure following Binomial distribution.

    """ 
    if RandSeed != None:
        np.random.seed(RandSeed)
    
    Y = np.random.binomial(1, FailureProb, (NumScenarios,NumLinks))
     
    Scenarios={}
    for k in range(NumScenarios):
        Index=0
        for s,d in Links:
            Scenarios[k,s,d]=CapPerLink[Index]*Y[k,Index]
            Index=Index+1
    return Scenarios

def ThreadGetRandScenarios(RandSeed, FailureProb,NumScenarios, StartIndex, NumLinks, Links, CapPerLink):    
    """Generate random failure scenarios based on Binomial distribution.

    Parameters
    ----------
    RandSeed : Random seed (necessary for multiprocessing calls).
    FailureProb: Failure probability for each edge (link) in the graph.
    NumScenarios : Number of scenarios to be generated.
    StartIndex: Start index for each thread
    NumLinks: Number of edges (links) on each scenario.
    Links: Graph edges (links)
    CapPerLink: Edge (link) capacity (weight) 
    
    Returns
    -------
    Scenarios: Group of scenarios with random failure following Binomial distribution.

    """     
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
    """Generate random failure scenarios based on Binomial distribution using multiprocessing.

    Parameters
    ----------
    FailureProb: Failure probability for each edge (link) in the graph.
    NumScenarios : Number of scenarios to be generated.
    NumLinks: Number of edges (links) on each scenario.
    Links: Graph edges (links)
    CapPerLink: Edge (link) capacity (weight) 
    
    Returns
    -------
    Scenarios: Group of scenarios with random failure following Binomial distribution.

    """
    
    #check the number of available processors
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
        RandSeed = k
        args[k]=(RandSeed, FailureProb, NewDivision[k], start, NumLinks, Links, CapPerLink)

    # launching multiple evaluations asynchronously *may* use more processes
    multiple_results = [p.apply_async(ThreadGetRandScenarios, (args[k])) for k in range(nb_processes)]
    
    Scenarios={}
    for res in multiple_results:
        Scenarios.update(res.get(timeout=120))
    
    return Scenarios 

def GetNumFailures(Scenario, Links):    
    """Calculate the sum of failures in the scenarios.

    Parameters
    ----------
    Scenario: Scenario for calculating the number of failures.
    Links: Graph edges (links)
    
    Returns
    -------
    NumFailures: Number of failures in the scenario.

    """
    NumFailures=0
    for s,d in Links:
        NumFailures = NumFailures + Scenario[s,d]
    return NumFailures

def GetBufferedFailureProbPar(FailureProb, NumScenarios, Links, CapPerLink, BackupLinks, CapPerBackupLink, OptBackupLinks):    
    """Calculate the buffered failure probability using multiprocessing.

    Parameters
    ----------
    FailureProb: Failure probability for each edge (link) in the graph.
    Scenarios: Group of scenarios with random failure following Binomial distribution.
    NumScenarios : Number of scenarios to be generated.
    Links: Graph edges (links)
    NumLinks: Number of edges (links) on each scenario.
    CapPerLink: Set of edge (link) capacity (weight).
    BackupLinks: Set of backup edges (links).
    CapPerBackupLink: Set of backup edge (link) capacity (weight)
    OptBackupLinks: Set of backup edges (links).
    
    Returns
    -------
    P: Buffered failure probability.

    """
    #check the number of available processors 
    nb_processes = multiprocessing.cpu_count ()
    print('Number of available processors: %g' %nb_processes)
    
    p = Pool(nb_processes)
    
    #divide the total number of scenarios to be generated among the available processes 
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

def GetBufferedFailureProb(ImportanceSampling, Scenarios, NumScenarios, Links, BackupLinks, CapPerBackupLink, OptBackupLinks):    
    """Calculate the buffered failure probability.

    Parameters
    ----------
    ImportanceSampling: Importance sampling vector (obtained by GetImportanceSamplingVector method). None if scenarios were not generated using importance sampling.
    FailureProb: Failure probability for each edge (link) in the graph.
    Scenarios: Set of scenarios with random failure following Binomial distribution.
    NumScenarios : Number of scenarios to be generated.
    Links: Graph edges (links)
    NumLinks: Number of edges (links) on each scenario.
    CapPerLink: Set of edge (link) capacity (weight).
    BackupLinks: Set of backup edges (links).
    CapPerBackupLink: Set of backup edge (link) capacity (weight)
    OptBackupLinks: Set of backup edges (links).
    
    Returns
    -------
    P: Buffered failure probability.

    """
    P={}
    for i,j in BackupLinks:
        P[i,j] = 0
        for k in range(NumScenarios):
            Psd=0
            for s,d in Links:
                Psd=Psd+OptBackupLinks[i,j,s,d]*Scenarios[k,s,d]
            if Psd > CapPerBackupLink[i,j]:
                if ImportanceSampling == None:
                    P[i,j]=P[i,j]+1
                else:
                    P[i,j]=P[i,j]+1*ImportanceSampling[k]
        P[i,j]=1.0*P[i,j]/NumScenarios
    return P

def ThreadGetBufferedFailureProb(RandSeed, FailureProb, NumScenarios, Links, CapPerLink, BackupLinks, CapPerBackupLink, OptBackupLinks):    
    """Thread to calculate the buffered failure probability.

    Parameters
    ----------
    RandSeed : Random seed (necessary for multiprocessing calls).
    FailureProb: Failure probability for each edge (link) in the graph.
    NumScenarios : Number of scenarios to be generated.
    Links: Graph edges (links)
    CapPerLink: Set of edge (link) capacity (weight).
    BackupLinks: Set of backup edges (links).
    CapPerBackupLink: Set of backup edge (link) capacity (weight)
    OptBackupLinks: Set of backup edges (links).
    
    Returns
    -------
    P: Buffered failure probability.

    """
    
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

def GetImportanceSamplingVector(Links, Scenarios, NumScenarios, FailureProb, FailureProbIS):
    """Calculate the importance sampling vector.
    
    Parameters
    ----------
    Links: Graph edges (links)
    Scenarios: Set of scenarios with random failure following Binomial distribution.
    NumScenarios : Number of scenarios to be generated.
    FailureProb: Failure probability for each edge (link) in the graph.
    FailureProbIS: Importance sampling failure probability for each edge (link) in the graph.
    
    Returns
    -------
    ImpSamp: Importance sampling vector.

    """
    ImpSamp={}
    for k in range(NumScenarios):
        sum_failure=0
        for s,d in Links:
            sum_failure=sum_failure+Scenarios[k,s,d]
        ImpSamp[k]=(FailureProb**(sum_failure)*(1-FailureProb)**(len(Links)-sum_failure))/(FailureProbIS**(sum_failure)*(1-FailureProbIS)**(len(Links)-sum_failure))
    return ImpSamp

def GetImportanceSamplingVectorR(Links, Scenarios, NumScenarios, FailureProb, FailureProbIS, Epsilon):
    """Calculate the importance sampling vector.
    
    Parameters
    ----------
    Links: Graph edges (links)
    Scenarios: Set of scenarios with random failure following Binomial distribution.
    NumScenarios : Number of scenarios to be generated.
    FailureProb: Failure probability for each edge (link) in the graph.
    FailureProbIS: Importance sampling failure probability for each edge (link) in the graph.
    
    Returns
    -------
    ImpSamp: Importance sampling vector.

    """
    print('1/n x epsilon = %g'%(1/(NumScenarios*Epsilon)))
    ImpSamp={}
    A={}
    MaxA={}
    for k in range(NumScenarios):
        sum_failure=0
        for s,d in Links:
            sum_failure=sum_failure+Scenarios[k,s,d]
        ImpSamp[k]=(FailureProb**(sum_failure)*(1-FailureProb)**(len(Links)-sum_failure))/(FailureProbIS**(sum_failure)*(1-FailureProbIS)**(len(Links)-sum_failure))
        A[k]=1.0*(ImpSamp[k]/(NumScenarios*Epsilon))
        if k == 0:
            MaxA=A[k]
        else:    
            if A[k] > MaxA:
                MaxA=A[k]
#    print A
#    print MaxA        
#    print ImpSamp
    return ImpSamp, A, MaxA