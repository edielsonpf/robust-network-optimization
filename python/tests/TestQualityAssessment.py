'''
Created on Jun 9, 2016

@author: Edielson
'''
import unittest
import time
from NetworkOptimization.BFPBackupModel import BFPBackupNetwork
from NetworkOptimization.QualityAssessment import QoS
from NetworkOptimization.RndScenariosGen import ScenariosGenerator
from NetworkOptimization import Tools


class Test(unittest.TestCase):


    def test_get_buffer_prob(self):
        print('\n######### Testing GetBufferedFailureProb method #########\n')
        num_scenarios = 100000
        p=0.025
        num_nodes = 5
        file_name = 'TestBackupNetDefault.dat'
                
        G,links,nodes,num_links=Tools.GetFullConnectedNetwork(num_nodes)
        #You must change here if there is a different capacity for each link 
        cap_per_link=[1 for i in range(num_links)]
        #Adding the respective capacity for each link in the graph
        for s,d in links:
            G.add_weighted_edges_from([(s,d,cap_per_link[links.index((s,d))])])
            
        
        BackupNet = BFPBackupNetwork()
        OptCapacityLoad,BackupLinksLoad,BkpLinksLoad = BackupNet.LoadBackupNetwork(file_name)
        
        ScenariosGen = ScenariosGenerator()
        print('Generating %s random scenarios for failure probability test...' %(num_scenarios))
        unif_scenarios = ScenariosGen.GetUniformRand(None,num_scenarios, num_links)
        print('Done!\n')
         
        print('Generating binomial random scenarios for p=%s...'%p)
        scenarios = ScenariosGen.GetBinomialFromUnif(unif_scenarios, p, num_scenarios, num_links, links, cap_per_link)
        print('Done!\n')
        
        SolutionQos = QoS()
        start = time.clock()
        BufferedP_Normal,Indicator = SolutionQos.GetBufferedFailureProb(None, scenarios, num_scenarios, links, BkpLinksLoad, OptCapacityLoad, BackupLinksLoad)
        stop = time.clock()        
        final_time_normal = (stop-start)
    
        start = time.clock()
        BufferedP_Parallel = SolutionQos.GetBufferedFailureProbPar(p, num_scenarios, links, cap_per_link, BkpLinksLoad, OptCapacityLoad, BackupLinksLoad)
        stop = time.clock()        
        final_time_parallel = (stop-start)
        
        print('%g > %g'%(final_time_normal,final_time_parallel))
        self.assertGreater(final_time_normal,final_time_parallel)
        
        for link in BufferedP_Normal:
            self.assertAlmostEquals(BufferedP_Normal[link], BufferedP_Parallel[link],delta=0.01)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()