'''
Created on Nov 23, 2015
 
@author: Edielson
'''
from gurobipy import *
 
class BFPBackup(object):
    '''
    classdocs
    '''
    # Private model object
    __model = []
         
    # Private model variables
    __BackupCapacity = {}
    __bBackupLink = {}
    __z0 = {}
    __z = {}
         
    # Private model parameters
    __links = []
    __nodes = []
    __capacity = []
    __epsilon = 1
    __impSample = {}
    __N = 1
        
    def __init__(self,imp_samp,nodes,links,capacity,epsilon,N):
        '''
        Constructor
        '''
        self.__links = links
        self.__nodes = nodes
        self.__capacity = capacity
        self.__epsilon = epsilon
        self.__N = N
        self.__loadModel(imp_samp)
                         
    def __loadModel(self,imp_samp):
                 
        # Create optimization model
        self.__model = Model('Backup')
     
        # Create variables
        for i,j in self.__links:
            self.__BackupCapacity[i,j] = self.__model.addVar(lb=0, name='Backup_Capacity[%s,%s]' % (i, j))
        self.__model.update()
          
        for i,j in self.__links:
            for s,d in self.__links:
                self.__bBackupLink[i,j,s,d] = self.__model.addVar(vtype=GRB.BINARY,name='Backup_Link[%s,%s,%s,%s]' % (i, j, s, d))
        self.__model.update()
         
        for i,j in self.__links:
            for k in range(self.__N):
                self.__z[k,i,j] = self.__model.addVar(lb=0,name='z[%s][%s][%s]' % (k,i,j))
        self.__model.update()
        
        for i,j in self.__links: 
            self.__z0[i,j] = self.__model.addVar(lb=-GRB.INFINITY,name='z0[%s][%s]' %(i,j))
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
          
        # Buffer probability I
        for i,j in self.__links:
            self.__model.addConstr(self.__z0[i,j] + 1/(self.__N*self.__epsilon)*quicksum(self.__z[k,i,j] for (k) in range(self.__N)) <= 0,'[CONST]Buffer_Prob_I[%s][%s]'%(i,j))
        self.__model.update()
         
        # Link capacity constraints
        for i,j in self.__links:
            for k in range(self.__N):
                self.__model.addConstr((quicksum(self.__bBackupLink[i,j,s,d]*self.__capacity[k,s,d] for s,d in self.__links) - self.__BackupCapacity[i,j] - self.__z0[i,j])*imp_samp[k,i,j] <= self.__z[k,i,j],'[CONST]Buffer_Prob_II[%s][%s][%s]' % (k,i,j))
        self.__model.update()
        
        # Link capacity constraints
        for i,j in self.__links:
            for k in range(self.__N):
                self.__model.addConstr(self.__z[k,i,j] >= 0,'[CONST]Buffer_Prob_III[%s][%s][%s]' % (k,i,j))
        self.__model.update()
         
        for i in self.__nodes:
            for s,d in self.__links:
                # Flow conservation constraints
                if i == s:
                    self.__model.addConstr(quicksum(self.__bBackupLink[i,j,s,d] for i,j in self.__links.select(i,'*')) - 
                                           quicksum(self.__bBackupLink[j,i,s,d] for j,i in self.__links.select('*',i)) == 1,'Flow1[%s,%s,%s]' % (i,s,d))
                # Flow conservation constraints
                elif i == d:
                    self.__model.addConstr(quicksum(self.__bBackupLink[i,j,s,d] for i,j in self.__links.select(i,'*')) - 
                                           quicksum(self.__bBackupLink[j,i,s,d] for j,i in self.__links.select('*',i)) == -1,'Flow2[%s,%s,%s]' % (i,s,d))
                # Flow conservation constraints
                else:    
                    self.__model.addConstr(quicksum(self.__bBackupLink[i,j,s,d] for i,j in self.__links.select(i,'*')) - 
                                           quicksum(self.__bBackupLink[j,i,s,d] for j,i in self.__links.select('*',i)) == 0,'Flow3[%s,%s,%s]' % (i,s,d))
        self.__model.update()
                 
         
    def optimize(self,MipGap, TimeLimit, LogLevel = None):
         
        self.__model.write('bpbackup.lp')
         
        if MipGap != None:
            self.__model.params.MIPGap = MipGap
        if TimeLimit != None:
            self.__model.params.timeLimit = TimeLimit
        # Compute optimal solution
        self.__model.optimize()
         
        # Print solution
        if self.__model.status == GRB.Status.OPTIMAL:
            BackupCapacitySolution = self.__model.getAttr('x', self.__BackupCapacity)
            BackupLinkSolution = self.__model.getAttr('x', self.__bBackupLink)

            if LogLevel == 1:
                for v in self.__model.getVars():
                    print('%s %g' % (v.varName, v.x))
                                                
        else:
            print('Optimal value not found!\n')
            BackupCapacitySolution = []
            BackupLinkSolution = {}
             
        return BackupCapacitySolution,BackupLinkSolution    