__author__ = "Edielson"

from BackupTest import BackupPathModelTest, BackupModelTest
from MonteCarlo import MonteCarloTest
from NSFNET import NSFNET

if __name__ == '__main__':
    pass

# Constant definition
NumNodes = 5
NumScenarios =500
#p = 0.06
p=0.06
#NSFNET p=0.009 is equivalent to p=0.06
#epsilon = 0.05
epsilon = 0.05
#NSFNET e=0.09 is equivalent to e=0.05  
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
#NSFNET(Options,NumScenarios, p, epsilon,MipGap,TimeLimit)