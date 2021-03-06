'''
Created on Nov 23, 2015

@author: Edielson
'''
from gurobipy import Model, GRB, quicksum

class PathBackup(object):
    """ Class object for normal-based backup network model.

    Parameters
    ----------
    nodes: set of nodes
    links: set of links
    paths: set of paths in the graph
    Psd: set of backup paths for link (s,d). 
    Pij: set of (s,d) paths that use link (i,j).
    capacity: capacities per link based based on random failures 
    mean: mean for failure random variable
    std: standard deviation for failure random variable
    invstd: inverse of Phi-normal distribution for (1-epsilon)

    Returns
    -------
    solution: set of capacity assigned per backup link. 
    
    """
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
            #LP Relaxation
            #self.__bPath[self.__paths.index(p)] = self.__model.addVar(lb=0,obj=1,name='Backup_Path[%s]' % (self.__paths.index(p)))
            self.__bPath[self.__paths.index(p)] = self.__model.addVar(vtype=GRB.BINARY,obj=1,name='Backup_Path[%s]' % (self.__paths.index(p)))
        self.__model.update()
        
        for i,j in self.__links:
            U[i,j] = self.__model.addVar(obj=1,name='U[%s,%s]' % (i, j))
        self.__model.update()
        
        for i,j in self.__links:
            for s,d in self.__links:
                R[i,j,s,d] = self.__model.addVar(obj=1,name='R[%s,%s,%s,%s]' % (i,j,s,d))
        self.__model.update()
        
        self.__model.modelSense = GRB.MINIMIZE
        self.__model.setObjective(quicksum(self.__BackupCapacity[i,j] for i,j in self.__links))
        self.__model.update()
        
           
        #------------------------------------------------------------------------#
        #                    Constraints definition                              #
        #                                                                        #
        #                                                                        #
        #------------------------------------------------------------------------#
         
        # Link capacity constraints
        for i,j in self.__links:
            self.__model.addConstr(self.__BackupCapacity[i,j] >= quicksum(self.__mean[s,d]*quicksum(self.__bPath[self.__paths.index(p)] for p in self.__Pij[i,j,s,d]) for s,d in self.__links) + U[i,j]*self.__invstd,'[CONST]Link_Cap[%s][%s]' % (i, j))
        self.__model.update()
            
        # SCOP Reformulation Constraints
        for i,j in self.__links:
            self.__model.addConstr(quicksum(R[i,j,s,d]*R[i,j,s,d] for s,d in self.__links) <= U[i,j]*U[i,j],'[CONST]SCOP1[%s][%s]' % (i, j))
        self.__model.update()
            
        # SCOP Reformulation Constraints    
        for i,j in self.__links:
            for s,d in self.__links:
                self.__model.addConstr(self.__std[s,d]*quicksum(self.__bPath[self.__paths.index(p)] for p in self.__Pij[i,j,s,d]) == R[i,j,s,d],'[CONST]SCOP2[%s][%s][%s][%s]' % (i,j,s,d))
        self.__model.update()
        
        # Unique path 
        for s,d in self.__links:
            self.__model.addConstr(quicksum(self.__bPath[self.__paths.index(p)] for p in self.__Psd[s,d]) == 1,'UniquePath[%s,%s]' % (s, d))
        self.__model.update()
        
    def optimize(self,MipGap,TimeLimit):
        
        self.__model.write('pathbackup.lp')
 
        if TimeLimit != None:
            self.__model.params.timeLimit = TimeLimit
        
        if MipGap != None:
            self.__model.params.MIPGap=MipGap
         
        # Compute optimal solution
        self.__model.optimize()
        
        # Print solution
        if self.__model.status == GRB.Status.OPTIMAL:
            solution = self.__model.getAttr('x', self.__bPath)
            for p in self.__paths:
                if solution[self.__paths.index(p)] > 0.001:
                    print('Path[%s] = %s = %s' % (self.__paths.index(p),p,solution[self.__paths.index(p)]))
            solution = self.__model.getAttr('x', self.__BackupCapacity)
            for i,j in self.__links:
                if solution[i,j] > 0:
                    print('%s -> %s: %g' % (i, j, solution[i,j]))
            
        else:
            print('Optimal value not found!\n')
            solution = self.__model.getAttr('x', self.__BackupCapacity)
            for i,j in self.__links:
                if solution[i,j] > 0:
                    print('%s -> %s: %g' % (i, j, solution[i,j]))
            #solution = []
            
        return solution;    
    
    def reset(self):
        '''
        Reset model solution
        '''
        self.__model.reset()