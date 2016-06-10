'''
Created on Jun 9, 2016

@author: Edielson
'''
import numpy as np
import time
import multiprocessing
from multiprocessing import Pool

def ThreadGetBufferedFailureProb(RandSeed, FailureProb, NumScenarios, Links, CapPerLink, BackupLinks, CapPerBackupLink, OptBackupLinks):    
    """Thread to calculate the buffered failure probability.

    Parameters
    ----------
    RandSeed : Random seed (necessary for multiprocessing calls).
    FailureProb: Failure probability for each edge (link) in the graph.
    NumScenarios : Number of scenarios to be generated.
    Links: Graph edges (links)
    CapPerLink: Set of edge (link) capacity (weight).
    BackupLinks: Set of backup edges (links).
    CapPerBackupLink: Set of backup edge (link) capacity (weight)
    OptBackupLinks: Set of backup edges (links).
    
    Returns
    -------
    P: Buffered failure probability.

    """
    
#         Scenarios = self.GetRandScenarios(RandSeed, FailureProb, NumScenarios, len(Links), Links, CapPerLink)
    if RandSeed != None:
        np.random.seed(RandSeed)
    
    Y = np.random.binomial(1, FailureProb, (NumScenarios,len(Links)))
     
    Scenarios={}
    for k in range(NumScenarios):
        Index=0
        for s,d in Links:
            Scenarios[k,s,d]=CapPerLink[Index]*Y[k,Index]
            Index=Index+1
        
    P={}
    for i,j in BackupLinks:
        P[i,j] = 0
        for k in range(NumScenarios):
            Psd=0
            for s,d in Links:
                Psd=Psd+OptBackupLinks[i,j,s,d]*Scenarios[k,s,d]
            if Psd > CapPerBackupLink[i,j]:
                P[i,j]=P[i,j]+1
        P[i,j]=1.0*P[i,j]/NumScenarios
    return P

class QoS(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
    
    def GetAvgLinksPerBackupLink(self,BkpLinks,BkpRoutes,Links):
        '''
        Constructor
        '''
        
        n={}
        aux=0
        cont=0
        for i,j in BkpLinks:
            n[i,j]=0
            for s,d in Links:
                n[i,j] =(n[i,j]+BkpRoutes[i,j,s,d])
            if(n[i,j] > 0):
                aux=aux+n[i,j]
                cont=cont+1
        return 1.0*(aux/cont)    
    
    def GetConfidenceInterval(self,Links,Variance,NumSamples,Interval):
        '''
        Constructor
        '''
        
        if Interval == None:
            Interval=1.96 #95%
            
        ConfidenceInterval={}
        for i,j in Links:
            ConfidenceInterval[i,j]=1.96*np.sqrt(Variance[i,j])/(np.sqrt(NumSamples))
        
        return ConfidenceInterval
    
    def GetBinomialConfidenceInterval(self,Links,FailureProb,Interval,NumSamples):
    
        if Interval == None:
            Interval=1.96 #95%
            
        ConfidenceInterval={}
        for i,j in Links:
            ConfidenceInterval[i,j]=1.96*np.sqrt((FailureProb[i,j])*(1-FailureProb[i,j]))/(np.sqrt(NumSamples))
        
        return ConfidenceInterval

    def GetBufferedFailureProb(self,ImportanceSampling, Scenarios, NumScenarios, Links, BackupLinks, CapPerBackupLink, OptBackupLinks):    
        """Calculate the buffered failure probability.
    
        Parameters
        ----------
        ImportanceSampling: Importance sampling vector (obtained by GetImportanceSamplingVector method). None if scenarios were not generated using importance sampling.
        Scenarios: Set of scenarios with random failure following Binomial distribution.
        NumScenarios : Number of scenarios to be generated.
        Links: Graph edges (links)
        NumLinks: Number of edges (links) on each scenario.
        CapPerLink: Set of edge (link) capacity (weight).
        BackupLinks: Set of backup edges (links).
        CapPerBackupLink: Set of backup edge (link) capacity (weight)
        OptBackupLinks: Set of backup edges (links).
        
        Returns
        -------
        P: Buffered failure probability.
    
        """
        P={}
        I={}
        for i,j in BackupLinks:
            P[i,j] = 0
            for k in range(NumScenarios):
                Psd=0
                for s,d in Links:
                    Psd=Psd+OptBackupLinks[i,j,s,d]*Scenarios[k,s,d]
                I[k,i,j]=0
                if Psd > CapPerBackupLink[i,j]:
                    if ImportanceSampling == None:
                        I[k,i,j]=1
                        P[i,j]=P[i,j]+1
                    else:
                        I[k,i,j]=ImportanceSampling[k]
                        P[i,j]=P[i,j]+1*ImportanceSampling[k]
            P[i,j]=1.0*P[i,j]/NumScenarios
        return P,I

    def GetVariance(self,NumScenarios, BkpLinks,Mean,Indicator):    
        """Calculate the buffered failure probability.
    
        Parameters
        ----------
        NumScenarios : Number of scenarios used in the mean estimation.
        BackupLinks: Set of backup edges (links).
        CapPerBackupLink: Set of backup edge (link) capacity (weight)
        OptBackupLinks: Set of backup edges (links).
        
        Returns
        -------
        P: Buffered failure probability.
    
        """
        Var={}
        for i,j in BkpLinks:
            Var[i,j] = 0
            for k in range(NumScenarios):
                Var[i,j]=Var[i,j]+(Indicator[k,i,j]-Mean[i,j])**2
            Var[i,j]=1.0*Var[i,j]/(NumScenarios-1)
        return Var



    def GetBufferedFailureProbPar(self,FailureProb, NumScenarios, Links, CapPerLink, BackupLinks, CapPerBackupLink, OptBackupLinks):    
        """Calculate the buffered failure probability using multiprocessing.
    
        Parameters
        ----------
        FailureProb: Failure probability for each edge (link) in the graph.
        Scenarios: Group of scenarios with random failure following Binomial distribution.
        NumScenarios : Number of scenarios to be generated.
        Links: Graph edges (links)
        NumLinks: Number of edges (links) on each scenario.
        CapPerLink: Set of edge (link) capacity (weight).
        BackupLinks: Set of backup edges (links).
        CapPerBackupLink: Set of backup edge (link) capacity (weight)
        OptBackupLinks: Set of backup edges (links).
        
        Returns
        -------
        P: Buffered failure probability.
    
        """
        #check the number of available processors 
        nb_processes = multiprocessing.cpu_count ()
        print('Using %g available processors' %nb_processes)
        
        p = Pool(nb_processes)
        
        #divide the total number of scenarios to be generated among the available processes 
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
            
            RandSeed = int(np.random.exponential(time.clock()))
            args[k]=(RandSeed, FailureProb, NewDivision[k], Links, CapPerLink, BackupLinks, CapPerBackupLink, OptBackupLinks) 
                        
        # launching multiple evaluations asynchronously *may* use more processes
        multiple_results = [p.apply_async(ThreadGetBufferedFailureProb, (args[k])) for k in range(nb_processes)]
        
        P={}
        for i,j in BackupLinks:
            P[i,j]=0
        Counter=0
        for res in multiple_results:
            AvgP = res.get(timeout=1000)
            for i,j in BackupLinks:
                P[i,j]=P[i,j] + 1.0*AvgP[i,j]
            Counter=Counter+1
        
        for i,j in BackupLinks:
            P[i,j]=1.0*P[i,j]/Counter
            
        p.close()
        p.join()
        
        return P
    