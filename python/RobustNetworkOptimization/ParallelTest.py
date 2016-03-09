import networkx as nx
from NetworkOptimization.BFPBackupModel import BFPBackup
from gurobipy import tuplelist
import time
from NetworkOptimization.Tools import GetRandScenarios, GetBufferedFailureProbPar, GetBufferedFailureProb

def ParallelValidation(NumNodes, NumScenarios, NumScenariosValid, p, p2, epsilon, MipGap, TimeLimit):

    #================================================================     
    #Generates a complete indirect graph 
    H = nx.complete_graph(NumNodes)
    # transforms the indirect graph in directed one
    G = H.to_directed()
    
    #Generates a list with all links (edges) in the graph
    links = G.edges()
    #Generates a list with all nodes (vertex) in the graph
    nodes = G.nodes() 
    
    #Check the number of links
    nobs = len(links)
    
    #You must change here if there is a different capacity for each link 
    CapPerLink=[1 for i in range(nobs)]
    
    print('Failure probability for importance sample: %g' %p2)
    scenarios = GetRandScenarios(None, p2, NumScenarios, nobs, links, CapPerLink)
    
    #Generates the importance sampling factor for each sample
    ImpSamp={}
    for i,j in links:
        for k in range(NumScenarios):
            sum_failure=0
            for s,d in links:
                sum_failure=sum_failure+scenarios[k,s,d]
            ImpSamp[k,i,j]=(p**(sum_failure)*(1-p)**(len(links)-sum_failure))/(p2**(sum_failure)*(1-p2)**(len(links)-sum_failure))
    
    
    print('Creating model...')
    links = tuplelist(links)
    BackupNet = BFPBackup(ImpSamp,nodes,links,scenarios,epsilon,NumScenarios)
    print('Done!\n')
    print('Solving...\n')
    OptCapacity,BackupLinks = BackupNet.optimize(MipGap,TimeLimit,None)
    
    print('\nCapacity assigned per backup link:\n' )
    BkpLinks={}
    for i,j in links:
        if OptCapacity[i,j] > 0.0001:
            print('C[%s,%s]: %g' % (i,j, OptCapacity[i,j]))
            if (len(BkpLinks) == 0):
                BkpLinks=[(i,j)]
            else:
                BkpLinks=BkpLinks+[(i,j)]
        
    print('\nGenerating %g random scenarios for new failure probability test...' %NumScenariosValid)
    
    start = time.clock()
    scenarios = GetRandScenarios(None, p, NumScenariosValid, nobs, links, CapPerLink)
    print('Done!\n')    
    
    print('\nBuffered failure probability using new scenarios:\n')
    BufferedP = GetBufferedFailureProb(scenarios, NumScenariosValid, links, BkpLinks, OptCapacity, BackupLinks)
    stop = time.clock()        
    print('[%g seconds]Done!\n'%(stop-start))
    
    AverageP=0
    MaxP=0
    for i,j in BkpLinks:
        print('p[2][%s,%s](x) = %g' %(i,j,1.0*BufferedP[i,j])) 
        if BufferedP[i,j] >= MaxP:
            MaxP=1.0*BufferedP[i,j]
        AverageP=AverageP+BufferedP[i,j]  
    print('Average p(x)=%g'%(1.0*AverageP/len(BkpLinks)))
    print('p(x) <= %g\n'%MaxP)
    
    print('\nTesting with parallel processing...')
    start = time.clock()
    BufferedP = GetBufferedFailureProbPar(p, scenarios, NumScenariosValid, links, CapPerLink, BkpLinks, OptCapacity, BackupLinks)
    stop = time.clock()        
    print('[%g seconds]Done!\n'%(stop-start))
     
    AverageP=0
    MaxP=0
    for i,j in BkpLinks:
        print('p[2][%s,%s](x) = %g' %(i,j,1.0*BufferedP[i,j])) 
        if BufferedP[i,j] >= MaxP:
            MaxP=1.0*BufferedP[i,j]
        AverageP=AverageP+BufferedP[i,j]  
    print('Average p(x)=%g'%(1.0*AverageP/len(BkpLinks)))
    print('p(x) <= %g'%MaxP)   
