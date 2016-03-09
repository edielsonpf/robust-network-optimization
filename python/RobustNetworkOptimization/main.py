__author__ = "edielsonpf"

from BFPBackupModelTest import BFPBackupModelTest
from PathBackupModelTest import PathBackupModelTest
from NormalBackupModelTest import NormalBackupModelTest
from ParallelTest import ParallelValidation
from SurvivabilityTest import SurvivabilityTest

if __name__ == '__main__':
   
    PARALLEL_TEST = 0
    SURVIVABILITY_TEST = 1
    
    
    NORMAL_BACKUP_MODEL = 0
    PATH_BACKUP_MODEL = 0
    BFP_BACKUP_MODEL = 0
    
    # Constant definition
    NumNodes = 5
    p=0.025
    
    #constant for buffered failure backup model only
    epsilon = 0.14
    
    #Optimization definitions
    MipGap = None
    #MipGap = 0.001
    TimeLimit = None
    
    #constant for choosing to plot (1) or not to plot (0) graphs
    PlotOptions = 0
    
    if NORMAL_BACKUP_MODEL == 1:
        
        #constant for backup model and backup model with paths 
        invstd = 2.326347874
    
        print('Normal-based backup model')  
        NormalBackupModelTest(PlotOptions, NumNodes,p,invstd,MipGap,TimeLimit)
    
    if PATH_BACKUP_MODEL == 1:
        
        #constant for backup model and backup model with paths 
        invstd = 2.326347874
    
        #CutoffList = [None, 2, 1]
        CutoffList = [None]
     
        for index in range(len(CutoffList)):
            cutoff = CutoffList[index]
            print('Normal-based backup model with paths: cutoff = %g' % cutoff[index])  
            PathBackupModelTest(PlotOptions,NumNodes,p,invstd,MipGap,TimeLimit,cutoff)
    
    if BFP_BACKUP_MODEL == 1:
        
        print('Buffered failure probability-based backup model')
        
        NumScenarios = [100,10000,10000,1010500]
        
        #Choose scenario 0 for a full directed graph with the number of nodes equal to the value of the variable NumNodes
        #or choose 1 to the NSFNET network with 14 nodes
        Scenario=0
        
        ImportanceSampling=1
        UseParallel = 1
        p2=5*p
        
        BFPBackupModelTest(UseParallel, ImportanceSampling,PlotOptions, NumNodes, Scenario, NumScenarios, p,p2, epsilon, MipGap, TimeLimit)
        
    if PARALLEL_TEST:
        
        NumScenarios = 50
        NumScenariosValid = 500000
        p2=2*p
        
        ParallelValidation(NumNodes, NumScenarios, NumScenariosValid, p, p2, epsilon, MipGap, TimeLimit)
        
    if SURVIVABILITY_TEST:
        
        # Constant definition
        p2=5*p
        
        NumScenarios = [100,10000,10000,501050]
        
        EpsilonList = [0.5, 0.1, 0.01]
        
        #Choose scenario 0 for a full directed graph with the number of nodes equal to the value of the variable NumNodes
        #or choose 1 to the NSFNET network with 14 nodes
        Scenario=0
        
        ImportanceSampling=1
        
        UseParallel = 1
        
        print('Buffered failure probability-based backup model: survivability test')
        SurvivabilityTest(UseParallel, ImportanceSampling,PlotOptions,NumNodes,Scenario,NumScenarios,p,p2,EpsilonList,MipGap,TimeLimit)    