'''
Created on Nov 23, 2015
 
@author: Edielson P. Frigieri
'''
from gurobipy import Model, GRB, quicksum, tuplelist
import json
import math
 
class BFP_JRD_Model(object):
    """ Class object for buffered failure probability-based model.

    Parameters
    ----------
    Gamma: importance sampling vector
    Nodes: set of nodes
    Connections: set of links
    Links: set of available links
    Capacity: capacities per link based based on random transmission 
    Survivability: desired survivabiliy factor (alpha)
    K: number of random scenarios
    
    Returns
    -------
    WavelengthCapacity: set of capacity per link. 
    AlternativeRoutes: set of assigned routes per links
    
    """         
    
    # Private model object
    model = []
         
    # Private model variables
    WavelengthCapacity = {}
    bAssignedRoute = {}
    z0 = {}
    z = {}
         
    def __init__(self):
        '''
        Constructor
        '''
                         
    def LoadModel(self,Gamma,Nodes,Connections,Links,Capacity,Survivability,NumSamples):
        """ Load model.
    
        Parameters
        ----------
        Gamma : importance sampling vector
        
        """         
        self.Connections = tuplelist(Connections)
        
        self.Links = tuplelist(Links)
        
        self.Capacity = Capacity
               
        # Create optimization model
        self.model = Model('BFP-JRD Model')
     
        # Create variables
        for i,j in self.Links:
            self.WavelengthCapacity[i,j] = self.model.addVar(vtype=GRB.CONTINUOUS,lb=0, name='Wavelength_Capacity[%s,%s]' % (i, j))
        self.model.update()
          
        for i,j in self.Links:
            for s,d in self.Connections:
                self.bAssignedRoute[i,j,s,d] = self.model.addVar(vtype=GRB.BINARY,name='Route[%s,%s,%s,%s]' % (i, j, s, d))
        self.model.update()
         
        for i,j in self.Links:
            for k in range(NumSamples):
                self.z[k,i,j] = self.model.addVar(lb=0,name='z[%s][%s][%s]' % (k,i,j))
        self.model.update()
        
        for i,j in self.Links: 
            self.z0[i,j] = self.model.addVar(lb=-GRB.INFINITY,name='z0[%s][%s]' %(i,j))
        self.model.update()
         
        self.model.modelSense = GRB.MINIMIZE
        
        self.model.setObjective(quicksum(self.WavelengthCapacity[i,j] for i,j in self.Links))
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
                    self.model.addConstr((quicksum(self.bAssignedRoute[i,j,s,d]*Capacity[k,s,d] for s,d in self.Connections) - self.WavelengthCapacity[i,j] - self.z0[i,j]) <= self.z[k,i,j],'[CONST]Buffer_Prob_II[%s][%s][%s]' % (k,i,j))
                else:    
                    self.model.addConstr((quicksum(self.bAssignedRoute[i,j,s,d]*Capacity[k,s,d] for s,d in self.Connections) - self.WavelengthCapacity[i,j] - self.z0[i,j])*Gamma[k] <= self.z[k,i,j],'[CONST]Buffer_Prob_II[%s][%s][%s]' % (k,i,j))
        self.model.update()
        
        # Variable bound constraints
        for i,j in self.Links:
            for k in range(NumSamples):
                self.model.addConstr(self.z[k,i,j] >= 0,'[CONST]Buffer_Prob_III[%s][%s][%s]' % (k,i,j))
        self.model.update()
         
        for i in Nodes:
            for s,d in self.Connections:
                # Flow conservation constraints
                if i == s:
                    self.model.addConstr(quicksum(self.bAssignedRoute[i,j,s,d] for i,j in self.Links.select(i,'*')) - 
                                           quicksum(self.bAssignedRoute[j,i,s,d] for j,i in self.Links.select('*',i)) == 1,'Flow1[%s,%s,%s]' % (i,s,d))
                # Flow conservation constraints
                elif i == d:
                    self.model.addConstr(quicksum(self.bAssignedRoute[i,j,s,d] for i,j in self.Links.select(i,'*')) - 
                                           quicksum(self.bAssignedRoute[j,i,s,d] for j,i in self.Links.select('*',i)) == -1,'Flow2[%s,%s,%s]' % (i,s,d))
                # Flow conservation constraints
                else:    
                    self.model.addConstr(quicksum(self.bAssignedRoute[i,j,s,d] for i,j in self.Links.select(i,'*')) - 
                                           quicksum(self.bAssignedRoute[j,i,s,d] for j,i in self.Links.select('*',i)) == 0,'Flow3[%s,%s,%s]' % (i,s,d))
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
        WavelengthCapacity: The total capacity assigned per backup link
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
                    
            self.WavelengthCapacitySolution = self.model.getAttr('x', self.WavelengthCapacity)
            self.RoutesSolution = self.model.getAttr('x', self.bAssignedRoute)
            
            self.LinksSolution={}
            self.HatWavelengthCapacity={}
            for link in self.WavelengthCapacitySolution:
                if self.WavelengthCapacitySolution[link] < 1 and self.WavelengthCapacitySolution[link] > 0.001:
                    self.HatWavelengthCapacity[link]=math.ceil(self.WavelengthCapacitySolution[link])
                else:
                    self.HatWavelengthCapacity[link]=math.floor(self.WavelengthCapacitySolution[link])
                if self.HatWavelengthCapacity[link] > 0:
                    if (len(self.LinksSolution) == 0):
                        self.LinksSolution=[link]
                    else:
                        self.LinksSolution=self.LinksSolution+[link]
        else:
            print('Optimal value not found!\n')
            self.WavelengthCapacitySolution = []
            self.RoutesSolution = {}
            self.LinksSolution = {}
            
        return self.WavelengthCapacitySolution,self.RoutesSolution,self.LinksSolution,self.HatWavelengthCapacity 
    
    
    def SaveWDNNetwork(self, file_name): 
        """Save the optimal backup network to the file ``file_name``.""" 
        
        data = {"links": [i for i in self.WavelengthCapacitySolution],
                "capacities": [self.WavelengthCapacitySolution[i] for i in self.WavelengthCapacitySolution],
                "routes": [i for i in self.RoutesSolution],
                "status": [self.RoutesSolution[i] for i in self.RoutesSolution]}
        f = open(file_name, "w") 
        json.dump(data, f) 
        f.close() 
 
    def LoadWDNNetwork(self,file_name): 
        """Load a backup network from the file ``file_name``.  
        Returns the backup network solution saved in the file. 
      
        """ 
        f = open(file_name, "r") 
        data = json.load(f) 
        f.close() 
        
        self.WavelengthCapacitySolution = {}
        self.RoutesSolution = {}
        self.LinksSolution = {}
        
        links = [i for i in data["links"]]
        capacities = [i for i in data["capacities"]] 
        routes = [i for i in data["routes"]] 
        status = [i for i in data["status"]]
        
        IndexAux=0
        for i,j in links:
            self.WavelengthCapacitySolution[i,j]=capacities[IndexAux]
            IndexAux=IndexAux+1
        
        self.HatWavelengthCapacity={}
        for link in self.WavelengthCapacitySolution:
            if self.WavelengthCapacitySolution[link] < 1 and self.WavelengthCapacitySolution[link] > 0.001:
                self.HatWavelengthCapacity[link]=math.ceil(self.WavelengthCapacitySolution[link])
            else:
                self.HatWavelengthCapacity[link]=math.floor(self.WavelengthCapacitySolution[link])
            if self.HatWavelengthCapacity[link] > 0:
                if (len(self.LinksSolution) == 0):
                    self.LinksSolution=[link]
                else:
                    self.LinksSolution=self.LinksSolution+[link]
        
        IndexAux=0
        for i,j,s,d in routes:
            self.RoutesSolution[i,j,s,d]=status[IndexAux]
            IndexAux=IndexAux+1
            
        return self.WavelengthCapacitySolution,self.RoutesSolution,self.LinksSolution, self.HatWavelengthCapacity
    
    def ResetModel(self):
        '''
        Reset model solution.
        '''
        self.WavelengthCapacity = {}
        self.bAssignedRoute = {}
        self.z0 = {}
        self.z = {}
        if self.model:
            self.model.reset()