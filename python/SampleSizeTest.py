__author__ = "edielsonpf"

from math import sqrt 
import networkx as nx
from NetworkOptimization.BFPBackupModel import BFPBackup
from NetworkOptimization.BFPBackupModel_ISR import BFPBackupISR 
from NetworkOptimization.SuperquantileModel import SQModel
from NetworkOptimization.Tools import GetBufferedFailureProb, GetRandScenarios, plotGraph, GetImportanceSamplingVector, GetRandScenariosPar

from gurobipy import tuplelist

def SampleSizeTest(use_parallel,importance_sampling,plot_options,num_nodes,scenario,num_scenarios,p,p2,epsilon,mip_gap,time_limit):
        
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
        
        print('Number of links: %g\n' %(len(links)))
        G=nx.DiGraph()
        
        G.add_nodes_from(nodes)
        G.add_edges_from(links)
    
    ###########################################
    #
    #    Random Scenarios
    #
    ###########################################
    k1=num_scenarios[0]
    nobs = len(links)
    
    CapPerLink=[1 for k in range(nobs)]
      
    ###############################################
    #
    #    Buffered failure probability
    #
    ###############################################
    k4 = num_scenarios[3]
    print('Generating %s random scenarios for new failure probability test...' %(k4))
    nobs = len(links)
    
    if use_parallel == 0:
        scenarios_4 = GetRandScenarios(None, p, k4, nobs, links, CapPerLink)
    else:
        scenarios_4 = GetRandScenariosPar(p, k4, nobs, links, CapPerLink)
    print('Done!\n')
    
    ################################################################
    #    
    #                       Super Quantile
    #
    ################################################################
    if importance_sampling == 1:
    
        k2=num_scenarios[1]
        nobs = len(links)
        print('Generating new %s random scenarios for super quantile...' %(k2))
        scenarios_2 = GetRandScenarios(None, p2, k2, nobs, links, CapPerLink)
        print('Done!\n')
        
    ################################################################
    #    
    #                       Design Assessment
    #
    ################################################################
        k3 = num_scenarios[2]
        nobs = len(links)
        print('Generating %s random scenarios for design assessment...' %(k3))
        scenarios_3 = GetRandScenarios(None, p2, k3, nobs, links, CapPerLink)
        print('Done!\n')
    
    ##################################
    #
    #        Plotting Graph
    #
    #################################
    if plot_options == 1:    
        #Plot Initial Graph
        plotGraph(G,option=None,position=None)
                        
    LastOptimal = 0
    Difference = 1000
    while Difference > 0.01:
        
        print('Generating %s random scenarios...' %(k1))
      
        if importance_sampling == 0:
            scenarios_1 = GetRandScenarios(None, p, k1, nobs, links, CapPerLink)
        else:
            print('Failure probability for importance sample: %g' %p2)
            scenarios_1 = GetRandScenarios(None, p2, k1, nobs, links, CapPerLink)
          
#         for i in range(k1):
#             for s,d in links:
#                 if scenarios_1[i,s,d] > 0:
#                     G.add_weighted_edges_from([(s,d,scenarios_1[i,s,d])])
#                 else:
#                     G.add_weighted_edges_from([(s,d,scenarios_1[i,s,d])])
#         print('Done!\n')
#         
        if importance_sampling == 1:
            print('Failure probability for importance sampling: %g' %p2)
            #importance sampling
            ImpSamp_1,A1,MaxA1=GetImportanceSamplingVector(links, scenarios_1, k1, p, p2,epsilon)
            ImpSamp_2,A2,MaxA2=GetImportanceSamplingVector(links, scenarios_2, k2, p, p2,epsilon)
            ImpSamp_3,A3,MaxA3=GetImportanceSamplingVector(links, scenarios_3, k3, p, p2,epsilon)
        else:
            print('Failure probability for importance sampling: %g' %p2)
            #importance sampling
            ImpSamp_1=None
            ImpSamp_2=None
            ImpSamp_3=None
            
        print('\n=======Simulation parameters=========\n')
        print('Failure prob. (p): %g' %p)
        print('Failure prob. for IS (p2): %g' %p2)
        print('IS ratio(p2/p): %g' %(p2/p))
        print('Survivability (epsilon): %g' %epsilon)
        print('Number of random scenarios (k): %g' %(k1))
        print('=====================================\n')
        
        ################################
        #
        #    Optimization
        #
        ################################
        print('Creating model...')
        links = tuplelist(links)
        if importance_sampling == 1:
            BackupNet = BFPBackupISR(ImpSamp_1,A1,MaxA1,nodes,links,scenarios_1,epsilon,k1)
        else:
            BackupNet = BFPBackup(ImpSamp_1,nodes,links,scenarios_1,epsilon,k1)
        print('Done!\n')
        print('Solving...\n')
        OptCapacity,BackupLinks = BackupNet.optimize(mip_gap,time_limit,None)
        
        print('\nCapacity assigned per backup link:\n' )
        ChoosenLinks={}
        BkpLinks={}
        for i,j in links:
            if OptCapacity[i,j] > 0.0001:
                print('C[%s,%s]: %g' % (i,j, OptCapacity[i,j]))
                ChoosenLinks[i,j]=1
                if (len(BkpLinks) == 0):
                    BkpLinks=[(i,j)]
                else:
                    BkpLinks=BkpLinks+[(i,j)]
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
        print('\nAverage nij: %g\n' % (aux/cont))
        
        BackupNet.reset()
        
        ##############################
        #    Survivability
        ##############################
        print('\nBuffered failure probability using same scenarios used in the model:\n')
        BufferedP = GetBufferedFailureProb(ImpSamp_1, scenarios_1, k1, links, BkpLinks, OptCapacity, BackupLinks)
             
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
        
            ##############################
            #    Superquatile
            ##############################    
            print('\nCreating super quantile model...')
            
            MySQModel = SQModel(ImpSamp_2,nodes,BkpLinks,scenarios_2,epsilon,k2,BackupLinks,OptCapacity)
            print('Done!\n')
            print('Solving...\n')
            SuperQuantile, OptimalZ = MySQModel.optimize(mip_gap,time_limit,None)
            print('\nSuper quantile assigned per backup link:\n' )
            #for i,j in links:
            for i,j in BkpLinks:
                print('q[%s,%s](x)=%g' % (i,j, SuperQuantile[i,j]))
                print('z0[%s,%s]=%g' % (i,j, OptimalZ[i,j]))
            MySQModel.reset()
            
            #########################################
            #
            #        Design Assessment
            #
            #########################################        
            print('Upper bound for q(x):\n')
            u={}
            U={}
            #for i,j in links:
            for i,j in BkpLinks:
                U[i,j]=0
                for k in range(k3):
                    Psd=0
                    for s,d in links:
                        Psd=Psd+BackupLinks[i,j,s,d]*scenarios_3[k,s,d]
                    u[k,i,j]=OptimalZ[i,j]+(1/epsilon)*max((Psd-OptCapacity[i,j]-OptimalZ[i,j]),0)*ImpSamp_3[k]
                    U[i,j]=U[i,j]+u[k,i,j]
                U[i,j]=U[i,j]/k3
                print('U[%g,%g]=%g'%(i,j,U[i,j]))
            
            print('\nCalculating variance for confidence interval:\n')
            Var={}
            AverageVar=0
            AverageCount=0
            for i,j in BkpLinks:
                Var[i,j]=0
                for k in range(k3):
                    Var[i,j]=Var[i,j]+(u[k,i,j]-U[i,j])**2
                Var[i,j]=Var[i,j]/(k3-1)
                AverageVar=AverageVar+Var[i,j]
                AverageCount=AverageCount+1
                print('Var[%g,%g]=%g'%(i,j,Var[i,j]))  
                print('Confidence interval[%g,%g]=[%g,%g]'%(i,j,U[i,j]-1.96*sqrt(Var[i,j]/k3),U[i,j]+1.96*sqrt(Var[i,j]/k3)))
            print('Average variance: %g' %(AverageVar/AverageCount))    
    
        ###############################################
        #
        #    Buffered failure probability
        #
        ###############################################
        print('\nBuffered failure probability using new scenarios:\n')
        BufferedP = GetBufferedFailureProb(None, scenarios_4, k4, links, BkpLinks, OptCapacity, BackupLinks)
        print('Done!\n')
        
        AverageP=0
        MaxP=0
        for i,j in BkpLinks:
            print('p[2][%s,%s](x) = %g' %(i,j,1.0*BufferedP[i,j])) 
            if BufferedP[i,j] >= MaxP:
                MaxP=1.0*BufferedP[i,j]
            AverageP=AverageP+BufferedP[i,j]  
        print('Average p(x)=%g'%(1.0*AverageP/len(BkpLinks)))
        print('p(x) <= %g'%MaxP)
        
        k1=k1*10
        TotalCapacity=0
        for i,j in BkpLinks:
            TotalCapacity = TotalCapacity+OptCapacity[i,j]
        Difference = (LastOptimal-TotalCapacity)**2
        print('Squared error:%g'%Difference)
        LastOptimal = TotalCapacity    