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
Options = 0
  
#BackupModelTest(Options, NumNodes,p,invstd,MipGap,TimeLimit)


#CutoffList = [None, 2, 1]
CutoffList = [None]

for index in range(len(CutoffList)):
    cutoff = CutoffList[index]
    BackupPathModelTest(Options,NumNodes,p,invstd,MipGap,TimeLimit,cutoff)
