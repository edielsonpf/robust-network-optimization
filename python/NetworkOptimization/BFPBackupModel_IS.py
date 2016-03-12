'''
Created on Nov 23, 2015
 
@author: Edielson P. Frigieri
'''
from gurobipy import Model, GRB, quicksum
 
class BFPBackupIS(object):
    """ Class object for buffered failure probability-based model.

    Parameters
    ----------
    ImpSamp: importance sampling vector
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
    __z = {}
         
    # Private model parameters
    __Links = []
    __Nodes = []
    __Capacity = []
    __Survivability = 1
    __impSample = {}
    __K = 1
        
    def __init__(self,ImpSamp,Nodes,Links,Capacity,Survivability,K):
        '''
        Constructor
        '''
        self.__Links = Links
        self.__Nodes = Nodes
        self.__Capacity = Capacity
        self.__Survivability = Survivability
        self.__K = K
        self.__loadModel(ImpSamp)
                         
    def __loadModel(self,ImpSamp):
        """ Load model.
    
        Parameters
        ----------
        ImpSamp : importance sampling vector
        
        """         
        
        # Create optimization model
        self.__model = Model('Backup')
     
        # Create variables
        for i,j in self.__Links:
            self.__BackupCapacity[i,j] = self.__model.addVar(vtype=GRB.INTEGER,lb=0, name='Backup_Capacity[%s,%s]' % (i, j))
            #self.__BackupCapacity[i,j] = self.__model.addVar(lb=0, name='Backup_Capacity[%s,%s]' % (i, j))
        self.__model.update()
          
        for i,j in self.__Links:
            for s,d in self.__Links:
                self.__bBackupLink[i,j,s,d] = self.__model.addVar(vtype=GRB.BINARY,name='Backup_Link[%s,%s,%s,%s]' % (i, j, s, d))
        self.__model.update()
         
        for i,j in self.__Links:
            for k in range(self.__K):
                self.__z[k,i,j] = self.__model.addVar(lb=0,name='z[%s][%s][%s]' % (k,i,j))
        self.__model.update()
        
        for i,j in self.__Links: 
            self.__z0[i,j] = self.__model.addVar(lb=-GRB.INFINITY,name='z0[%s][%s]' %(i,j))
        self.__model.update()
         
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
            self.__model.addConstr(self.__z0[i,j] + 1/(self.__K*self.__Survivability)*quicksum(self.__z[k,i,j] for (k) in range(self.__K)) <= 0,'[CONST]Buffer_Prob_I[%s][%s]'%(i,j))
        self.__model.update()
         
        # Link capacity constraints
        for i,j in self.__Links:
            for k in range(self.__K):
                self.__model.addConstr((quicksum(self.__bBackupLink[i,j,s,d]*self.__Capacity[k,s,d] for s,d in self.__Links) - self.__BackupCapacity[i,j] - self.__z0[i,j])*ImpSamp[k,i,j] <= self.__z[k,i,j],'[CONST]Buffer_Prob_II[%s][%s][%s]' % (k,i,j))
        self.__model.update()
        
        # Link capacity constraints
        for i,j in self.__Links:
            for k in range(self.__K):
                self.__model.addConstr(self.__z[k,i,j] >= 0,'[CONST]Buffer_Prob_III[%s][%s][%s]' % (k,i,j))
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
    
    def reset(self):
        '''
        Reset model solution.
        '''
        self.__model.reset()