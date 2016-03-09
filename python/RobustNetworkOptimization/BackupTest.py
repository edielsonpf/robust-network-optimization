import time
from math import sqrt

# import networkx as nx

from optimizer.backup import Backup
from optimizer.pbackup import PathBackup
from optimizer.bfpbackup import BFPBackup
from optimizer.sqmodel import SQModel
from optimizer.tools import *

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

def BackupBFPModelTest(importance_sampling,plot_options,num_nodes,scenario,num_scenarios,p,p2,epsilon,mip_gap,time_limit):
        
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
        scenarios = GetRandScenarios(p, num_scenarios[0], nobs, links, CapPerLink)  
    else:
        print('Failure probability for importance sample: %g' %p2)
        scenarios = GetRandScenarios(p2, num_scenarios[0], nobs, links, CapPerLink)
        
        #Generates the importance sampling factor for each sample
        ImpSamp={}
        for i,j in links:
            for k in range(num_scenarios[0]):
                sum_failure=0
                for s,d in links:
                    sum_failure=sum_failure+scenarios[k,s,d]
                ImpSamp[k,i,j]=(p**(sum_failure)*(1-p)**(len(links)-sum_failure))/(p2**(sum_failure)*(1-p2)**(len(links)-sum_failure))
    
    stop = time.clock()
    print('[%g seconds]Done!\n'%(stop-start))
  
    ################################
    #
    #        Optimization
    #
    ################################
    print('Creating model...')
    links = tuplelist(links)
    BackupNet = BFPBackup(ImpSamp,nodes,links,scenarios,epsilon,num_scenarios[0])
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
    for i,j in BkpLinks:
        n[i,j]=0
        for s,d in links:
            if (BackupLinks[i,j,s,d] > 0.0001) & (ChoosenLinks[i,j] == 1):
                n[i,j] =(n[i,j]+BackupLinks[i,j,s,d])
        if((n[i,j] > 0) & ChoosenLinks[i,j] == 1):
#        if n[i,j] > 0:
            aux=aux+n[i,j]
            cont=cont+1
    print('\nAverage nij: %g\n' % (aux/cont))
    
    ##############################
    #    Failure probability
    ##############################
    print('\nBuffered failure probability using same scenarios used in the model:\n')
    for i,j in BkpLinks:
        Reliability = 0
        for k in range(num_scenarios[0]):
            Psd=0
            for s,d in links:
                Psd=Psd+BackupLinks[i,j,s,d]*scenarios[k,s,d]
            if Psd > OptCapacity[i,j]:
                Reliability=Reliability+1*ImpSamp[k,i,j]
        print('p[1][%s,%s](x) = %g' %(i,j,(1.0*Reliability/num_scenarios[0])))
        
    ################################################################
    #    
    #                       Super Quantile
    #
    ################################################################
    if importance_sampling == 1:
        
        print('\nGenerating new %s random scenarios for super quantile...' %(num_scenarios[1]))
        print('Failure probability for importance sampling: %g' %p2)
        
        start = time.clock()
        scenarios = GetRandScenarios(p2, num_scenarios[1], nobs, links, CapPerLink)
             
        #importance sampling
        ImpSamp={}
        for i,j in BkpLinks:
            for k in range(num_scenarios[1]):
                sum_failure=0
                for s,d in links:
                    sum_failure=sum_failure+scenarios[k,s,d]
                ImpSamp[k,i,j]=(p**(sum_failure)*(1-p)**(len(links)-sum_failure))/(p2**(sum_failure)*(1-p2)**(len(links)-sum_failure))
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
    if importance_sampling == 1:
        
        print('\nGenerating %s random scenarios for design assessment...' %(num_scenarios[2]))
        
        start = time.clock()
        scenarios = GetRandScenarios(p2, num_scenarios[2], nobs, links, CapPerLink)
        
        ImpSamp={}
        for i,j in BkpLinks:
            for k in range(num_scenarios[2]):
                sum_failure=0
                for s,d in links:
                    sum_failure=sum_failure+scenarios[k,s,d]
                ImpSamp[k,i,j]=(p**(sum_failure)*(1-p)**(len(links)-sum_failure))/(p2**(sum_failure)*(1-p2)**(len(links)-sum_failure))
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
                u[k,i,j]=OptimalZ[i,j]+(1/epsilon)*max((Psd-OptCapacity[i,j]-OptimalZ[i,j]),0)*ImpSamp[k,i,j]
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
    
    start = time.clock()
    scenarios = GetRandScenarios(p, num_scenarios[3], nobs, links, CapPerLink)
    stop = time.clock()        
    print('[%g seconds]Done!\n'%(stop-start))

    
    print('\nBuffered failure probability using new scenarios:\n')
    
    start = time.clock()
    BufferedP = GetBufferedFailureProb(scenarios, num_scenarios[3], links, BkpLinks, OptCapacity, BackupLinks)
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

#     start = time.clock()
#     BufferedP = GetBufferedFailureProbPar(p, scenarios, num_scenarios[3], links, CapPerLink, BkpLinks, OptCapacity, BackupLinks)
#     stop = time.clock()        
#     print('[%g seconds]Done!\n'%(stop-start))
#     
#     AverageP=0
#     MaxP=0
#     for i,j in BkpLinks:
#         print('p[2][%s,%s](x) = %g' %(i,j,1.0*BufferedP[i,j])) 
#         if BufferedP[i,j] >= MaxP:
#             MaxP=1.0*BufferedP[i,j]
#         AverageP=AverageP+BufferedP[i,j]  
#     print('Average p(x)=%g'%(1.0*AverageP/len(BkpLinks)))
#     print('p(x) <= %g'%MaxP)

    
#    AverageP=0
#    MaxP=0
#    for i,j in BkpLinks:
        #if OptCapacity[i,j] > 0.0001:
#        Reliability = 0
#        for k in range(num_scenarios[3]):
#            Psd=0
#            for s,d in links:
#                Psd=Psd+BackupLinks[i,j,s,d]*scenarios[k,s,d]
#            if Psd > OptCapacity[i,j]:
#                Reliability=Reliability+1
#        print('p[2][%s,%s](x) = %g' %(i,j,1.0*Reliability/num_scenarios[3])) 
#        if (1.0*Reliability/num_scenarios[3]) >= MaxP:
#            MaxP=(1.0*Reliability/num_scenarios[3])
#       AverageP=AverageP+1.0*Reliability/num_scenarios[3]  
#   print('Average p(x)=%g'%(AverageP/len(BkpLinks)))
#   print('p(x) <= %g'%MaxP)    

def EpsilonBFPModelTest(importance_sampling,plot_options,num_nodes,scenario,num_scenarios,p,p2,EpsilonList,mip_gap,time_limit):
        
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
      
    print('Generating %s random scenarios...' %(k1))
      
    if importance_sampling == 0:
        scenarios_1 = GetRandScenarios(p, k1, nobs, links, CapPerLink)
    else:
        print('Failure probability for importance sample: %g' %p2)
        scenarios_1 = GetRandScenarios(p2, k1, nobs, links, CapPerLink)
      
    for i in range(k1):
        for s,d in links:
            if scenarios_1[i,s,d] > 0:
                G.add_weighted_edges_from([(s,d,scenarios_1[i,s,d])])
            else:
                G.add_weighted_edges_from([(s,d,scenarios_1[i,s,d])])
    
    if importance_sampling == 1:
        #importance sampling
        ImpSamp_1={}
        for i,j in links:
            for k in range(k1):
                sum_failure=0
                for s,d in links:
                    sum_failure=sum_failure+scenarios_1[k,s,d]
                ImpSamp_1[k,i,j]=(p**(sum_failure)*(1-p)**(len(links)-sum_failure))/(p2**(sum_failure)*(1-p2)**(len(links)-sum_failure))
                
    print('Done!\n')

    ###############################################
    #
    #    Buffered failure probability
    #
    ###############################################
    k4 = num_scenarios[3]
    print('Generating %s random scenarios for new failure probability test...' %(k4))
    nobs = len(links)
#     Y = np.random.binomial(1, p, (k4,nobs))
    
#     capacity_4={}
#     for i,j in links:
#         Aux=1
#         for k in range(k4):
#             AuxCount = 0
#             for s,d in links:
#                 #generating capacity for each s,d link
#                 capacity_4[k,s,d] = Aux*Y[k,AuxCount]
#                 AuxCount = AuxCount+1
    scenarios_4 = GetRandScenarios(p, k4, nobs, links, CapPerLink)
            
    print('Done!\n')
    
    ################################################################
    #    
    #                       Super Quantile
    #
    ################################################################
    if importance_sampling == 1:
    
        k2=num_scenarios[1]
        print('Generating new %s random scenarios for super quantile...' %(k2))
        nobs = len(links)
        
        print('Failure probability for importance sampling: %g' %p2)
        
#         Y=stats.binom.rvs(1,p2,size=(k2,nobs))
#         
#         capacity_2={}
#         Aux=1
#         for k in range(k2):
#             AuxCount = 0
#             for s,d in links:
#                 #generating capacity for each s,d link
#                 capacity_2[k,s,d] = Aux*Y[k,AuxCount]
#                 AuxCount = AuxCount+1
        scenarios_2 = GetRandScenarios(p2, k2, nobs, links, CapPerLink)
        
        #importance sampling
        ImpSamp_2={}
        for i,j in links:
            for k in range(k2):
                sum_failure=0
                for s,d in links:
                    sum_failure=sum_failure+scenarios_2[k,s,d]
                ImpSamp_2[k,i,j]=(p**(sum_failure)*(1-p)**(len(links)-sum_failure))/(p2**(sum_failure)*(1-p2)**(len(links)-sum_failure))
                
        print('Done!\n')
        
    ################################################################
    #    
    #                       Design Assessment
    #
    ################################################################
        k3 = num_scenarios[2]
        print('Generating %s random scenarios for design assessment...' %(k3))
        nobs = len(links)
#         Y = np.random.binomial(1, p2, (k3,nobs))
        scenarios_3 = GetRandScenarios(p2, k3, nobs, links, CapPerLink)
        
        ImpSamp_3={}
#         capacity_3={}
        for i,j in links:
#             Aux=1
            for k in range(k3):
#                 AuxCount = 0
                sum_failure=0
                for s,d in links:
                    #generating capacity for each s,d link
#                     capacity_3[k,s,d] = Aux*Y[k,AuxCount]
#                     AuxCount = AuxCount+1
                    sum_failure=sum_failure+scenarios_3[k,s,d]
                ImpSamp_3[k,i,j]=(p**(sum_failure)*(1-p)**(len(links)-sum_failure))/(p2**(sum_failure)*(1-p2)**(len(links)-sum_failure))
                
        print('Done!\n')
    
    ##################################
    #
    #        Plotting Graph
    #
    #################################
    if plot_options == 1:    
        #Plot Initial Graph
        plotGraph(G,option=None,position=None)
                        
    for index in range(len(EpsilonList)):
        epsilon = EpsilonList[index]

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
        for i,j in links:
            if OptCapacity[i,j] > 0.0001:
                Reliability = 0
                for k in range(k1):
                    Psd=0
                    for s,d in links:
                        Psd=Psd+BackupLinks[i,j,s,d]*scenarios_1[k,s,d]
                    if Psd > OptCapacity[i,j]:
                        Reliability=Reliability+1*ImpSamp_1[k,i,j]
                print('p[1][%s,%s](x) = %g' %(i,j,(1.0*Reliability/k1)))
            
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
                    u[k,i,j]=OptimalZ[i,j]+(1/epsilon)*max((Psd-OptCapacity[i,j]-OptimalZ[i,j]),0)*ImpSamp_3[k,i,j]
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
        print('Buffered failure probability using new scenarios:\n')
        
        #for i,j in links:
        AverageP=0
        MaxP=0
        for i,j in BkpLinks:
            #if OptCapacity[i,j] > 0.0001:
            Reliability = 0
            for k in range(k4):
                Psd=0
                for s,d in links:
                    Psd=Psd+BackupLinks[i,j,s,d]*scenarios_4[k,s,d]
                if Psd > OptCapacity[i,j]:
                    Reliability=Reliability+1
            print('p[2][%s,%s](x) = %g' %(i,j,1.0*Reliability/k4)) 
            if (1.0*Reliability/k4) >= MaxP:
                MaxP=(1.0*Reliability/k4)
            AverageP=AverageP+1.0*Reliability/k4  
        print('Average p(x)=%g'%(AverageP/len(BkpLinks)))
        print('p(x) <= %g'%MaxP)
