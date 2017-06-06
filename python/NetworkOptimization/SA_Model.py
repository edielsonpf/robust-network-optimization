"Finds backup paths according to simulated annealing"
#"Based off of paper:  S.P. Brooks and B.J.T. Morgan, Optimization using simulated annealing"
#Author: Matt Johnston, 2010

import random
import math
import copy
import sys

defaultEpsilon = 0.0001
defaultdfile = 'fullSurvive.dat'
defaultProbLinkFail = 0.075

#label = sys.argv[1];
#datafile = sys.argv[2];
#probLinkFail = float(sys.argv[3]);
#epsilon = float(sys.argv[4]);

# label = 'test';
# datafile = 'nsfnetFail.dat';
# probLinkFail = 0.0005;
# epsilon = 1e-5;

def computeGamma(n,epsilon, p):

    return computeActualGamma(n,epsilon, p)
    #start = max(int(math.ceil(n*p)), 1)
    #if n <= 1:
    #    return n
    
    #for gam in range(start,n):
    #    q = (((n-n*p)/(n-gam))**(n-gam)) * (n*p/gam)**gam
    #    if q <= epsilon:
    #        return gam
    #return n

# This method computes the Gamma worst primary capacities on each backup link
# and uses that to compute the total capacity required in the backup network 
def totalBackupCap(links, b, epsilon, p, Cp):
    total = 0;
    for ij in links:
        loads = [Cp[sd] for sd in links if b[sd][ij] > 0]
        numPrimaries = len(loads)
        gam = computeGamma(numPrimaries,epsilon,p);
        gamInt = int(gam)
        gamFrac = gam-gamInt
        loads.sort()
        loads.reverse()
        requiredCap = sum(loads[:gamInt])
        if (gamInt < len(loads)):
            requiredCap = requiredCap + gamFrac * loads[gamInt]
        #print('CB%s=%f'%(str(ij),requiredCap))    
        total = total + requiredCap;
    return total;

def factorial(n):
    if n == 0:
        return 1
    else:
        return n*factorial(n-1)

def nchoosek(n,k):
    return factorial(n) / (factorial(k)*factorial(n-k))

def computeActualGamma(n,epsilon,p):
    q = 0
    for gam in range(n,0,-1):
        q = q + nchoosek(n,gam)*(p**gam)*((1-p)**(n-gam))
        if q > epsilon:
            return min(n,gam)
    return 0;


def randomPath(i, sd, badNodes, nodes, links):
    s = sd[1:-1].split(',')[0] # the node s in '(s,d)'
    d = sd[1:-1].split(',')[1] # the node d in '(s,d)'
    if (s == i): # special case for i = s
        choices = nodes[:]; # copy nodes
        for n in badNodes:  # remove all bad nodes
            choices.remove(n)
        #pchoices.remove(d)   # cant have 1-hop paths here
        random.shuffle(choices)    # randomly order choices
        
        for newNode in choices:
            # try this choice, and if it doesn't work, then try another
            l = '('+i+','+newNode+')' # link (i,newNode)
            newBadNodes = badNodes[:]
            newBadNodes.append(newNode)
            if (links.count(l) > 0):    # if this is actually a link  
                if (newNode == d):
                    return [l]
                else:
                    path = randomPath(newNode,sd,newBadNodes,nodes,links)
                    if (len(path)>0):
                        path.append(l)
                        return path
                    # else, try again
            # else try again
        # no possible choice can give you a path
        return []
    else:
        choices = nodes[:]; # copy nodes
        for n in badNodes:  # remove all bad nodes
            choices.remove(n)
        random.shuffle(choices)    # randomly order choices
        
        for newNode in choices:
            # try this choice, and if it doesn't work, then try another
            l = '('+i+','+newNode+')' # link (i,newNode)
            newBadNodes = badNodes[:]
            newBadNodes.append(newNode)
            if (links.count(l) > 0):    # if this is actually a link  
                if (newNode == d):
                    return [l]
                else:
                    path = randomPath(newNode,sd,newBadNodes,nodes,links)
                    if (len(path)>0):
                        path.append(l)
                        return path
                    # else, try again
            # else try again
        # no possible choice can give you a path
        return []
            
    
def design(dfile, label, probLinkFail, epsilon):
    ## Load data file
    
    datafile = open(dfile,'r')   # read SET NODES := node1 node2 ... noden;
    nodes = datafile.readline().split()
    nodes = nodes[3:]
    nodes[-1] = nodes[-1][:-1]
    numNodes = len(nodes)

    line = datafile.readline()  # set LINKS :=
    line = datafile.readline()
    links = []

    while (not line.rstrip() == ';'):
        a,b = line.split()
        links.append('(' + a + ',' + b + ')')
        line = datafile.readline()

    # read in link loads
    line = datafile.readline()  # param Cp :=
    line = datafile.readline()
    linkLoads = dict();
    while (not line.rstrip() == ';'):
        a,b,c  = line.split()
        linkLoads['(' + a + ',' + b + ')'] = int(c)
        line = datafile.readline()

    blinks = linkLoads.keys()
    for plink in links:
        if blinks.count(plink) == 0:
            linkLoads[plink] = 0
            
    datafile.close()
    numLinks = len(links)
    
    ## initialize backups and Ctotal
    backups = dict()
    for sd in links:
        s = sd[1:-1].split(',')[0] # the node s in '(s,d)'
        sdpath = randomPath(s,sd,[s],nodes,links)
        temp = dict()
        for ij in links:
            if sdpath.count(ij) > 0:
                temp[ij] = 1
            else:
                temp[ij] = 0
        backups[sd] = temp
    Ctotal = totalBackupCap(links,backups,epsilon,probLinkFail, linkLoads)

    T0 = numNodes * max(linkLoads.values()) # numNodes;
    print 'STARTING T = ' + str(T0)
    T = T0
    minT = 1
    rho = 0.95
    noMoveCount = 0
    totalCount = 0
    steadyStateTime = 50*numNodes**2   # number of no moves before you admit you are at steady state... function of problem size
    ## iterate
    while(1):
        #print Ctotal
        totalCount = totalCount + 1
        #print totalCount
        sd = random.choice(links)   # choose a random link
        s = sd[1:-1].split(',')[0] # the node s in '(s,d)'
        path = randomPath(s,sd,[s],nodes,links)
        newBackups = copy.deepcopy(backups)
        for ij in links:
            if path.count(ij) > 0:
                newBackups[sd][ij] = 1
            else:
                newBackups[sd][ij] = 0
        newCtotal = totalBackupCap(links,newBackups,epsilon,probLinkFail, linkLoads)
        #print newCtotal
        q = math.exp(-1.0 * (newCtotal - Ctotal) / max(T,0.01))
        U = random.random()
        if (U < q):  # this happens wp1 if newCtotal < Ctotal, and wp q if newCtotal > Ctotal
            backups = newBackups    # don't need to copy
            if (T < 0.00001):
                if (newCtotal < Ctotal):# | (T > 10**(-6)):
                    noMoveCount = 0
                else:
                    noMoveCount = noMoveCount + 1
            else:
                noMoveCount = 0
            Ctotal = newCtotal
           
        else:
            noMoveCount = noMoveCount+1
        if (totalCount > steadyStateTime):
            print 'REDUCING T to ' + str(rho*T)
            # reduce temperature
            print Ctotal
            if (noMoveCount == totalCount): # if there were no successful changes to arrive in steady state
                # then system is frozen
                break;
            totalCount = 0
            noMoveCount = 0
            T = rho * T

    results = open(label + 'SARouting.out', 'w')
    results.write('\nTotal Backup Capacity: ' + str(Ctotal));
    results.write('\nBackups:\n')
    for link in links:
        results.write(link + '\t')
        for l2 in links:
            if (backups[link][l2] > 0):
                results.write(l2 + ': ' + str(backups[link][l2]) + ', ')
        results.write('\n')
    results.write('\nNum backups / link: \n');
    for link in links:
        results.write(link + '\t' + str(len([sd for sd in links if backups[sd][link] > 0])) + '\n')
    results.close()        

    print 'Final Results:'

    print 'Backup Links: '
    for link in links:
            print link + ': '
            for l2 in links:
                if (backups[link][l2] > 0):
                    print '\t' + l2 + ': ' + str(backups[link][l2])
    print 'Ctotal = ' + str(Ctotal)

#design()
