import numpy as np
import math
import networkx as nx
from NetworkOptimization.BFPBackupModel import BFPBackup
from NetworkOptimization.Tools import GetBufferedFailureProb, GetImportanceSamplingVector, GetRandScenariosFromUnif, GetUniformRandScenarios
from NetworkOptimization.Tools import GetConfidenceInterval, GetVariance, GetConfidenceInterval2
from gurobipy import tuplelist

def GetScenarios(Scenarios,NumScenarios, NumLinks, Links, CapPerLink):    
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
     
    NewScenarios={}
    k=0
    for EachScenario in Scenarios:
        Index=0
        for s,d in Links:
            NewScenarios[k,s,d]=CapPerLink[Index]*EachScenario[Index]
            Index=Index+1
        k=k+1    
    return NewScenarios

def GetIndicator(Scenarios, NumScenarios, Links, BackupLinks, CapPerBackupLink, OptBackupLinks):    
    """Calculate the buffered failure probability.

    Parameters
    ----------
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
                P[i,j]=P[i,j]+1
        P[i,j]=1.0*P[i,j]
    return P

def per(n):
    for i in range(1<<n):
        s=bin(i)[2:]
        s='0'*(n-len(s))+s
        print map(int,list(s))
                                        
if __name__=="__main__":
   
    ########################################################################
    p=0.025
    p2=5*p
    epsilon=0.1
    num_scenarios = 100
    n2=1000000
    num_nodes=5
    
    print('\n=======Simulation parameters=========\n')
    print('Failure prob. (p): %g' %p)
    print('Failure prob. for IS (p2): %g' %p2)
    print('IS ratio(p2/p): %g' %(p2/p))
    print('Survivability (epsilon): %g' %epsilon)
    print('Number of random scenarios (k): %g' %(num_scenarios))
    print('=====================================\n')
    
    ############################################
    #
    #            Creating Graphs
    #
    ############################################
    
    print('Scenario based on a full connected and directed graph with %s nodes.' %(num_nodes))
    
    #Generates a complete indirect graph 
    H = nx.complete_graph(num_nodes)
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
    
    #Adding the respective capacity for each link in the graph
    for s,d in links:
        G.add_weighted_edges_from([(s,d,CapPerLink[links.index((s,d))])])
    
    ###########################################
    #
    #            Random Scenarios
    #
    ###########################################
    print('\nGenerating %s random scenarios...' %(num_scenarios))
        
    unif_scenarios = GetUniformRandScenarios(None, num_scenarios, nobs)
    scenarios = GetRandScenariosFromUnif(unif_scenarios, p2, num_scenarios, nobs, links, CapPerLink)
            
    Gamma=GetImportanceSamplingVector(links, scenarios, num_scenarios, p, p2)
    ImpSamp = Gamma
    
    print('Done!\n')
    ################################
    #
    #        Optimization
    #
    ################################
    print('Creating model...')
    links = tuplelist(links)
    BackupNet = BFPBackup()
    BackupNet.loadModel(ImpSamp,nodes,links,scenarios,epsilon,num_scenarios)
    print('Done!\n')
    print('Solving...\n')
    OptCapacity,BackupLinks,BkpLinks = BackupNet.optimize(None,None,None)
    
    print('\nCapacity assigned per backup link:\n' )
    for i,j in BkpLinks:
        if OptCapacity[i,j] > 0.0001:
            print('C[%s,%s]: %g' % (i,j, OptCapacity[i,j]))
                 
    n={}
    aux=0
    cont=0
    for i,j in BkpLinks:
        n[i,j]=0
        for s,d in links:
            n[i,j] =(n[i,j]+BackupLinks[i,j,s,d])
        if(n[i,j] > 0):
            aux=aux+n[i,j]
            cont=cont+1
    AvgNij=(aux/cont)
    print('\nAverage nij: %g\n' % (AvgNij))
     
    #Reseting model
    BackupNet.reset()
    
    ##############################
    #    Failure probability
    ##############################
    print('Failure probability for importance sample: %g' %p2)
    
    print('\nGenerating %s uniform random scenarios for new failure probability test...' %(n2))
    test_unif_scenarios = GetUniformRandScenarios(None, n2, nobs)
    print('Done!\n')        
    
    print('\nGenerating binomial scenarios from uniform with failure probability of %g...'%p2)
    test_scenarios = GetRandScenariosFromUnif(test_unif_scenarios, p2, n2, nobs, links, CapPerLink)
    test_gamma=GetImportanceSamplingVector(links, test_scenarios, n2, p, p2)
    print('Done!\n')        
    
    print('\nBuffered failure probability using IS:\n')     
    BufferedP,Indicator = GetBufferedFailureProb(test_gamma, test_scenarios, n2, links, BkpLinks, OptCapacity, BackupLinks)
          
#     ConfidenceInterval={}
    for i,j in BkpLinks:
        print('p[1][%s,%s](x) = %g' %(i,j,1.0*BufferedP[i,j]))
#         ConfidenceInterval[i,j]=1.96*np.sqrt((BufferedP[i,j])*(1-BufferedP[i,j]))/(np.sqrt(n2)) 
    
#     print('\nConfidence interval')
#     ConfidenceInterval=GetConfidenceInterval(BkpLinks, BufferedP, None, n2)
#     for i,j in BkpLinks:
#         print('[1][%s,%s] = [%g,%g]'%(i,j,BufferedP[i,j]-ConfidenceInterval[i,j],BufferedP[i,j]+ConfidenceInterval[i,j]))
        
    print('\nVariance:\n')
    Variance_IS = GetVariance(test_gamma, test_scenarios, n2, links, BkpLinks, OptCapacity, BackupLinks,BufferedP,Indicator)
    for i,j in BkpLinks:
        print('Var[1][%s,%s] = %g'%(i,j,Variance_IS[i,j]))  
        
    print('\nConfidence interval')
    ConfidenceInterval=GetConfidenceInterval2(BkpLinks, Variance_IS, None, n2)
    for i,j in BkpLinks:
        print('[1][%s,%s] = %g,%g'%(i,j,BufferedP[i,j]-ConfidenceInterval[i,j],BufferedP[i,j]+ConfidenceInterval[i,j]))
    
    
    ###############################################
    #
    #    Actual buffered failure probability
    #
    ###############################################
    print('\nGenerating binomial scenarios from uniform with failure probability of %g...'%p)
    test_scenarios = GetRandScenariosFromUnif(test_unif_scenarios, p, n2, nobs, links, CapPerLink)
    print('Done!')
    
    print('\nBuffered failure probability with no IS:\n')
    BufferedP,Indicator = GetBufferedFailureProb(None, test_scenarios, n2, links, BkpLinks, OptCapacity, BackupLinks)
 
#     ConfidenceInterval={}
    for i,j in BkpLinks:
        print('p[2][%s,%s](x) = %g' %(i,j,1.0*BufferedP[i,j]))
#         ConfidenceInterval[i,j]=1.96*np.sqrt((BufferedP[i,j])*(1-BufferedP[i,j]))/(np.sqrt(n2)) 
    
#     print('\nConfidence interval')
#     ConfidenceInterval=GetConfidenceInterval(BkpLinks, BufferedP, None, n2)
#     for i,j in BkpLinks:
#         print('[2,1][%s,%s] = [%g,%g]'%(i,j,BufferedP[i,j]-ConfidenceInterval[i,j],BufferedP[i,j]+ConfidenceInterval[i,j]))     

    print('\nVariance:\n')
    Variance = GetVariance(test_gamma, test_scenarios, n2, links, BkpLinks, OptCapacity, BackupLinks,BufferedP,Indicator)
    for i,j in BkpLinks:
        print('Var[2][%s,%s] = %g'%(i,j,Variance[i,j]))  
        
    print('\nConfidence Interval:\n')
    ConfidenceInterval=GetConfidenceInterval2(BkpLinks, Variance, None, n2)
    for i,j in BkpLinks:
        print('[2][%s,%s] = %g,%g'%(i,j,BufferedP[i,j]-ConfidenceInterval[i,j],BufferedP[i,j]+ConfidenceInterval[i,j]))
    
    
    print('\nVariance Ratio:\n')
    for i,j in BkpLinks:
        print('Var_Ratio[%s,%s] = %g'%(i,j,1.0*(Variance/Variance_IS)))
    
    
    print('\n######################################################\n')
    
    print('Generating combinations...')
    L=20
    Num_S=np.zeros(L+1)
    for n in xrange(L+1):
        Num_S[n]=math.factorial(L)/(math.factorial(n)*math.factorial(L-n))
        
    S0=[]
    S1=[]
    S2=[]
    S3=[]
    S4=[]
    S5=[]
    S6=[]
    S7=[]
    S8=[]
    S9=[]
    S10=[]
    S11=[]
    S12=[]
    S13=[]
    S14=[]
    S15=[]
    S16=[]
    S17=[]
    S18=[]
    S19=[]
    S20=[]
    
    for i in range(1<<n):
        s=bin(i)[2:]
        s='0'*(n-len(s))+s
        aux = map(int,list(s))
        aux_sum=np.sum(aux)
        
        if aux_sum == 0:
            S0.append(aux)
        elif aux_sum == 1:
            S1.append(aux)
        elif aux_sum == 2:
            S2.append(aux)
        elif aux_sum == 3:
            S3.append(aux)
        elif aux_sum == 4:
            S4.append(aux)
        elif aux_sum == 5:
            S5.append(aux)
        elif aux_sum == 6:
            S6.append(aux)
        elif aux_sum == 7:
            S7.append(aux)
        elif aux_sum == 8:
            S8.append(aux)
        elif aux_sum == 9:
            S9.append(aux)
        elif aux_sum == 10:
            S10.append(aux)
        elif aux_sum == 11:
            S11.append(aux)
        elif aux_sum == 12:
            S12.append(aux)
        elif aux_sum == 13:
            S13.append(aux)
        elif aux_sum == 14:
            S14.append(aux)
        elif aux_sum == 15:
            S15.append(aux)
        elif aux_sum == 16:
            S16.append(aux)
        elif aux_sum == 17:
            S17.append(aux)
        elif aux_sum == 18:
            S18.append(aux)
        elif aux_sum == 19:
            S19.append(aux)
        elif aux_sum == 20:
            S20.append(aux)
    print('Done!\n')        

    Sum={}
    for i,j in BkpLinks:
        Sum[i,j]=0
    
    for k in xrange(L+1):
        if k == 0:
            Scenarios = S0
        elif k == 1:
            Scenarios =S1
        elif k == 2:
            Scenarios =S2
        elif k == 3:
            Scenarios =S3
        elif k == 4:
            Scenarios =S4
        elif k == 5:
            Scenarios =S5
        elif k == 6:
            Scenarios =S6
        elif k == 7:
            Scenarios =S7
        elif k == 8:
            Scenarios =S8
        elif k == 9:
            Scenarios =S9
        elif k == 10:
            Scenarios =S10
        elif k == 11:
            Scenarios =S11
        elif k == 12:
            Scenarios =S12
        elif k == 13:
            Scenarios =S13
        elif k == 14:
            Scenarios =S14
        elif k == 15:
            Scenarios =S15
        elif k == 16:
            Scenarios =S16
        elif k == 17:
            Scenarios =S17
        elif k == 18:
            Scenarios =S18
        elif k == 19:
            Scenarios =S19
        else:
            Scenarios =S20
        
        IS=(p**k)*(1-p)**(L-k)
        NewScenarios = GetScenarios(Scenarios, int(Num_S[k]), nobs, links, CapPerLink)
        print('IS[%s]=%g'%(k,IS)) 
        
        Indicator = GetIndicator(NewScenarios, int(Num_S[k]), links, BkpLinks, OptCapacity, BackupLinks)
        for i,j in BkpLinks:
            Sum[i,j]=Sum[i,j]+Indicator[i,j]*IS
#             print('Indicator[%s,%s] = %g' %(i,j,1.0*Indicator[i,j]))
        
    print('\nReal failure probability')
    for i,j in BkpLinks:
        print('[%s,%s] = %g'%(i,j,Sum[i,j]))  