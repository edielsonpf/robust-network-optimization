'''
Created on Jun 9, 2016

@author: Edielson
'''
import unittest
import time
import math 
import numpy as np

from NetworkOptimization.BFPBackupModel import BFPBackupNetwork
from NetworkOptimization.QualityAssessment import QoS
from NetworkOptimization.RndScenariosGen import ScenariosGenerator
from NetworkOptimization import Tools

def GetScenarios(Scenarios,NumScenarios, NumLinks, Links, CapPerLink):    
    """Generate random failure scenarios based on Binomial distribution.

    Parameters
    ----------
    NumScenarios : Number of scenarios to be generated.
    NumLinks: Number of edges (links) on each scenario.
    Links: Graph edges (links)
    CapPerLink: Edge (link) capacity (weight) 
    
    Returns
    -------
    Scenarios: Group of scenarios with random failure following Binomial distribution.

    """ 
    NewScenarios={}
    k=0
    for EachScenario in Scenarios:
        Index=0
        for s,d in Links:
            NewScenarios[k,s,d]=CapPerLink[Index]*EachScenario[Index]
            Index=Index+1
        k=k+1    
    return NewScenarios

def GetIndicator(Scenarios, NumScenarios, Links, BackupLinks, CapPerBackupLink, BackupRoutes):    
    """Calculate the buffered failure probability.

    Parameters
    ----------
    Scenarios: Set of scenarios with random failure following Binomial distribution.
    NumScenarios : Number of scenarios to be generated.
    Links: Graph edges (links)
    BackupLinks: Set of backup edges (links).
    CapPerBackupLink: Set of backup edge (link) capacity (weight)
    BackupRoutes: Set of backup edges (links).
    
    Returns
    -------
    P: Buffered failure probability.

    """
    P={}
    for i,j in BackupLinks:
        P[i,j] = 0
        for k in range(NumScenarios):
            Psd=0
            for s,d in Links:
                Psd=Psd+BackupRoutes[i,j,s,d]*Scenarios[k,s,d]
            if Psd > CapPerBackupLink[i,j]:
                P[i,j]=P[i,j]+1
        P[i,j]=1.0*P[i,j]
    return P

def GetRealFailureProbability(FailureProbability,BackupLinks,BackupRoutes, BackupCapacity,Links,NumLinks, CapPerLink):
    L=20
    Num_S=np.zeros(L+1)
    for n in xrange(L+1):
        Num_S[n]=math.factorial(L)/(math.factorial(n)*math.factorial(L-n))
        
    S0=[]
    S1=[]
    S2=[]
    S3=[]
    S4=[]
    S5=[]
    S6=[]
    S7=[]
    S8=[]
    S9=[]
    S10=[]
    S11=[]
    S12=[]
    S13=[]
    S14=[]
    S15=[]
    S16=[]
    S17=[]
    S18=[]
    S19=[]
    S20=[]
    
    for i in range(1<<n):
        s=bin(i)[2:]
        s='0'*(n-len(s))+s
        aux = map(int,list(s))
        aux_sum=np.sum(aux)
        
        if aux_sum == 0:
            S0.append(aux)
        elif aux_sum == 1:
            S1.append(aux)
        elif aux_sum == 2:
            S2.append(aux)
        elif aux_sum == 3:
            S3.append(aux)
        elif aux_sum == 4:
            S4.append(aux)
        elif aux_sum == 5:
            S5.append(aux)
        elif aux_sum == 6:
            S6.append(aux)
        elif aux_sum == 7:
            S7.append(aux)
        elif aux_sum == 8:
            S8.append(aux)
        elif aux_sum == 9:
            S9.append(aux)
        elif aux_sum == 10:
            S10.append(aux)
        elif aux_sum == 11:
            S11.append(aux)
        elif aux_sum == 12:
            S12.append(aux)
        elif aux_sum == 13:
            S13.append(aux)
        elif aux_sum == 14:
            S14.append(aux)
        elif aux_sum == 15:
            S15.append(aux)
        elif aux_sum == 16:
            S16.append(aux)
        elif aux_sum == 17:
            S17.append(aux)
        elif aux_sum == 18:
            S18.append(aux)
        elif aux_sum == 19:
            S19.append(aux)
        elif aux_sum == 20:
            S20.append(aux)
    
    Sum={}
    for i,j in BackupLinks:
        Sum[i,j]=0
    
    for k in xrange(L+1):
        if k == 0:
            Scenarios = S0
        elif k == 1:
            Scenarios =S1
        elif k == 2:
            Scenarios =S2
        elif k == 3:
            Scenarios =S3
        elif k == 4:
            Scenarios =S4
        elif k == 5:
            Scenarios =S5
        elif k == 6:
            Scenarios =S6
        elif k == 7:
            Scenarios =S7
        elif k == 8:
            Scenarios =S8
        elif k == 9:
            Scenarios =S9
        elif k == 10:
            Scenarios =S10
        elif k == 11:
            Scenarios =S11
        elif k == 12:
            Scenarios =S12
        elif k == 13:
            Scenarios =S13
        elif k == 14:
            Scenarios =S14
        elif k == 15:
            Scenarios =S15
        elif k == 16:
            Scenarios =S16
        elif k == 17:
            Scenarios =S17
        elif k == 18:
            Scenarios =S18
        elif k == 19:
            Scenarios =S19
        else:
            Scenarios =S20
        
        IS=(FailureProbability**k)*(1-FailureProbability)**(L-k)
        NewScenarios = GetScenarios(Scenarios, int(Num_S[k]), NumLinks, Links, CapPerLink)
        
        Indicator = GetIndicator(NewScenarios, int(Num_S[k]), Links, BackupLinks, BackupCapacity, BackupRoutes)
        for i,j in BackupLinks:
            Sum[i,j]=Sum[i,j]+Indicator[i,j]*IS
            
    return Sum
    
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
        OptBackupCapacity,BackupRoutes,BackupLinks = BackupNet.LoadBackupNetwork(file_name)
        
        ScenariosGen = ScenariosGenerator()
        print('Generating %s random scenarios for failure probability test...' %(num_scenarios))
        unif_scenarios = ScenariosGen.GetUniformRand(None,num_scenarios, num_links)
        print('Done!\n')
         
        print('Generating binomial random scenarios for p=%s...'%p)
        scenarios = ScenariosGen.GetBinomialFromUnif(unif_scenarios, p, num_scenarios, num_links, links, cap_per_link)
        print('Done!\n')
        
        SolutionQos = QoS()
        start = time.clock()
        BufferedP_Normal,Variance = SolutionQos.GetBufferedFailureProb(None, scenarios, num_scenarios, links, BackupLinks, OptBackupCapacity, BackupRoutes)
        stop = time.clock()        
        final_time_normal = (stop-start)
    
        start = time.clock()
        BufferedP_Parallel = SolutionQos.GetBufferedFailureProbPar(p, num_scenarios, links, cap_per_link, BackupLinks, OptBackupCapacity, BackupRoutes)
        stop = time.clock()        
        final_time_parallel = (stop-start)
        
        print('%g > %g'%(final_time_normal,final_time_parallel))
        self.assertGreater(final_time_normal,final_time_parallel)
        
        for link in BufferedP_Normal:
            self.assertAlmostEquals(BufferedP_Normal[link], BufferedP_Parallel[link],delta=0.01)

    def test_get_confidence_interval(self):
        print('\n######### Testing GetConfidenceInterval method #########\n')
        
        num_scenarios = 1000000
        p=0.025
        p2=5*p
        num_nodes = 5
        file_name = 'TestBackupNetDefault.dat'
                
        G,links,nodes,num_links=Tools.GetFullConnectedNetwork(num_nodes)
        #You must change here if there is a different capacity for each link 
        cap_per_link=[1 for i in range(num_links)]
        #Adding the respective capacity for each link in the graph
        for s,d in links:
            G.add_weighted_edges_from([(s,d,cap_per_link[links.index((s,d))])])
            
        
        BackupNet = BFPBackupNetwork()
        BackupCapacity,BackupRoutes,BackupLinks = BackupNet.LoadBackupNetwork(file_name)
        
        ScenariosGen = ScenariosGenerator()
        print('Generating %s random scenarios for failure probability test...' %(num_scenarios))
        unif_scenarios = ScenariosGen.GetUniformRand(None,num_scenarios, num_links)
        print('Done!\n')
         
        print('Generating binomial random scenarios for p=%s...'%p2)
        scenarios = ScenariosGen.GetBinomialFromUnif(unif_scenarios, p2, num_scenarios, num_links, links, cap_per_link)
        gamma = ScenariosGen.GetImportanceSamplingVector(links, scenarios, num_scenarios, p, p2)
        print('Done!\n')
        
        print('Getting estimated failure probability...')
        SolutionQos = QoS()
        BufferedP,Variance = SolutionQos.GetBufferedFailureProb(gamma, scenarios, num_scenarios, links, BackupLinks, BackupCapacity, BackupRoutes)
        print('Done!\n')
        
        print('\nExpected failure probability:')
        for i,j in BackupLinks:
            print('E[p(x)][%g,%g]=%g'%(i,j,BufferedP[i,j]))
        
        print('\nVariance:')
        for i,j in BackupLinks:
            print('Var[p(x)][%g,%g]=%g'%(i,j,Variance[i,j]))    
        
        print('\nConfidence interval')
        ConfidenceInterval=SolutionQos.GetConfidenceInterval(BackupLinks,Variance,num_scenarios,None)
        for i,j in BackupLinks:
            print('[%g,%g]=[%g,%g]'%(i,j,BufferedP[i,j]-ConfidenceInterval[i,j],BufferedP[i,j]+ConfidenceInterval[i,j]))
        
        print('\nGetting real failure probability...(you should take a coffee)')
        RealBufferedP = GetRealFailureProbability(p, BackupLinks, BackupRoutes, BackupCapacity, links, num_links, cap_per_link)
        print('Done!\n')
        for i,j in BackupLinks:
            print('p(x)[%g,%g]=%g'%(i,j,RealBufferedP[i,j]))
        
        for i,j in BackupLinks:
            self.assertGreaterEqual(RealBufferedP[i,j],BufferedP[i,j]-ConfidenceInterval[i,j])
            self.assertLessEqual(RealBufferedP[i,j],BufferedP[i,j]+ConfidenceInterval[i,j])
            

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()