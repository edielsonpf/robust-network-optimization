'''
Created on Nov 23, 2015

@author: Edielson
'''
from gurobipy import Model, GRB, quicksum

class Backup(object):
    '''
    classdocs
    '''
    # Private model object
    __model = []
    
    # Private model variables
    __BackupCapacity = {}
    __bBackupLink = {}
    __ValidLink = {}
        
    # Private model parameters
    __links = []
    __nodes = []
    __capacity = []
    __mean = []
    __std = []
    __invstd = 1
    
    def __init__(self,nodes,links,capacity,mean,std,invstd):
        '''
        Constructor
        '''
        self.__links = links
        self.__nodes = nodes
        self.__capacity = capacity
        self.__mean = mean
        self.__std = std
        self.__invstd = invstd
        
        self.__loadModel()
                
    def __loadModel(self):
                
        # Create optimization model
        self.__model = Model('Backup')
    
        # Auxiliary variables for SOCP reformulation
        U = {}
        R = {}
      
        # Create variables
        for i,j in self.__links:
            self.__BackupCapacity[i,j] = self.__model.addVar(lb=0, obj=1, name='Backup_Capacity[%s,%s]' % (i, j))
        self.__model.update()
         
        for i,j in self.__links:
            for s,d in self.__links:
                self.__bBackupLink[i,j,s,d] = self.__model.addVar(vtype=GRB.BINARY,obj=1,name='Backup_Link[%s,%s,%s,%s]' % (i, j, s, d))
        self.__model.update()
        
        for i,j in self.__links:
            U[i,j] = self.__model.addVar(obj=1,name='U[%s,%s]' % (i, j))
        self.__model.update()
        
        for i,j in self.__links:
            for s,d in self.__links:
                R[i,j,s,d] = self.__model.addVar(obj=1,name='R[%s,%s,%s,%s]' % (i,j,s,d))
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
            self.__model.addConstr(self.__BackupCapacity[i,j] >= quicksum(self.__mean[s,d]*self.__bBackupLink[i,j,s,d] for (s,d) in self.__links) + U[i,j]*self.__invstd,'[CONST]Link_Cap_%s_%s' % (i, j))
        self.__model.update()
            
        # SCOP Reformulation Constraints
        for i,j in self.__links:
            self.__model.addConstr(quicksum(R[i,j,s,d]*R[i,j,s,d] for (s,d) in self.__links) <= U[i,j]*U[i,j],'[CONST]SCOP1[%s][%s]' % (i, j))
        self.__model.update()
            
        # SCOP Reformulation Constraints    
        for i,j in self.__links:
            for s,d in self.__links:
                self.__model.addConstr(self.__std[s,d]*self.__bBackupLink[i,j,s,d] == R[i,j,s,d],'[CONST]SCOP2[%s][%s][%s][%s]' % (i, j,s,d))
        self.__model.update()
        
        for i in self.__nodes:
            for s,d in self.__links:
                # Flow conservation constraints
                if i == s:
                    self.__model.addConstr(quicksum(self.__bBackupLink[i,j,s,d] for i,j in self.__links.select(i,'*')) - 
                                           quicksum(self.__bBackupLink[j,i,s,d] for j,i in self.__links.select('*',i)) == 1,'Flow1[%s,%s,%s,%s]' % (i,j,s, d))
                # Flow conservation constraints
                elif i == d:
                    self.__model.addConstr(quicksum(self.__bBackupLink[i,j,s,d] for i,j in self.__links.select(i,'*')) - 
                                           quicksum(self.__bBackupLink[j,i,s,d] for j,i in self.__links.select('*',i)) == -1,'Flow2[%s,%s,%s,%s]' % (i,j,s, d))
                # Flow conservation constraints
                else:    
                    self.__model.addConstr(quicksum(self.__bBackupLink[i,j,s,d] for i,j in self.__links.select(i,'*')) - 
                                           quicksum(self.__bBackupLink[j,i,s,d] for j,i in self.__links.select('*',i)) == 0,'Flow3[%s,%s,%s,%s]' % (i,j,s, d))
        self.__model.update()
                
        
    def optimize(self,MipGap, TimeLimit):
        
        self.__model.write('backup.lp')
        
        if MipGap != None:
            self.__model.params.timeLimit = TimeLimit
        if TimeLimit != None:
            self.__model.params.MIPGap = MipGap
         
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
    
    def reset(self):
        '''
        Reset model solution
        '''
        self.__model.reset()