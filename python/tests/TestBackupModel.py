import unittest
from NetworkOptimization.BFPBackupModel import *
from NetworkOptimization.RndScenariosGen import *
from NetworkOptimization.Tools import *
from datetime import datetime

class TestBackupModel(unittest.TestCase):

    def test_save(self):
        
        p=0.025
        p2=2*p
        epsilon=0.01
        num_scenarios = 100
        num_nodes=5
         
        G,links,nodes,num_links=GetFullConnectedNetwork(num_nodes)
        #You must change here if there is a different capacity for each link 
        cap_per_link=[1 for i in range(num_links)]
        #Adding the respective capacity for each link in the graph
        for s,d in links:
            G.add_weighted_edges_from([(s,d,cap_per_link[links.index((s,d))])])
        
        ScenariosGen = ScenariosGenerator()
        
        unif_scenarios = ScenariosGen.GetUniformRand(None, num_scenarios, num_links)
        scenarios = ScenariosGen.GetBinomialFromUnif(unif_scenarios, p2, num_scenarios, num_links, links, cap_per_link)
            
        #Generates the importance sampling factor for each sample
        gamma=ScenariosGen.GetImportanceSamplingVector(links, scenarios, num_scenarios, p, p2)
        
        BackupNet = BFPBackupNetwork()
        BackupNet.LoadModel(gamma,nodes,links,scenarios,epsilon,num_scenarios)
        
        OptCapacity,BackupLinks,BkpLinks = BackupNet.Optimize()
        
        file_name=('%s,%s,%s,%s,%s,%s.dat'%(num_nodes,p,p2,epsilon,num_scenarios,datetime.strftime(datetime.now(), '%Y-%m-%d,%H-%M-%S')))
        BackupNet.Save(file_name)
    
        #Reseting model
        BackupNet.ResetModel()
    
        OptCapacityLoad,BackupLinksLoad,BkpLinksLoad = BackupNet.LoadBackupNetwork(file_name)
    
         
        self.assertEqual(OptCapacity, OptCapacityLoad)
        self.assertEqual(BackupLinks, BackupLinksLoad)
        
        Answer=False
        for links in BkpLinks:
            if links in BkpLinksLoad:
                Answer=True
            else:
                Answer=False
                break
                  
        self.assertTrue(Answer, None)

if __name__ == '__main__':
    unittest.main()
