import unittest
from NetworkOptimization.RndScenariosGen import ScenariosGenerator
from NetworkOptimization import Tools

class TestRandScenariosGen(unittest.TestCase):

    def test_GetUnifRand(self):
    
        num_nodes=5
        num_scenarios = 100
         
        G,links,nodes,num_links=Tools.GetFullConnectedNetwork(num_nodes)
        #You must change here if there is a different capacity for each link 
        cap_per_link=[1 for i in range(num_links)]
        #Adding the respective capacity for each link in the graph
        for s,d in links:
            G.add_weighted_edges_from([(s,d,cap_per_link[links.index((s,d))])])
        
        RndScenarios = ScenariosGenerator()         
        print('Generating %s random scenarios...' %(num_scenarios))
        unif_scenarios = RndScenarios.GetUniformRand(None,num_scenarios, num_links)
        print('Done!\n')
         
        p=0.05
         
        print('Generating binomial random scenarios for p=%s...'%p)
        scenarios = RndScenarios.GetBinomialFromUnif(unif_scenarios, p, num_scenarios, num_links, links, cap_per_link)
        print('Done!\n')
         
        NumFailures = RndScenarios.GetNumFailures(scenarios,num_scenarios,links)
        Average1=0
        for i in range(num_scenarios):
            Average1 = Average1+1.0*NumFailures[i]/num_scenarios
             
        p=0.25
         
        print('Generating binomial random scenarios for p=%s...'%p)
        scenarios = RndScenarios.GetBinomialFromUnif(unif_scenarios, p, num_scenarios, num_links, links, cap_per_link)
        print('Done!\n')
         
         
        NumFailures = RndScenarios.GetNumFailures(scenarios,num_scenarios,links)
        Average2=0
        for i in range(num_scenarios):
            Average2=Average2+1.0*NumFailures[i]/num_scenarios   
         
        self.assertGreater(Average2, Average1, None)

    def testSaveandLoad(self):
        
        seed=0
        file_name = 'TestUnifRandScenario.dat'
        num_scenarios = 100
        num_nodes = 5
        p=0.025
        p2=5*p
        
        G,links,nodes,num_links=Tools.GetFullConnectedNetwork(num_nodes)
        #You must change here if there is a different capacity for each link 
        cap_per_link=[1 for i in range(num_links)]
        #Adding the respective capacity for each link in the graph
        for s,d in links:
            G.add_weighted_edges_from([(s,d,cap_per_link[links.index((s,d))])])
            
        ScenariosGen = ScenariosGenerator()
        
        unif_scenarios = ScenariosGen.GetUniformRand(seed, num_scenarios, num_links)
        scenarios = ScenariosGen.GetBinomialFromUnif(unif_scenarios, p2, num_scenarios, num_links, links, cap_per_link)
        
        ScenariosGen.SaveRandScenario(file_name, scenarios)
        
        loadedScenarios = ScenariosGen.LoadRandScenarios(file_name)
        
        self.assertEqual(scenarios, loadedScenarios)
            
                    
if __name__ == '__main__':
    unittest.main()
