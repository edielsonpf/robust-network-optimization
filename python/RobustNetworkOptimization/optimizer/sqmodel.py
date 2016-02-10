'''
Created on Fev 05, 2016
 
@author: Edielson P. Frigieri
'''
from gurobipy import *
 
class SQModel(object):
    '''
    classdocs
    '''
    # Private model object
    __model = []
         
    # Private model variables
    __z0 = {}
    __z = {}
         
    # Private model parameters
    __BackupCapacity = {}
    __bBackupLink = {}
    __links = []
    __nodes = []
    __capacity = []
    __epsilon = 1
    __impSample = {}
    __N = 1
        
    def __init__(self,imp_samp,nodes,links,capacity,epsilon,N,backup_link,link_capacity):
        '''
        Constructor
        '''
        self.__links = links
        self.__nodes = nodes
        self.__capacity = capacity
        self.__epsilon = epsilon
        self.__N = N
        self.__loadModel(imp_samp,backup_link,link_capacity)
                                 
    def __loadModel(self,imp_samp, backup_link,link_capacity):
                 
        # Create optimization model
        self.__model = Model('Backup')
     
        for i,j in self.__links:
            for k in range(self.__N):
                self.__z[k,i,j] = self.__model.addVar(lb=0,name='z[%s][%s][%s]' % (k,i,j))
        self.__model.update()
        
        for i,j in self.__links: 
            self.__z0[i,j] = self.__model.addVar(lb=-GRB.INFINITY,name='z0[%s][%s]' %(i,j))
        self.__model.update()
         
        self.__model.modelSense = GRB.MINIMIZE
        
        #self.__model.setObjective(quicksum(self.__z0[i,j] for i,j in self.__links))
        self.__model.setObjective(quicksum((self.__z0[i,j] + 1/(self.__N*self.__epsilon)*quicksum(self.__z[k,i,j]*imp_samp[k,i,j] for (k) in range(self.__N))) for i,j in self.__links))
        self.__model.update()
         
            
        #------------------------------------------------------------------------#
        #                    Constraints definition                              #
        #                                                                        #
        #                                                                        #
        #------------------------------------------------------------------------#
          
        # Buffer probability I
#         for i,j in self.__links:
#             self.__model.addConstr(self.__z0[i,j] + 1/(self.__N*self.__epsilon)*quicksum(self.__z[k,i,j] for (k) in range(self.__N)) <= 0,'[CONST]Buffer_Prob_I[%s][%s]'%(i,j))
#         self.__model.update()
         
        # Link capacity constraints
        for i,j in self.__links:
            for k in range(self.__N):
                self.__model.addConstr((quicksum(backup_link[i,j,s,d]*self.__capacity[k,s,d] for s,d in self.__links) - link_capacity[i,j] - self.__z0[i,j]) <= self.__z[k,i,j],'[CONST]Buffer_Prob_II[%s][%s][%s]' % (k,i,j))
        self.__model.update()
        
        # Link capacity constraints
        for i,j in self.__links:
            for k in range(self.__N):
                self.__model.addConstr(self.__z[k,i,j] >= 0,'[CONST]Buffer_Prob_III[%s][%s][%s]' % (k,i,j))
        self.__model.update()
         
    def optimize(self,MipGap, TimeLimit, LogLevel = None):
         
        self.__model.write('quantile.lp')
         
        if MipGap != None:
            self.__model.params.MIPGap = MipGap
        if TimeLimit != None:
            self.__model.params.timeLimit = TimeLimit
        # Compute optimal solution
        self.__model.optimize()
         
        # Print solution
        if self.__model.status == GRB.Status.OPTIMAL:
            SuperQuantileSolution = self.__model.getAttr('x', self.__z0)
            
            if LogLevel == 1:
                for v in self.__model.getVars():
                    print('%s %g' % (v.varName, v.x))
                                                
        else:
            print('Optimal value not found!\n')
            SuperQuantileSolution = []
                         
        return SuperQuantileSolution    