'''
Created on Nov 23, 2015
 
@author: Edielson P. Frigieri
'''
from gurobipy import Model, GRB, quicksum, tuplelist
import json
import math
 
class BFPBackupNetwork_Continuous(object):
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
                         
    def LoadModel(self,Gamma,Nodes,Links,Capacity,Survivability,NumSamples):
        """ Load model.
    
        Parameters
        ----------
        Gamma : importance sampling vector
        
        """         
        self.Links = tuplelist(Links)
        self.Capacity = Capacity
        self.Nodes=Nodes
        
        # Create optimization model
        self.model = Model('Backup')
     
        # Create variables
        for i,j in self.Links:
            self.BackupCapacity[i,j] = self.model.addVar(vtype=GRB.CONTINUOUS,lb=0, name='Backup_Capacity[%s,%s]' % (i, j))
            #self.BackupCapacity[i,j] = self.model.addVar(lb=0, name='Backup_Capacity[%s,%s]' % (i, j))
        self.model.update()
          
        for s,d in self.Links:
            for i,j in self.Links:
                self.bBackupLink[s,d,i,j] = self.model.addVar(vtype=GRB.BINARY,name='BackupLink[%s,%s,%s,%s]' % (s, d, i, j))
        self.model.update()
         
        for i,j in self.Links:
            for k in range(NumSamples):
                self.z[k,i,j] = self.model.addVar(lb=0,name='z[%s][%s,%s]' % (k,i,j))
        self.model.update()
        
        for i,j in self.Links: 
            self.z0[i,j] = self.model.addVar(lb=-GRB.INFINITY,name='z0[%s,%s]' %(i,j))
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
            self.model.addConstr(self.z0[i,j] + 1/(NumSamples*Survivability)*quicksum(self.z[k,i,j] for (k) in range(NumSamples)) <= 0,'[CONST]Buffer_Prob_I[%s,%s]'%(i,j))
        self.model.update()
         
        # Link capacity constraints
        for i,j in self.Links:
            for k in range(NumSamples):
                if Gamma == None:
                    self.model.addConstr((quicksum(self.bBackupLink[s,d,i,j]*Capacity[k,s,d] for s,d in self.Links) - self.BackupCapacity[i,j] - self.z0[i,j]) <= self.z[k,i,j],'[CONST]Buffer_Prob_II[%s][%s,%s]' % (k,i,j))
                else:    
                    self.model.addConstr((quicksum(self.bBackupLink[s,d,i,j]*Capacity[k,s,d] for s,d in self.Links) - self.BackupCapacity[i,j] - self.z0[i,j])*Gamma[k] <= self.z[k,i,j],'[CONST]Buffer_Prob_II[%s][%s,%s]' % (k,i,j))
        self.model.update()
        
        # Link capacity constraints
        for i,j in self.Links:
            for s,d in Links:
                self.model.addConstr(self.bBackupLink[s,d,i,j] <= self.BackupCapacity[i,j],'[CONST]Buffer_Prob_III[%s,%s,%s,%s]' % (s,d,i,j))
        self.model.update()

        
        # Link capacity constraints
#        for i,j in self.Links:
#            for k in range(NumSamples):
#                self.model.addConstr(self.z[k,i,j] >= 0,'[CONST]Buffer_Prob_III[%s][%s,%s]' % (k,i,j))
#        self.model.update()
         
        for i in Nodes:
            for s,d in self.Links:
                # Flow conservation constraints
                if i == s:
                    self.model.addConstr(quicksum(self.bBackupLink[s,d,i,j] for i,j in self.Links.select(i,'*')) - 
                                           quicksum(self.bBackupLink[s,d,l,i] for l,i in self.Links.select('*',i)) == 1,'Flow(%s,%s,%s)'%(i,s,d))
                # Flow conservation constraints
                elif i == d:
                    self.model.addConstr(quicksum(self.bBackupLink[s,d,i,j] for i,j in self.Links.select(i,'*')) - 
                                           quicksum(self.bBackupLink[s,d,l,i] for l,i in self.Links.select('*',i)) == -1,'Flow(%s,%s,%s)'%(i,s,d))
                # Flow conservation constraints
                else:    
                    self.model.addConstr(quicksum(self.bBackupLink[s,d,i,j] for i,j in self.Links.select(i,'*')) - 
                                           quicksum(self.bBackupLink[s,d,l,i] for l,i in self.Links.select('*',i)) == 0,'Flow(%s,%s,%s)'%(i,s,d))
                # Flow conservation constraints
#        self.model.addConstr(
#                (self.bBackupLink.sum('*',j,s,d) == self.bBackupLink.sum(j,'*',s,d)
#                for s,d in self.Links for i in Nodes),'Flow[%s,%s,%s]' % (i,s,d))
#        self.model.addConstrs(
#       (quicksum(self.bBackupLink[i,j,s,d] for i,j in self.Links.select('*',j)) ==
#         quicksum(self.bBackupLink[j,k,s,d] for j,k in self.Links.select(j,'*'))
#         for s,d in self.Links for j in Nodes), 'Flow')

                
                
        self.model.update()
                 
         
    def Optimize(self, MipGap=None, TimeLimit = None, LogLevel = None):
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
            
            #print(self.BackupCapacitySolution)
#            for route in self.BackupRoutesSolution:
#                if(self.BackupRoutesSolution[route] > 0 ):  
#                    print('[2]%s: %d'%(route,self.BackupRoutesSolution[route]))
            
            
            BackupRoute = dict()
            for sd in self.Links:
                temp = dict()
                for ij in self.Links:
                    temp[ij] = 0
                BackupRoute[sd] = temp
#            print(BackupRoute)         
            
            for s,d,i,j in self.BackupRoutesSolution:
                sd=(s,d)
                ij=(i,j)
                BackupRoute[sd][ij]=self.BackupRoutesSolution[s,d,i,j]
#                if(self.BackupRoutesSolution[s,d,i,j] > 0 ):
#                    print('[1]%s,%s,%s,%s: %d'%(s,d,i,j,self.BackupRoutesSolution[s,d,i,j]))
            
#            print(BackupRoute)
            
            self.BackupLinksSolution={}
            self.HatBackupCapacity={}
            for link in self.BackupCapacitySolution:
                if self.BackupCapacitySolution[link] < 1 and self.BackupCapacitySolution[link] > 0.001:
                    self.HatBackupCapacity[link]=math.ceil(self.BackupCapacitySolution[link])
                else:
                    self.HatBackupCapacity[link]=math.floor(self.BackupCapacitySolution[link])
                if self.HatBackupCapacity[link] > 0:
                    if (len(self.BackupLinksSolution) == 0):
                        self.BackupLinksSolution=[link]
                    else:
                        self.BackupLinksSolution=self.BackupLinksSolution+[link]
        
            
#            for s,d in self.Links:
#                print('(%s,%s): '%(s,d)),
#                for i,j in self.BackupLinksSolution:
#                    if(self.BackupRoutesSolution[s,d,i,j] > 0):
#                        print('(%s,%s): %d,'%(i,j,self.BackupRoutesSolution[s,d,i,j])),
#                print('\n')
            for sd in self.Links:
                for ij in self.Links:
                    if(sd == ij):
                        if(BackupRoute[sd][ij] > 0):
                            for kl in self.Links:
                                if(kl != ij):
#                                    print('Changed! %s,%s'%(sd,kl))
                                    BackupRoute[sd][kl]=0

            for sd in self.Links:
                print('%s:'%(str(sd)))
                print('\t'),
                for ij in self.Links:
                    if(BackupRoute[sd][ij] > 0):
                        print('%s: %d,'%(str(ij),BackupRoute[sd][ij])),
                print('\n')

                
#            for i in self.Nodes:
#                for s,d in self.Links:
#                    flow=0
#                    for i,j in self.Links.select(i,'*'):
#                        flow=flow+self.BackupRoutesSolution[s,d,i,j]
#                    for l,i in self.Links.select('*',i):
#                        flow=flow-self.BackupRoutesSolution[s,d,l,i]    
#                    if(s==i):
#                        print('Flow(%s,%s,%s)=%d and must be equal to 1'%(i,s,d,flow))
#                    elif(d==i):
#                        print('Flow(%s,%s,%s)=%d and must be equal to -1'%(i,s,d,flow))
#                    else:
#                        print('Flow(%s,%s,%s)=%d and must be equal to 0'%(i,s,d,flow))
        else:
            print('Optimal value not found!\n')
            self.BackupCapacitySolution = []
            self.BackupRoutesSolution = {}
            self.BackupLinksSolution = {}
            
        return self.BackupCapacitySolution,self.BackupRoutesSolution,self.BackupLinksSolution,self.HatBackupCapacity 
    
    
    def SaveBakupNetwork(self, file_name): 
        """Save the optimal backup network to the file ``file_name``.""" 
        
        data = {"links": [i for i in self.BackupCapacitySolution],
                "capacities": [self.BackupCapacitySolution[i] for i in self.BackupCapacitySolution],
                "routes": [i for i in self.BackupRoutesSolution],
                "status": [self.BackupRoutesSolution[i] for i in self.BackupRoutesSolution]}
        f = open(file_name, "w") 
        json.dump(data, f) 
        f.close() 
 
    def LoadBackupNetwork(self,file_name): 
        """Load a backup network from the file ``file_name``.  
        Returns the backup network solution saved in the file. 
      
        """ 
        f = open(file_name, "r") 
        data = json.load(f) 
        f.close() 
        
        self.BackupCapacitySolution = {}
        self.BackupRoutesSolution = {}
        self.BackupLinksSolution = {}
        
        links = [i for i in data["links"]]
        capacities = [i for i in data["capacities"]] 
        routes = [i for i in data["routes"]] 
        status = [i for i in data["status"]]
        
        IndexAux=0
        for i,j in links:
            self.BackupCapacitySolution[i,j]=capacities[IndexAux]
            IndexAux=IndexAux+1
        
        self.HatBackupCapacity={}
        for link in self.BackupCapacitySolution:
            if self.BackupCapacitySolution[link] < 1 and self.BackupCapacitySolution[link] > 0.001:
                self.HatBackupCapacity[link]=math.ceil(self.BackupCapacitySolution[link])
            else:
                self.HatBackupCapacity[link]=math.floor(self.BackupCapacitySolution[link])
            if self.HatBackupCapacity[link] > 0:
                if (len(self.BackupLinksSolution) == 0):
                    self.BackupLinksSolution=[link]
                else:
                    self.BackupLinksSolution=self.BackupLinksSolution+[link]
        
        IndexAux=0
        for s,d,i,j in routes:
            self.BackupRoutesSolution[s,d,i,j]=status[IndexAux]
            IndexAux=IndexAux+1
            
        return self.BackupCapacitySolution,self.BackupRoutesSolution,self.BackupLinksSolution, self.HatBackupCapacity
    
    def ResetModel(self):
        '''
        Reset model solution.
        '''
        self.BackupCapacity = {}
        self.bBackupLink = {}
        self.z0 = {}
        self.z = {}
        if self.model:
            self.model.reset()