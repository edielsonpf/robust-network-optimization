__author__ = "Edielson"

from BackupTest import BackupPathModelTest, BackupModelTest

if __name__ == '__main__':
    pass

# Constant definition
NumNodes = 5
p = 0.025
invstd = 2.326347874

MipGap = 0.2
TimeLimit = 500
  
BackupModelTest(NumNodes,p,invstd,MipGap,TimeLimit)
BackupPathModelTest(NumNodes,p,invstd,MipGap,TimeLimit)
