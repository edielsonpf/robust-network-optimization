import networkx as nx
from NetworkOptimization.BFPBackupModel import BFPBackup
from gurobipy import tuplelist
import time
from NetworkOptimization.Tools import GetRandScenarios, GetBufferedFailureProbPar, GetBufferedFailureProb, GetImportanceSamplingVector

def ParallelValidation(NumNodes, NumScenarios, p, p2, epsilon, MipGap, TimeLimit):

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
    
    print('Generating %g scenarios with importance sample of %g...'%(NumScenarios[0],p2))
    scenarios = GetRandScenarios(None, p2, NumScenarios[0], nobs, links, CapPerLink)
    
    #Generates the importance sampling factor for each sample
    ImpSamp=GetImportanceSamplingVector(links, scenarios, NumScenarios[0], p, p2)
    
    print('Creating model...')
    links = tuplelist(links)
    BackupNet = BFPBackup(ImpSamp,nodes,links,scenarios,epsilon,NumScenarios[0])
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
        
    print('\nGenerating %g random scenarios for new failure probability test...' %NumScenarios[1])
    
    start = time.clock()
    scenarios = GetRandScenarios(None, p, NumScenarios[1], nobs, links, CapPerLink)
    print('Done!\n')    
    
    print('\nBuffered failure probability using new scenarios:\n')
    BufferedP = GetBufferedFailureProb(None, scenarios, NumScenarios[1], links, BkpLinks, OptCapacity, BackupLinks)
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
    BufferedP = GetBufferedFailureProbPar(p, NumScenarios[1], links, CapPerLink, BkpLinks, OptCapacity, BackupLinks)
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
