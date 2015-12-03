'''
Created on Nov 23, 2015

@author: Edielson
'''
from gurobipy import *

class PathBackup(object):
    '''
    classdocs
    '''
    # Private model object
    __model = []
    
    # Private model variables
    __BackupCapacity = {}
    __bPath = {}
           
    # Private model parameters
    __links = []
    __paths = []
    __nodes = []
    __capacity = []
    __mean = []
    __std = []
    __Psd = []
    __Pij = []
    __invstd = 1
    
    
    def __init__(self,nodes,links,paths,Psd,Pij,capacity,mean,std,invstd):
        '''
        Constructor
        '''
        self.__links = links
        self.__nodes = nodes
        self.__paths = paths
        self.__capacity = capacity
        self.__mean = mean
        self.__std = std
        self.__invstd = invstd
        self.__Psd = Psd
        self.__Pij = Pij
        
        self.__loadModel()
                
    def __loadModel(self):
                
        # Create optimization model
        self.__model = Model('PathBackup')
    
        # Auxiliary variables for SOCP reformulation
        U = {}
        R = {}
      
        # Create variables
        for i,j in self.__links:
            self.__BackupCapacity[i,j] = self.__model.addVar(lb=0, obj=1, name='Backup_Capacity[%s,%s]' % (i, j))
        self.__model.update()
         
        for p in self.__paths:
            self.__bPath[self.__paths.index(p)] = self.__model.addVar(vtype=GRB.BINARY,obj=1,name='Backup_Path[%s]' % (self.__paths.index(p)))
        self.__model.update()
        
        for i,j in self.__links:
            U[i,j] = self.__model.addVar(obj=1,name='U[%s,%s]' % (i, j))
        self.__model.update()
        
        for i,j in self.__links:
            for p in self.__paths:
                R[i,j,self.__paths.index(p)] = self.__model.addVar(obj=1,name='R[%s,%s,%s]' % (i,j,self.__paths.index(p)))
        self.__model.update()
        
        self.__model.modelSense = GRB.MINIMIZE
        #m.setObjective(quicksum([fixedCosts[p]*open[p] for p in plants]))
        self.__model.setObjective(quicksum(self.__BackupCapacity[i,j] for i,j in self.__links))
        self.__model.update()
        
           
        #------------------------------------------------------------------------#
        #                    Constraints definition                              #
        #                                                                        #
        #                                                                        #
        #------------------------------------------------------------------------#
         
        # Link capacity constraints
        for i,j in self.__links:
            self.__model.addConstr(self.__BackupCapacity[i,j] >= quicksum(self.__mean[self.__paths.index(p)]*self.__bPath[self.__paths.index(p)] for p in self.__Pij[i,j]) + U[i,j]*self.__invstd,'[CONST]Link_Cap[%s][%s]' % (i, j))
        self.__model.update()
            
        # SCOP Reformulation Constraints
        for i,j in self.__links:
            self.__model.addConstr(quicksum(R[i,j,self.__paths.index(p)]*R[i,j,self.__paths.index(p)] for p in self.__Pij[i,j]) <= U[i,j]*U[i,j],'[CONST]SCOP1[%s][%s]' % (i, j))
        self.__model.update()
            
        # SCOP Reformulation Constraints    
        for i,j in self.__links:
            for p in self.__Pij[i,j]:
                self.__model.addConstr(self.__std[self.__paths.index(p)]*self.__bPath[self.__paths.index(p)] == R[i,j,self.__paths.index(p)],'[CONST]SCOP2[%s][%s][%s]' % (i,j,self.__paths.index(p)))
        self.__model.update()
        
        for s,d in self.__links:
            self.__model.addConstr(quicksum(self.__bPath[self.__paths.index(p)] for p in self.__Psd[s,d]) == 1,'UniquePath[%s,%s]' % (s, d))
        self.__model.update()
                
        
    def optimize(self):
        
        self.__model.write('pathbackup.lp')
 
        # Compute optimal solution
        self.__model.optimize()
        
        # Print solution
        if self.__model.status == GRB.Status.OPTIMAL:
            solution = self.__model.getAttr('x', self.__BackupCapacity)
            for i,j in self.__links:
                if solution[i,j] > 0:
                    print('%s -> %s: %g' % (i, j, solution[i,j]))
            
        else:
            print('Optimal value not found!\n')
            solution = []
            
        return solution;    