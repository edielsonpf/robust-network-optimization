import time
from math import sqrt
import networkx as nx
# from NetworkOptimization.BFPBackupModel_ISR import BFPBackupISR
from NetworkOptimization.BFPBackupModel import BFPBackup
# from NetworkOptimization.BFPBackupModel_IS import BFPBackupIS
from NetworkOptimization.SuperquantileModel import SQModel
from NetworkOptimization.Tools import GetBufferedFailureProbPar, GetBufferedFailureProb, GetRandScenarios, plotGraph, GetImportanceSamplingVectorR,\
    GetImportanceSamplingVector
from NetworkOptimization.Tools import GetRandScenariosFromUnif, GetUniformRandScenarios
from gurobipy import tuplelist

def BFPBackupModelTest(use_parallel, importance_sampling,plot_options,num_nodes,scenario,num_scenarios,p,p2,epsilon,mip_gap,time_limit):
        
    print('\n=======Simulation parameters=========\n')
    print('Failure prob. (p): %g' %p)
    print('Failure prob. for IS (p2): %g' %p2)
    print('IS ratio(p2/p): %g' %(p2/p))
    print('Survivability (epsilon): %g' %epsilon)
    print('Number of random scenarios (k): %g' %(num_scenarios[0]))
    print('=====================================\n')
    
    ############################################
    #
    #            Creating Graphs
    #
    ############################################
    
    if scenario == 0:
        print('Scenario based on a full connected and directed graph with %s nodes.' %(num_nodes))
        
        #Generates a complete indirect graph 
        H = nx.complete_graph(num_nodes)
        # transforms the indirect graph in directed one
        G = H.to_directed()
        
        #Generates a list with all links (edges) in the graph
        links = G.edges()
        #Generates a list with all nodes (vertex) in the graph
        nodes = G.nodes() 
        
    elif scenario == 1:
        print('Scenario based on 14-node NSFNET (1991) with 14 nodes.')
        
        num_nodes=14
        
        nodes = [i+1 for i in range(14)]
    
        links=[(1,2),(1,3),(1,4),(2,1),(2,3),(2,8),(3,1),(3,2),(3,7),(4,1),(4,5),(4,9),(5,4),(5,6),(5,7),
               (6,5),(6,8),(7,3),(7,5),(7,10),(7,13),(8,2),(8,6),(8,11),(9,4),(9,12),(9,14),(10,7),
               (10,11),(11,8),(11,10),(11,12),(11,14),(12,9),(12,11),(12,13),(13,7),(13,12),(13,14),(14,9),(14,11),(14,13)]
        
        print('Number of links: %g' %(len(links)))
        G=nx.DiGraph()
        
        G.add_nodes_from(nodes)
        G.add_edges_from(links)
    
    #Check the number of links
    nobs = len(links)
    
    #You must change here if there is a different capacity for each link 
    CapPerLink=[1 for i in range(nobs)]
    
    #Adding the respective capacity for each link in the graph
    for s,d in links:
        G.add_weighted_edges_from([(s,d,CapPerLink[links.index((s,d))])])
    
    #Plotting original graph
    if plot_options == 1:    
        #Plot Initial Graph
        plotGraph(G,option=None,position=None)
            
    ###########################################
    #
    #            Random Scenarios
    #
    ###########################################
    print('\nGenerating %s random scenarios...' %(num_scenarios[0]))
        
    start = time.clock()
    if importance_sampling == 0:
        scenarios = GetRandScenarios(None, p, num_scenarios[0], nobs, links, CapPerLink)
        ImpSamp=None  
    else:
        print('Failure probability for importance sample: %g' %p2)
#         scenarios = GetRandScenarios(None, p2, num_scenarios[0], nobs, links, CapPerLink)
        unif_scenarios = GetUniformRandScenarios(None, num_scenarios[0], nobs)
        scenarios = GetRandScenariosFromUnif(unif_scenarios, p2, num_scenarios[0], nobs, links, CapPerLink)
            
        #Generates the importance sampling factor for each sample
#         Gamma,A,MaxA,ScaledGamma=GetImportanceSamplingVectorR(links, scenarios, num_scenarios[0], p, p2,epsilon)
        Gamma,ScaledGamma=GetImportanceSamplingVector(links, scenarios, num_scenarios[0], p, p2)
        ImpSamp = ScaledGamma
    stop = time.clock()
    print('[%g seconds]Done!\n'%(stop-start))
    ################################
    #
    #        Optimization
    #
    ################################
    print('Creating model...')
    links = tuplelist(links)
    BackupNet = BFPBackup()
    BackupNet.loadModel(ImpSamp,nodes,links,scenarios,epsilon,num_scenarios[0])
    print('Done!\n')
    print('Solving...\n')
    OptCapacity,BackupLinks,BkpLinks,LHS = BackupNet.optimize(mip_gap,time_limit,None)
    
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
    print('\nBuffered failure probability using same scenarios used in the model:\n')
    BufferedP = GetBufferedFailureProb(ImpSamp, scenarios, num_scenarios[0], links, BkpLinks, OptCapacity, BackupLinks)
         
    AverageP=0
    MaxP=0
    for i,j in BkpLinks:
        print('p[1][%s,%s](x) = %g' %(i,j,1.0*BufferedP[i,j])) 
        if BufferedP[i,j] >= MaxP:
            MaxP=1.0*BufferedP[i,j]
        AverageP=AverageP+BufferedP[i,j]  
    print('Average p(x)=%g'%(1.0*AverageP/len(BkpLinks)))
    print('p(x) <= %g'%MaxP)        
    
    
    if importance_sampling == 1:
        ################################################################
        #    
        #                       Super Quantile
        #
        ################################################################
        
        print('\nGenerating new %s random scenarios for super quantile...' %(num_scenarios[1]))
        print('Failure probability for importance sampling: %g' %p2)
        
        start = time.clock()
        scenarios = GetRandScenarios(None, p2, num_scenarios[1], nobs, links, CapPerLink)
             
        #importance sampling
        Gamma,A,MaxA,ScaledGamma=GetImportanceSamplingVectorR(links, scenarios, num_scenarios[1], p, p2,epsilon)
        ImpSamp = ScaledGamma
        stop = time.clock()        
        print('[%g seconds]Done!\n'%(stop-start))
            
        print('Creating super quantile model...')
        MySQModel = SQModel(ImpSamp,nodes,BkpLinks,scenarios,epsilon,num_scenarios[1],BackupLinks,OptCapacity)
        print('Done!\n')
        print('Solving...\n')
        SuperQuantile, OptimalZ = MySQModel.optimize(mip_gap,time_limit,None)
        
        print('\nSuper quantile assigned per backup link:\n' )
        for i,j in BkpLinks:
            print('q[%s,%s](x)=%g' % (i,j, SuperQuantile[i,j]))
            print('z0[%s,%s]=%g' % (i,j, OptimalZ[i,j]))
    
        #########################################
        #
        #        Design Assessment
        #
        #########################################        
        print('\nGenerating %s random scenarios for design assessment...' %(num_scenarios[2]))
        
        start = time.clock()
        scenarios = GetRandScenarios(None, p2, num_scenarios[2], nobs, links, CapPerLink)
        Gamma,A,MaxA,ScaledGamma=GetImportanceSamplingVectorR(links, scenarios, num_scenarios[2], p, p2,epsilon)
        ImpSamp=ScaledGamma
        stop = time.clock()        
        print('[%g seconds]Done!\n'%(stop-start))
        
        print('Upper bound for q(x):\n')
        u={}
        U={}
        for i,j in BkpLinks:
            U[i,j]=0
            for k in range(num_scenarios[2]):
                Psd=0
                for s,d in links:
                    Psd=Psd+BackupLinks[i,j,s,d]*scenarios[k,s,d]
                u[k,i,j]=OptimalZ[i,j]+(1/epsilon)*max((Psd-OptCapacity[i,j]-OptimalZ[i,j]),0)*ImpSamp[k]
                U[i,j]=U[i,j]+u[k,i,j]
            U[i,j]=U[i,j]/num_scenarios[2]
            print('U[%g,%g]=%g'%(i,j,U[i,j]))
        
        print('\nCalculating variance for confidence interval:\n')
        Var={}
        AverageVar=0
        AverageCount=0
        #for i,j in links:
        for i,j in BkpLinks:
            Var[i,j]=0
            for k in range(num_scenarios[2]):
                Var[i,j]=Var[i,j]+(u[k,i,j]-U[i,j])**2
            Var[i,j]=Var[i,j]/(num_scenarios[2]-1)
            AverageVar=AverageVar+Var[i,j]
            AverageCount=AverageCount+1
            print('Var[%g,%g]=%g'%(i,j,Var[i,j]))  
            print('Confidence interval[%g,%g]=[%g,%g]'%(i,j,U[i,j]-1.96*sqrt(Var[i,j]/num_scenarios[2]),U[i,j]+1.96*sqrt(Var[i,j]/num_scenarios[2])))
        print('Average variance: %g' %(AverageVar/AverageCount))    
    
    ###############################################
    #
    #    Actual buffered failure probability
    #
    ###############################################
    print('\nGenerating %s random scenarios for new failure probability test...' %(num_scenarios[3]))
        
    if use_parallel == 0:
        print('Normal operation!\n')
        start = time.clock()
        scenarios = GetRandScenarios(None, p, num_scenarios[3], nobs, links, CapPerLink)
        BufferedP = GetBufferedFailureProb(None, scenarios, num_scenarios[3], links, BkpLinks, OptCapacity, BackupLinks)
         
    else:
        print('Using parallel processing!!\n')
        start = time.clock()
        BufferedP = GetBufferedFailureProbPar(p, num_scenarios[3], links, CapPerLink, BkpLinks, OptCapacity, BackupLinks)
        
    stop = time.clock()        
    print('[%g seconds]Done!\n'%(stop-start))
    
    print('\nBuffered failure probability using new scenarios:\n')
    AverageP=0
    MaxP=0
    for i,j in BkpLinks:
        print('p[2][%s,%s](x) = %g' %(i,j,1.0*BufferedP[i,j])) 
        if BufferedP[i,j] >= MaxP:
            MaxP=1.0*BufferedP[i,j]
        AverageP=AverageP+BufferedP[i,j]  
    print('Average p(x)=%g'%(1.0*AverageP/len(BkpLinks)))
    print('p(x) <= %g'%MaxP)    