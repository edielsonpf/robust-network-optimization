#########################################################
#			SETS  NAD PARAMETERS DEFINITION				#
#########################################################
param N >= 0;
param NLINKS >=0; 
param MSTART >=0;

set NODES = 1..N;	# set of nodes

set M = MSTART..NLINKS;		# table index upper bound is N*(N-1)

set LINKS within (NODES cross NODES);		# set of links between nodes

param K >=0;  # big M value

param gamma {M} >= 0;         				# minimum capacity resulted for m links considering probability constraint

param capacity_P {LINKS} >= 0;         		# capacity of each link at primary network  

#########################################################
# 				VARIABLES DEFINITION					#
#########################################################

var CB{(i,j) in LINKS} >= 0;	#capacity per backup link

var B{NODES,NODES,NODES,NODES} binary; #binary variable to define if backup link is active or not

var THETA{NODES,NODES,NODES,NODES} >=0; #used for linearization
var V{(i,j) in LINKS} >=0 ;	#used for linearization
var X{NODES,NODES,M} binary; #used for linearization
var Y{NODES,NODES,M} >=0; #used for linearization

#########################################################
#					MODEL DEFINITION					#
# The objective is to minimize the backup capcity		#
#########################################################

minimize BackupCapacity: sum{(i,j) in LINKS} CB[i,j];

#subject to

subject to Capacity {(i,j) in LINKS}: CB[i,j] >= sum{m in M} Y[i,j,m]*gamma[m] + sum{(s,d) in LINKS} THETA[i,j,s,d];

subject to defnV{(i,j) in LINKS, (s,d) in LINKS}: V[i,j] + THETA[i,j,s,d] >= capacity_P[s,d]*B[i,j,s,d];

subject to pickoneX{(i,j) in LINKS}: sum{m in M} X[i,j,m]=1;

subject to limitB{(i,j) in LINKS}: sum{(s,d) in LINKS} B[i,j,s,d] <= sum{m in M} m*X[i,j,m];

subject to defY1{(i,j) in LINKS, m in M}: Y[i,j,m] >= V[i,j] + K*(X[i,j,m]-1);
subject to defY2{(i,j) in LINKS, m in M}: Y[i,j,m] <= K*X[i,j,m];

subject to Flow2 {i in NODES, (s,d) in LINKS: i=s} : sum{(i,j) in LINKS}B[i,j,s,d] - sum{(j,i) in LINKS} B[j,i,s,d] = 1; 
subject to Flow3 {i in NODES, (s,d) in LINKS: i=d} : sum{(i,j) in LINKS}B[i,j,s,d] - sum{(j,i) in LINKS} B[j,i,s,d] = -1; 
subject to Flow1 {i in NODES, (s,d) in LINKS: i!=s and i!=d} : sum{(i,j) in LINKS}B[i,j,s,d] - sum{(j,i) in LINKS} B[j,i,s,d] = 0; 



