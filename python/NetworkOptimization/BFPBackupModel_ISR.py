'''
Created on Nov 23, 2015
 
@author: Edielson P. Frigieri
'''
from gurobipy import Model, GRB, quicksum
 
class BFPBackupISR(object):
    """ Class object for buffered failure probability-based model.

    Parameters
    ----------
    Gamma: importance sampling vector
    Nodes: set of nodes
    Links: set of links
    Capacity: capacities per link based based on random failures 
    Survivability: desired survivabiliy factor (epsilon)
    K: number of random scenarios
    
    Returns
    -------
    BackupCapacitySolution: set of capacity per backup link. 
    BackupLinkSolution: set of backup links
    
    """         
    
    # Private model object
    __model = []
         
    # Private model variables
    __BackupCapacity = {}
    __bBackupLink = {}
    __z0 = {}
#     __z0Bar = {}
#     __z = {}
    __zBar = {}
         
    # Private model parameters
    __Links = []
    __Nodes = []
    __Capacity = []
    __Survivability = 1
    __n = 1
        
    def __init__(self):
        '''
        Constructor
        '''
        
                         
    def loadModel(self,Gamma,Nodes,Links,Capacity,Survivability,NumSamples):
        """ Load model.
    
        Parameters
        ----------
        Gamma : importance sampling vector
        
        """         
        self.__Links = Links
        self.__Nodes = Nodes
        self.__Capacity = Capacity
        self.__Survivability = Survivability
        self.__n = NumSamples
        
        
        # Create optimization model
        self.__model = Model('Rescaled Backup Model')
     
        # Create variables
        for i,j in self.__Links:
            self.__BackupCapacity[i,j] = self.__model.addVar(vtype=GRB.INTEGER,lb=0, name='Backup_Capacity[%s,%s]' % (i, j))
        self.__model.update()
          
        for i,j in self.__Links:
            for s,d in self.__Links:
                self.__bBackupLink[i,j,s,d] = self.__model.addVar(vtype=GRB.BINARY,name='Backup_Link[%s,%s,%s,%s]' % (i, j, s, d))
        self.__model.update()
         
#         for i,j in self.__Links:
#             for k in range(self.__n):
#                 self.__z[k,i,j] = self.__model.addVar(lb=0,name='z[%s][%s][%s]' % (k,i,j))
#         self.__model.update()
         
        for i,j in self.__Links: 
            self.__z0[i,j] = self.__model.addVar(lb=-GRB.INFINITY,name='z0[%s][%s]' %(i,j))
        self.__model.update()
        
#         for i,j in self.__Links: 
#             self.__z0Bar[i,j] = self.__model.addVar(lb=-GRB.INFINITY,name='z0[%s][%s]' %(i,j))
#         self.__model.update()
         
        for i,j in self.__Links:
            for k in range(self.__n):
                self.__zBar[k,i,j] = self.__model.addVar(lb=0,name='zbar[%s][%s][%s]' % (k,i,j))
        self.__model.update()
         
#         for i,j in self.__Links: 
#             self.__zBar0[i,j] = self.__model.addVar(lb=-GRB.INFINITY,name='zbar0[%s][%s]' %(i,j))
#         self.__model.update() 
         
        self.__model.modelSense = GRB.MINIMIZE
        
        self.__model.setObjective(quicksum(self.__BackupCapacity[i,j] for i,j in self.__Links))
        self.__model.update()
         
            
        #------------------------------------------------------------------------#
        #                    Constraints definition                              #
        #                                                                        #
        #                                                                        #
        #------------------------------------------------------------------------#
          
        # Buffer probability I
        for i,j in self.__Links:
#             self.__model.addConstr(self.__z0[i,j] + 1/(self.__n*self.__Survivability)*quicksum(self.__zBar[k,i,j]*Gamma[k] for (k) in range(self.__n)) <= 0,'[CONST]Buffer_Prob_I[%s][%s]'%(i,j))
            self.__model.addConstr(self.__z0[i,j] + quicksum(self.__zBar[k,i,j]*Gamma[k] for (k) in range(self.__n)) <= 0,'[CONST]Buffer_Prob_I[%s][%s]'%(i,j))
        self.__model.update()
         
        # Link capacity constraints
        for i,j in self.__Links:
            for k in range(self.__n):
                self.__model.addConstr(quicksum(self.__bBackupLink[i,j,s,d]*self.__Capacity[k,s,d] for s,d in self.__Links) - self.__BackupCapacity[i,j] - self.__z0[i,j] <= self.__zBar[k,i,j],'[CONST]Buffer_Prob_II[%s][%s][%s]' % (k,i,j))
#                 self.__model.addConstr((quicksum(self.__bBackupLink[i,j,s,d]*self.__Capacity[k,s,d] for s,d in self.__Links) - self.__BackupCapacity[i,j] - self.__z0Bar[i,j]) <= self.__zBar[k,i,j]*(2*LHS[k,i,j]),'[CONST]Buffer_Prob_II[%s][%s][%s]' % (k,i,j))
        self.__model.update()
        
        for i in self.__Nodes:
            for s,d in self.__Links:
                # Flow conservation constraints
                if i == s:
                    self.__model.addConstr(quicksum(self.__bBackupLink[i,j,s,d] for i,j in self.__Links.select(i,'*')) - 
                                           quicksum(self.__bBackupLink[j,i,s,d] for j,i in self.__Links.select('*',i)) == 1,'Flow1[%s,%s,%s]' % (i,s,d))
                # Flow conservation constraints
                elif i == d:
                    self.__model.addConstr(quicksum(self.__bBackupLink[i,j,s,d] for i,j in self.__Links.select(i,'*')) - 
                                           quicksum(self.__bBackupLink[j,i,s,d] for j,i in self.__Links.select('*',i)) == -1,'Flow2[%s,%s,%s]' % (i,s,d))
                # Flow conservation constraints
                else:    
                    self.__model.addConstr(quicksum(self.__bBackupLink[i,j,s,d] for i,j in self.__Links.select(i,'*')) - 
                                           quicksum(self.__bBackupLink[j,i,s,d] for j,i in self.__Links.select('*',i)) == 0,'Flow3[%s,%s,%s]' % (i,s,d))
        self.__model.update()
                 
         
    def optimize(self, MipGap=None, TimeLimit = None, LogLevel = None):
        """ Optimize the defined  model.
    
        Parameters
        ----------
        MipGap : desired gap
        TimeLimit : time limit
        LogLevel: log level 1 for printing all optimal variables and None otherwise
        
        Returns
        -------
        path_generator: Paths
           A tuple list with all paths for edge (s,d) that uses (i,j).
    
        """ 
        self.__model.write('rbpbackup.lp')
         
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
            
            OptimalBkpLinks={}
            for i,j in self.__Links:
                if BackupCapacitySolution[i,j] > 0.0001:
                    if (len(OptimalBkpLinks) == 0):
                        OptimalBkpLinks=[(i,j)]
                    else:
                        OptimalBkpLinks=OptimalBkpLinks+[(i,j)]
                        
            if LogLevel == 1:
                for v in self.__model.getVars():
                    print('%s %g' % (v.varName, v.x))
                                                
        else:
            print('Optimal value not found!\n')
            BackupCapacitySolution = []
            BackupLinkSolution = {}
            OptimalBkpLinks={}
             
        return BackupCapacitySolution,BackupLinkSolution,OptimalBkpLinks    
    
    def reset(self):
        '''
        Reset model solution.
        '''
        self.__model.reset()