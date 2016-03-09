__author__ = "edielsonpf"

from BackupTest import EpsilonBFPModelTest

if __name__ == '__main__':
    pass

# Constant definition
NumNodes = 14
p=0.06
p2=1.2*p

NumScenarios = [20,10000,10000,101050]

#Choose scenario 0 for a full directed graph with the number of nodes equal to the value of the variable NumNodes
#or choose 1 to the NSFNET network with 14 nodes
Scenario=1
ImportanceSampling=1

EpsilonList = [0.2, 0.15]

MipGap = None
TimeLimit = None

#constant for choosing to plot (1) or not to plot (0) graphs
PlotOptions = 0

print('Buffered failure probability-based backup model')
EpsilonBFPModelTest(ImportanceSampling,PlotOptions,NumNodes,Scenario,NumScenarios,p,p2,EpsilonList,MipGap,TimeLimit)