__author__ = "Edielson"

from BackupTest import BackupPathModelTest, BackupModelTest

if __name__ == '__main__':
    pass

# Constant definition
NumNodes = 3
p = 0.025
invstd = 2.326347874

MipGap = None
TimeLimit = None
  
#BackupModelTest(NumNodes,p,invstd,MipGap,TimeLimit)
Options = 0
#CutoffList = [None, 3, 2, 1]
CutoffList = [None, 1]

for index in range(len(CutoffList)):
    cutoff = CutoffList[index]
    print(cutoff)
    BackupPathModelTest(Options,NumNodes,p,invstd,MipGap,TimeLimit,cutoff)
