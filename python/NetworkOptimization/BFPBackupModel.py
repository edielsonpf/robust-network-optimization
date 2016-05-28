'''
Created on Nov 23, 2015
 
@author: Edielson P. Frigieri
'''
from gurobipy import Model, GRB, quicksum, tuplelist
import json
 
class BFPBackup(object):
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
    BackupCapacity: set of capacity per backup link. 
    BackupRoutes: set of backup links
    
    """         
    
    # Private model object
    model = []
         
    # Private model variables
    BackupCapacity = {}
    bBackupLink = {}
    z0 = {}
    z = {}
         
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
        self.Links = tuplelist(Links)
        self.Capacity = Capacity
               
        # Create optimization model
        self.model = Model('Backup')
     
        # Create variables
        for i,j in self.Links:
            self.BackupCapacity[i,j] = self.model.addVar(vtype=GRB.INTEGER,lb=0, name='Backup_Capacity[%s,%s]' % (i, j))
            #self.BackupCapacity[i,j] = self.model.addVar(lb=0, name='Backup_Capacity[%s,%s]' % (i, j))
        self.model.update()
          
        for i,j in self.Links:
            for s,d in self.Links:
                self.bBackupLink[i,j,s,d] = self.model.addVar(vtype=GRB.BINARY,name='Backup_Link[%s,%s,%s,%s]' % (i, j, s, d))
        self.model.update()
         
        for i,j in self.Links:
            for k in range(NumSamples):
                self.z[k,i,j] = self.model.addVar(lb=0,name='z[%s][%s][%s]' % (k,i,j))
        self.model.update()
        
        for i,j in self.Links: 
            self.z0[i,j] = self.model.addVar(lb=-GRB.INFINITY,name='z0[%s][%s]' %(i,j))
        self.model.update()
         
        self.model.modelSense = GRB.MINIMIZE
        
        self.model.setObjective(quicksum(self.BackupCapacity[i,j] for i,j in self.Links))
        self.model.update()
         
            
        #------------------------------------------------------------------------#
        #                    Constraints definition                              #
        #                                                                        #
        #                                                                        #
        #------------------------------------------------------------------------#
          
        # Buffer probability I
        for i,j in self.Links:
            self.model.addConstr(self.z0[i,j] + 1/(NumSamples*Survivability)*quicksum(self.z[k,i,j] for (k) in range(NumSamples)) <= 0,'[CONST]Buffer_Prob_I[%s][%s]'%(i,j))
        self.model.update()
         
        # Link capacity constraints
        for i,j in self.Links:
            for k in range(NumSamples):
                if Gamma == None:
                    self.model.addConstr((quicksum(self.bBackupLink[i,j,s,d]*Capacity[k,s,d] for s,d in self.Links) - self.BackupCapacity[i,j] - self.z0[i,j]) <= self.z[k,i,j],'[CONST]Buffer_Prob_II[%s][%s][%s]' % (k,i,j))
                else:    
                    self.model.addConstr((quicksum(self.bBackupLink[i,j,s,d]*Capacity[k,s,d] for s,d in self.Links) - self.BackupCapacity[i,j] - self.z0[i,j])*Gamma[k] <= self.z[k,i,j],'[CONST]Buffer_Prob_II[%s][%s][%s]' % (k,i,j))
        self.model.update()
        
        # Link capacity constraints
        for i,j in self.Links:
            for k in range(NumSamples):
                self.model.addConstr(self.z[k,i,j] >= 0,'[CONST]Buffer_Prob_III[%s][%s][%s]' % (k,i,j))
        self.model.update()
         
        for i in Nodes:
            for s,d in self.Links:
                # Flow conservation constraints
                if i == s:
                    self.model.addConstr(quicksum(self.bBackupLink[i,j,s,d] for i,j in self.Links.select(i,'*')) - 
                                           quicksum(self.bBackupLink[j,i,s,d] for j,i in self.Links.select('*',i)) == 1,'Flow1[%s,%s,%s]' % (i,s,d))
                # Flow conservation constraints
                elif i == d:
                    self.model.addConstr(quicksum(self.bBackupLink[i,j,s,d] for i,j in self.Links.select(i,'*')) - 
                                           quicksum(self.bBackupLink[j,i,s,d] for j,i in self.Links.select('*',i)) == -1,'Flow2[%s,%s,%s]' % (i,s,d))
                # Flow conservation constraints
                else:    
                    self.model.addConstr(quicksum(self.bBackupLink[i,j,s,d] for i,j in self.Links.select(i,'*')) - 
                                           quicksum(self.bBackupLink[j,i,s,d] for j,i in self.Links.select('*',i)) == 0,'Flow3[%s,%s,%s]' % (i,s,d))
        self.model.update()
                 
         
    def optimize(self, MipGap=None, TimeLimit = None, LogLevel = None):
        """ Optimize the defined  model.
    
        Parameters
        ----------
        MipGap : desired gap
        TimeLimit : time limit
        LogLevel: log level 1 for printing all optimal variables and None otherwise
        
        Returns
        -------
        BackupCapacity: The total capacity assigned per backup link
        BackupRoutes: The set of selected backup links 
           A tuple list with all paths for edge (s,d) that uses (i,j).
    
        """ 
        self.model.write('bpbackup.lp')
         
        if MipGap != None:
            self.model.params.MIPGap = MipGap
        if TimeLimit != None:
            self.model.params.timeLimit = TimeLimit
        # Compute optimal solution
        self.model.optimize()
         
        # Print solution
        if self.model.status == GRB.Status.OPTIMAL:
            
            if LogLevel == 1:
                for v in self.model.getVars():
                    print('%s %g' % (v.varName, v.x))
                    
            self.BackupCapacitySolution = self.model.getAttr('x', self.BackupCapacity)
            self.BackupRoutesSolution = self.model.getAttr('x', self.bBackupLink)
            
            self.BackupLinksSolution={}
            for link in self.BackupCapacitySolution:
                if self.BackupCapacitySolution[link] > 0.0001:
                    if (len(self.BackupLinksSolution) == 0):
                        self.BackupLinksSolution=[link]
                    else:
                        self.BackupLinksSolution=self.BackupLinksSolution+[link]
            
#             #SuperQuantileSolution = self.model.getAttr('x', self.z0)
#             ZNotSolution = {}
#             ZSolution = {}
#             for i,j in self.Links:
#                 for k in range(self.K):
#                     name='z[%s][%s][%s]'%(k,i,j)
#                     v = self.model.getVarByName(name)
#                     ZSolution[k,i,j]=v.x
#                 name='z0[%s][%s]'%(i,j)
#                 v = self.model.getVarByName(name)
#                 ZNotSolution[i,j]=v.x
#                 
#             LHS={}
#             for i,j in self.Links:
#                 for k in range(self.K):
#                     LHS[k,i,j]=0
#                     Psd=0
#                     for s,d in self.Links:
#                         Psd=Psd+BackupRoutes[i,j,s,d]*self.Capacity[k,s,d]
#                     LHS[k,i,j]=Psd-BackupCapacity[i,j]-ZNotSolution[i,j]
#                     if LogLevel == 1:
#                         print('LHS[%s,%s,%s]=%g'%(k,i,j,LHS[k,i,j]))
                            
        else:
            print('Optimal value not found!\n')
            self.BackupCapacitySolution = []
            self.BackupRoutesSolution = {}
            self.BackupLinksSolution = {}
#             LHS = {}
             
#         return BackupCapacity,BackupRoutes,BackupLinks,LHS
        return self.BackupCapacitySolution,self.BackupRoutesSolution,self.BackupLinksSolution    
    
    
    def save(self, filename): 
        """Save the optimal backup network to the file ``filename``.""" 
        
        data = {"links": [i for i in self.BackupCapacitySolution],
                "capacities": [self.BackupCapacitySolution[i] for i in self.BackupCapacitySolution],
                "routes": [i for i in self.BackupRoutesSolution],
                "status": [self.BackupRoutesSolution[i] for i in self.BackupRoutesSolution]}
        f = open(filename, "w") 
        json.dump(data, f) 
        f.close() 
 
 
    def reset(self):
        '''
        Reset model solution.
        '''
        self.model.reset()