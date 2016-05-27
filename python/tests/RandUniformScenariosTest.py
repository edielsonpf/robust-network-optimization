from NetworkOptimization.Tools import GetUniformRandScenarios,GetNumFailures,\
    GetRandScenariosFromUnif
import networkx as nx

if __name__ == '__main__':

    NumNodes = 5
    
    #================================================================     
    #Generates a complete indirect graph 
    H = nx.complete_graph(NumNodes)
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
        
    n4 = 5
        
    print('Generating %s random scenarios for new failure probability test...' %(n4))
    unif_scenarios = GetUniformRandScenarios(None,n4, nobs)
#     print(unif_scenarios)
    print('Done!\n')
    
    p=0.05
    
    print('Generating binomial random scenarios for p=%s...'%p)
    scenarios = GetRandScenariosFromUnif(unif_scenarios, p, n4, nobs, links, CapPerLink)
    print('Done!\n')
    
    NumFailures = GetNumFailures(scenarios,n4,links)
    for i in range(n4):
        print('Number of failures in scenario #%s=%s'%(i,NumFailures[i]))
        
    p=0.25
    
    print('Generating binomial random scenarios for p=%s...'%p)
    scenarios = GetRandScenariosFromUnif(unif_scenarios, p, n4, nobs, links, CapPerLink)
    print('Done!\n')
    
    NumFailures = GetNumFailures(scenarios,n4,links)
    for i in range(n4):
        print('Number of failures in scenario #%s=%s'%(i,NumFailures[i]))    
    