__author__ = "Edielson"

from BackupTest import BackupPathModelTest, BackupModelTest, BackupBFPModelTest

if __name__ == '__main__':
    pass

BACKUP_MODEL = 0
BACKUP_PATH_MODEL = 0
BACKUP_BFP_MODEL = 1

# Constant definition
NumNodes = 5
p=0.075
#constant for backup model and backup model with paths 
invstd = 2.326347874
#constant for buffered failure backup model only
#0.045 to 0.05 blow up model with 3 nodes
epsilon = 0.05


#Optimization definitions
#MipGap = None
MipGap = 0.001
TimeLimit = None

#constant for choosing to plot (1) or not to plot (0) graphs
PlotOptions = 0

if BACKUP_MODEL == 1:
    print('Normal-based backup model')  
    BackupModelTest(PlotOptions, NumNodes,p,invstd,MipGap,TimeLimit)

if BACKUP_PATH_MODEL == 1:
    print('Normal-based backup model with paths')  
    #CutoffList = [None, 2, 1]
    CutoffList = [None]
 
    for index in range(len(CutoffList)):
        cutoff = CutoffList[index]
        BackupPathModelTest(PlotOptions,NumNodes,p,invstd,MipGap,TimeLimit,cutoff)

if BACKUP_BFP_MODEL == 1:
    NumScenarios = 200
    #Choose scenario 0 for a full directed graph with the number of nodes equal to the value of the variable NumNodes
    #or choose 1 to the NSFNET network with 14 nodes
    Scenario=1
    print('Buffered failure probability-based backup model')
    BackupBFPModelTest(PlotOptions, NumNodes, Scenario, NumScenarios, p, epsilon, MipGap, TimeLimit)