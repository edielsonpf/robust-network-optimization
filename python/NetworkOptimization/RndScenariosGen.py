'''
Created on Jun 9, 2016

@author: Edielson
'''

import numpy as np
import json
import multiprocessing
from multiprocessing import Pool

def ThreadGetRand(RandSeed, FailureProb,NumScenarios, StartIndex, NumLinks, Links, CapPerLink):    
    """Generate random failure scenarios based on Binomial distribution.

    Parameters
    ----------
    RandSeed : Random seed (necessary for multiprocessing calls).
    FailureProb: Failure probability for each edge (link) in the graph.
    NumScenarios : Number of scenarios to be generated.
    StartIndex: Start index for each thread
    NumLinks: Number of edges (links) on each scenario.
    Links: Graph edges (links)
    CapPerLink: Edge (link) capacity (weight) 
    
    Returns
    -------
    Scenarios: Group of scenarios with random failure following Binomial distribution.

    """     
    if RandSeed != None:
        np.random.seed(RandSeed)
    
    Y = np.random.binomial(1, FailureProb, (NumScenarios,NumLinks))
     
    Scenarios={}
    for k in range(NumScenarios):
        Index=0
        for s,d in Links:
            Scenarios[StartIndex+k,s,d]=CapPerLink[Index]*Y[k,Index]
            Index=Index+1
    return Scenarios

class ScenariosGenerator(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
    
    def GetBinomialRand(self,RandSeed, FailureProb,NumScenarios, NumLinks, Links, CapPerLink):    
        """Generate random failure scenarios based on Binomial distribution.
    
        Parameters
        ----------
        RandSeed : Random seed (necessary for multiprocessing calls).
        FailureProb: Failure probability for each edge (link) in the graph.
        NumScenarios : Number of scenarios to be generated.
        NumLinks: Number of edges (links) on each scenario.
        Links: Graph edges (links)
        CapPerLink: Edge (link) capacity (weight) 
        
        Returns
        -------
        Scenarios: Group of scenarios with random failure following Binomial distribution.
    
        """ 
        if RandSeed != None:
            np.random.seed(RandSeed)
        
        Y = np.random.binomial(1, FailureProb, (NumScenarios,NumLinks))
         
        Scenarios={}
        for k in range(NumScenarios):
            Index=0
            for s,d in Links:
                Scenarios[k,s,d]=CapPerLink[Index]*Y[k,Index]
                Index=Index+1
        return Scenarios
    
    def GetBinomialRandPar(self,FailureProb,NumScenarios, NumLinks, Links, CapPerLink):    
        """Generate random failure scenarios based on Binomial distribution using multiprocessing.
    
        Parameters
        ----------
        FailureProb: Failure probability for each edge (link) in the graph.
        NumScenarios : Number of scenarios to be generated.
        NumLinks: Number of edges (links) on each scenario.
        Links: Graph edges (links)
        CapPerLink: Edge (link) capacity (weight) 
        
        Returns
        -------
        Scenarios: Group of scenarios with random failure following Binomial distribution.
    
        """
        
        #check the number of available processors
        nb_processes = multiprocessing.cpu_count ()
        print('Number of available processors: %g' %nb_processes)
        
        p = Pool(nb_processes)
         
        Dividend = NumScenarios/nb_processes
        Rest=NumScenarios-(nb_processes*Dividend)
        NewDivision=[0 for k in range(nb_processes)]
        args = [0 for k in range(nb_processes)]
        start=0
        for k in range(nb_processes):
            NewDivision[k]=Dividend
            if k == 0:
                NewDivision[k]=NewDivision[k]+Rest
                start=0
            else:
                start=start+NewDivision[k-1]
            RandSeed = k
            args[k]=(RandSeed, FailureProb, NewDivision[k], start, NumLinks, Links, CapPerLink)
    
        # launching multiple evaluations asynchronously *may* use more processes
        multiple_results = [p.apply_async(ThreadGetRand, (args[k])) for k in range(nb_processes)]
        
        Scenarios={}
        for res in multiple_results:
            Scenarios.update(res.get(timeout=500))
        
        return Scenarios    
    
    
    def GetImportanceSamplingVector(self,Links, Scenarios, NumScenarios, FailureProb, FailureProbIS):
        """Calculate the importance sampling vector.
        
        Parameters
        ----------
        Links: Graph edges (links)
        Scenarios: Set of scenarios with random failure following Binomial distribution.
        NumScenarios : Number of scenarios to be generated.
        FailureProb: Failure probability for each edge (link) in the graph.
        FailureProbIS: Importance sampling failure probability for each edge (link) in the graph.
        
        Returns
        -------
        Gamma: Importance sampling vector.
    
        """
        Gamma={}
        for k in range(NumScenarios):
            sum_failure=0
            for s,d in Links:
                sum_failure=sum_failure+Scenarios[k,s,d]
            Gamma[k]=(FailureProb**(sum_failure)*(1-FailureProb)**(len(Links)-sum_failure))/(FailureProbIS**(sum_failure)*(1-FailureProbIS)**(len(Links)-sum_failure))
            
        return Gamma
    
    def GetBinomialFromUnif(self,UnifScenarios,FailureProb,NumScenarios,NumLinks, Links, CapPerLink):    
        """Generate random failure scenarios based on Binomial distribution.
    
        Parameters
        ----------
        RandSeed : Random seed (necessary for multiprocessing calls).
        FailureProb: Failure probability for each edge (link) in the graph.
        NumScenarios : Number of scenarios to be generated.
        NumLinks: Number of edges (links) on each scenario.
        Links: Graph edges (links)
        CapPerLink: Edge (link) capacity (weight) 
        
        Returns
        -------
        Scenarios: Group of scenarios with random failure following Binomial distribution.
    
        """ 
        Scenarios={}
        for k in range(NumScenarios):
            Index=0
            for s,d in Links:
                Scenarios[k,s,d]=0
                if UnifScenarios[k,Index] < FailureProb:
                    Scenarios[k,s,d]=CapPerLink[Index]
                Index=Index+1
        return Scenarios
    
    def GetUniformRand(self,RandSeed, NumScenarios, NumLinks):    
        """Generate random failure scenarios based on Binomial distribution.
    
        Parameters
        ----------
        RandSeed : Random seed (necessary for multiprocessing calls).
        FailureProb: Failure probability for each edge (link) in the graph.
        NumScenarios : Number of scenarios to be generated.
        NumLinks: Number of edges (links) on each scenario.
        Links: Graph edges (links)
        CapPerLink: Edge (link) capacity (weight) 
        
        Returns
        -------
        Scenarios: Group of scenarios with random failure following Binomial distribution.
    
        """ 
        if RandSeed != None:
            np.random.seed(RandSeed)
        
        Y = np.random.uniform(0, 1, (NumScenarios,NumLinks))
        return Y
    
    def GetNumFailures(self,Scenarios, NumScenarios, Links):    
        """Calculate the sum of failures in the scenarios.
    
        Parameters
        ----------
        Scenarios: Scenarios for calculating the number of failures.
        Links: Graph edges (links)
        
        Returns
        -------
        NumFailures: Number of failures on each scenario.
    
        """
        NumFailures=[0 for i in range(NumScenarios)]
        for i in range(NumScenarios):
            for s,d in Links:
                NumFailures[i] = NumFailures[i] + Scenarios[i,s,d]
        return NumFailures
    
    def SaveRandScenario(self, file_name,scenarios): 
        """Save the optimal backup network to the file ``filename``.""" 
        
        data = {"scenarios": [scenario for scenario in scenarios],
                "scenario_status": [scenarios[scenario] for scenario in scenarios]}
        f = open(file_name, "w") 
        json.dump(data, f) 
        f.close()
        
    def LoadRandScenarios(self,file_name): 
        """Load a backup network from the file ``filename``.  
        Returns the backup network solution saved in the file. 
      
        """ 
        f = open(file_name, "r") 
        data = json.load(f) 
        f.close() 
        
        scenarios = [scenario for scenario in data["scenarios"]]
        scenarios_status = [status for status in data["scenario_status"]] 
                
        RndScenarios={}
        IndexAux=0
        for k,s,d in scenarios:
            RndScenarios[k,s,d]=scenarios_status[IndexAux]
            IndexAux=IndexAux+1
        
        return RndScenarios    