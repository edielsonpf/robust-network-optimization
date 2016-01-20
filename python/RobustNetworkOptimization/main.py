__author__ = "Edielson"

from BackupTest import BackupPathModelTest, BackupModelTest
from MonteCarlo import MonteCarloTest

if __name__ == '__main__':
    pass

# Constant definition
NumNodes = 5
NumScenarios = 50
p = 0.025
#p=0.0005
#p=0.025
epsilon = 0.01
invstd = 2.326347874

MipGap = None
TimeLimit = None
Options = 0

#print('original backup model')  
#BackupModelTest(Options, NumNodes,p,invstd,MipGap,TimeLimit)


#CutoffList = [None, 2, 1]
# CutoffList = [None]
# 
# for index in range(len(CutoffList)):
#     cutoff = CutoffList[index]
#     BackupPathModelTest(Options,NumNodes,p,invstd,MipGap,TimeLimit,cutoff)

print('Buffer probability-based backup model')
MonteCarloTest(Options, NumNodes, NumScenarios, p, epsilon,MipGap,TimeLimit)
