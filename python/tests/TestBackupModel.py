import unittest
from NetworkOptimization.BFPBackupModel import *
from NetworkOptimization.Tools import *

class TestSaveAndLoad(unittest.TestCase):

    def test_save(self):
        
        p=0.025
        p2=2*p
        epsilon=0.01
        num_scenarios = 100
         
        G,links,nodes,num_links=GetFullConnectedNetwork(5)
        #You must change here if there is a different capacity for each link 
        cap_per_link=[1 for i in range(num_links)]
        #Adding the respective capacity for each link in the graph
        for s,d in links:
            G.add_weighted_edges_from([(s,d,cap_per_link[links.index((s,d))])])
        
        unif_scenarios = GetUniformRandScenarios(None, num_scenarios, num_links)
        scenarios = GetRandScenariosFromUnif(unif_scenarios, p2, num_scenarios, num_links, links, cap_per_link)
            
        #Generates the importance sampling factor for each sample
        gamma=GetImportanceSamplingVector(links, scenarios, num_scenarios, p, p2)
        
        BackupNet = BFPBackup()
        BackupNet.loadModel(gamma,nodes,links,scenarios,epsilon,num_scenarios)
        
        OptCapacity,BackupLinks,BkpLinks = BackupNet.optimize()
        
        BackupNet.save('TestBackupNet.dat')
    
        #Reseting model
        BackupNet.reset()
    
        OptCapacityLoad,BackupLinksLoad,BkpLinksLoad = load('TestBackupNet.dat')
    
         
        self.assertEqual(OptCapacity, OptCapacityLoad)
        self.assertEqual(BackupLinks, BackupLinksLoad)
        
        Answer=False
        for links in BkpLinks:
            if links in BkpLinksLoad:
                Answer=True
            else:
                Answer=False
                break
                  
        self.assertEqual(Answer, True)

        
    
#     def test_isupper(self):
#         self.assertTrue('FOO'.isupper())
#         self.assertFalse('Foo'.isupper())
# 
#     def test_split(self):
#         s = 'hello world'
#         self.assertEqual(s.split(), ['hello', 'world'])
#         # check that s.split fails when the separator is not a string
#         with self.assertRaises(TypeError):
#             s.split(2)
if __name__ == '__main__':
    unittest.main()
