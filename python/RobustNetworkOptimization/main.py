__author__ = "Edielson"

from BackupTest import BackupModelTest, BackupPathModelTest

if __name__ == '__main__':
    pass

# Constant definition
NumNodes = 5
p = 0.025
invstd = 2.326347874
  
#BackupModelTest()
BackupPathModelTest(NumNodes,p,invstd)
