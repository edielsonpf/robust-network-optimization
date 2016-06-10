import time
from math import sqrt

from NetworkOptimization.BFPBackupModel import BFPBackupNetwork
from NetworkOptimization.RndScenariosGen import ScenariosGenerator
from NetworkOptimization.QualityAssessment import QoS
from NetworkOptimization.SuperquantileModel import SQModel
from NetworkOptimization import Tools


def BFPBackupModelExample(use_parallel,importance_sampling,plot_options,num_nodes,scenario,num_scenarios,p,p2,epsilon,mip_gap,time_limit):
        
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
        
        G,links,nodes,num_links=Tools.GetFullConnectedNetwork(num_nodes)
                 
    elif scenario == 1:
        print('Scenario based on 14-node NSFNET (1991) with 14 nodes.')
        G,links,nodes,num_links=Tools.GetFSNETNetwork()
            
    #You must change here if there is a different capacity for each link 
    CapPerLink=[1 for i in range(num_links)]
    
    #Adding the respective capacity for each link in the graph
    for s,d in links:
        G.add_weighted_edges_from([(s,d,CapPerLink[links.index((s,d))])])
    
    #Plotting original graph
    if plot_options == 1:    
        #Plot Initial Graph
        Tools.plotGraph(G,option=None,position=None)
            
    ###########################################
    #
    #            Random Scenarios
    #
    ###########################################
    print('\nGenerating %s random scenarios...' %(num_scenarios[0]))
        
    ScenariosGen=ScenariosGenerator()
    start = time.clock()
    if importance_sampling == 0:
        scenarios = ScenariosGen.GetBinomialRand(None, p, num_scenarios[0], num_links, links, CapPerLink)
        gamma=None  
    else:
        print('Failure probability for importance sample: %g' %p2)
#         scenarios = GetRandScenarios(None, p2, num_scenarios[0], num_links, links, CapPerLink)
        unif_scenarios = ScenariosGen.GetUniformRand(None, num_scenarios[0], num_links)
        scenarios = ScenariosGen.GetBinomialFromUnif(unif_scenarios, p2, num_scenarios[0], num_links, links, CapPerLink)
        #Generates the importance sampling factor for each sample
        gamma=ScenariosGen.GetImportanceSamplingVector(links, scenarios, num_scenarios[0], p, p2)
    stop = time.clock()
    print('[%g seconds]Done!\n'%(stop-start))
    
    ################################
    #        Optimization
    ################################
    print('Creating model...')
    BackupNet = BFPBackupNetwork()
    BackupNet.LoadModel(gamma,nodes,links,scenarios,epsilon,num_scenarios[0])
    print('Done!\n')
    print('Solving...\n')
    OptCapacity,BkpRoutes,BkpLinks = BackupNet.Optimize(mip_gap,time_limit,None)
    
    #Reseting model
    BackupNet.ResetModel()
        
    print('\nCapacity assigned per backup link:\n' )
    for i,j in BkpLinks:
        print('C[%s,%s]: %g' % (i,j, OptCapacity[i,j]))
    
    SolutionQos=QoS()
    
    AvgNij=SolutionQos.GetAvgLinksPerBackupLink(BkpLinks, BkpRoutes, links)             
    print('\nAverage nij: %g\n' % (AvgNij))
    
    print('\nGenerating %s random scenarios for new failure probability test...' %(num_scenarios[3]))
    start = time.clock()
    if use_parallel == 0:
        print('Normal operation!\n')
        scenarios_test = ScenariosGen.GetBinomialRand(None, p2, num_scenarios[3], num_links, links, CapPerLink)
        gamma_test = ScenariosGen.GetImportanceSamplingVector(links, scenarios, num_scenarios[3], p, p2)
        BufferedP = SolutionQos.GetBufferedFailureProb(gamma_test, scenarios_test, num_scenarios[3], links, BkpLinks, OptCapacity, BkpRoutes)
         
    else:
        print('Using parallel processing!!\n')
        BufferedP = SolutionQos.GetBufferedFailureProbPar(p, num_scenarios[3], links, CapPerLink, BkpLinks, OptCapacity, BkpRoutes)
        
    stop = time.clock()        
    print('[%g seconds]Done!\n'%(stop-start))
    
    print('\nBuffered failure probability using new scenarios:\n')
    for i,j in BkpLinks:
        print('p(x)[%s,%s] = %g' %(i,j,1.0*BufferedP[i,j])) 
     
    if importance_sampling == 1:
        ################################################################
        #    
        #                       Super Quantile
        #
        ################################################################
        
        print('\nGenerating new %s random scenarios for super quantile...' %(num_scenarios[1]))
        print('Failure probability for importance sampling: %g' %p2)
        
        start = time.clock()
        scenarios = ScenariosGen.GetBinomialRand(None, p2, num_scenarios[1], num_links, links, CapPerLink)
        #importance sampling
        gamma=ScenariosGen.GetImportanceSamplingVector(links, scenarios, num_scenarios[1], p, p2)
        stop = time.clock()        
        print('[%g seconds]Done!\n'%(stop-start))
            
        print('Creating super quantile model...')
        MySQModel = SQModel(gamma,nodes,BkpLinks,scenarios,epsilon,num_scenarios[1],BkpRoutes,OptCapacity)
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
        scenarios = ScenariosGen.GetBinomialRand(None, p2, num_scenarios[2], num_links, links, CapPerLink)
        gamma=ScenariosGen.GetImportanceSamplingVector(links, scenarios, num_scenarios[2], p, p2)
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
                    Psd=Psd+BkpRoutes[i,j,s,d]*scenarios[k,s,d]
                u[k,i,j]=OptimalZ[i,j]+(1/epsilon)*max((Psd-OptCapacity[i,j]-OptimalZ[i,j]),0)*gamma[k]
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
        
if __name__ == '__main__':
    
    #constant for choosing to plot (1) or not to plot (0) the graphs
    PlotOptions = 0
    
    #definition of the number of nodes in the network
    NumNodes = 5
    
    #definition of the link failure probability
    p=0.025
    
    #definition of the desired survivability (epsilon)
    epsilon = 0.01
    
    #Optimization definitions
    #definition of the desired MipGap, or None for optimal
    MipGap = None
    #definition of the time limit, or None for no time limit
    TimeLimit = None
    
    #definition of the number of scenarios on each step:
    # 1- Number of scenarios for the optimization model
    # 2- Number of scenarios for superquantile model (calculus of CVaR)
    # 3- Number of scenarios for design assessment (confidence interval)
    # 4- Number of scenarios for buffered failure probability 
    NumScenarios = [100,100000,10000,100000]
    
    #Choose scenario 0 for a full directed graph with the number of nodes equal to the value of the variable NumNodes
    #or choose 1 to the NSFNET network with 14 nodes
    Scenario=0
    
    #Choose 1 to indicate the use of importance sampling and 0 otherwise
    ImportanceSampling=1
    #Choose 1 to indicate the use of multiprocessing methods and 0 otherwise
    UseParallel = 1
    #If using importance sampling, define here the failure probability ratio
    p2=1.25*p
    
    print('Buffered failure probability-based backup model')
    BFPBackupModelExample(UseParallel, ImportanceSampling,PlotOptions, NumNodes, Scenario, NumScenarios, p,p2, epsilon, MipGap, TimeLimit)