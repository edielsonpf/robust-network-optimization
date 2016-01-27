__author__ = "Edielson"

from BackupTest import BackupPathModelTest, BackupModelTest, BackupBFPModelTest

if __name__ == '__main__':
    pass

BACKUP_MODEL = 1
BACKUP_PATH_MODEL = 0
BACKUP_BFP_MODEL = 0

# Constant definition
NumNodes = 4
p=0.025
#constant for backup model and backup model with paths 
invstd = 2.326347874
#constant for buffered failure backup model only
epsilon = 0.01


#Optimization definitions
MipGap = None
#MipGap = 0.01
TimeLimit = None

#constant for choosing to plot (1) or not to plot (2) graphs
PlotOptions = 1

if BACKUP_MODEL == 1:
    print('Normal-based backup model')  
    BackupModelTest(PlotOptions, NumNodes,p,invstd,MipGap,TimeLimit)

if BACKUP_PATH_MODEL == 1:
    print('Path-based backup model')  
    #CutoffList = [None, 2, 1]
    CutoffList = [None]
 
    for index in range(len(CutoffList)):
        cutoff = CutoffList[index]
        BackupPathModelTest(PlotOptions,NumNodes,p,invstd,MipGap,TimeLimit,cutoff)

if BACKUP_BFP_MODEL == 1:
    NumScenarios = 50
    Scenario=1
    print('Buffer probability-based backup model')
    BackupBFPModelTest(PlotOptions, NumNodes, Scenario, NumScenarios, p, epsilon, MipGap, TimeLimit)