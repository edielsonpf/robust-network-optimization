import unittest
from NetworkOptimization.BFPBackupModel import *
from NetworkOptimization.Tools import *

class TestTools(unittest.TestCase):

    def test_get_buffer_prob(self):
        
        num_scenarios = 100000
        p=0.025
                
        G,links,nodes,num_links=GetFullConnectedNetwork(5)
        #You must change here if there is a different capacity for each link 
        cap_per_link=[1 for i in range(num_links)]
        #Adding the respective capacity for each link in the graph
        for s,d in links:
            G.add_weighted_edges_from([(s,d,cap_per_link[links.index((s,d))])])
            
        OptCapacityLoad,BackupLinksLoad,BkpLinksLoad = load('TestBackupNetDefault.dat')
        
        print('Generating %s random scenarios for failure probability test...' %(num_scenarios))
        unif_scenarios = GetUniformRandScenarios(None,num_scenarios, num_links)
        print('Done!\n')
         
        print('Generating binomial random scenarios for p=%s...'%p)
        scenarios = GetRandScenariosFromUnif(unif_scenarios, p, num_scenarios, num_links, links, cap_per_link)
        print('Done!\n')
        
        start = time.clock()
        BufferedP_Normal = GetBufferedFailureProb(None, scenarios, num_scenarios, links, BkpLinksLoad, OptCapacityLoad, BackupLinksLoad)
        stop = time.clock()        
        final_time_normal = (stop-start)
    
        start = time.clock()
        BufferedP_Parallel = GetBufferedFailureProbPar(p, num_scenarios, links, cap_per_link, BkpLinksLoad, OptCapacityLoad, BackupLinksLoad)
        stop = time.clock()        
        final_time_parallel = (stop-start)
        
        self.assertGreater(final_time_normal,final_time_parallel)
        for link in BufferedP_Normal:
            self.assertAlmostEquals(BufferedP_Normal[link], BufferedP_Parallel[link],delta=0.001)

    def test_get_rand_unif(self):
         
        G,links,nodes,num_links=GetFullConnectedNetwork(5)
        #You must change here if there is a different capacity for each link 
        cap_per_link=[1 for i in range(num_links)]
        #Adding the respective capacity for each link in the graph
        for s,d in links:
            G.add_weighted_edges_from([(s,d,cap_per_link[links.index((s,d))])])
              
        num_scenarios = 100
                 
        print('Generating %s random scenarios...' %(num_scenarios))
        unif_scenarios = GetUniformRandScenarios(None,num_scenarios, num_links)
        print('Done!\n')
         
        p=0.05
         
        print('Generating binomial random scenarios for p=%s...'%p)
        scenarios = GetRandScenariosFromUnif(unif_scenarios, p, num_scenarios, num_links, links, cap_per_link)
        print('Done!\n')
         
        NumFailures = GetNumFailures(scenarios,num_scenarios,links)
        Average1=0
        for i in range(num_scenarios):
            Average1 = Average1+1.0*NumFailures[i]/num_scenarios
             
        p=0.25
         
        print('Generating binomial random scenarios for p=%s...'%p)
        scenarios = GetRandScenariosFromUnif(unif_scenarios, p, num_scenarios, num_links, links, cap_per_link)
        print('Done!\n')
         
         
        NumFailures = GetNumFailures(scenarios,num_scenarios,links)
        Average2=0
        for i in range(num_scenarios):
            Average2=Average2+1.0*NumFailures[i]/num_scenarios   
         
        self.assertGreater(Average2, Average1, None)



if __name__ == '__main__':
    unittest.main()
