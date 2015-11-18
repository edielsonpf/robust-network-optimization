#########################################################
#			SETS  NAD PARAMETERS DEFINITION				#
#########################################################
param n >= 0;

set NODES = 1..n;	# set of nodes

set LINKS within (NODES cross NODES);		# set of links between nodes

param capacity_P {LINKS} >= 0;         		# capacity of each link at primary network  

param mean {LINKS} >= 0;         		# capacity of each link at primary network  

param variance {LINKS} >= 0;         		# capacity of each link at primary network  

param nlinks >= 0;

param p >=0;

param epsilon >= 0;

param invstd >=0;

#########################################################
# 				VARIABLES DEFINITION					#
#########################################################

var CB{(i,j) in LINKS} integer;	#capacity per backup link

var B{NODES,NODES,NODES,NODES} binary; #binary variable to define if backup link is active or not

#########################################################
#					MODEL DEFINITION					#
# The objective is to minimize the backup capcity		#
#########################################################

minimize BackupCapacity: sum{(i,j) in LINKS} CB[i,j];

#subject to

subject to Capacity {(i,j) in LINKS}: CB[i,j] >= sum{(s,d) in LINKS} (mean[s,d]+sqrt(variance[s,d])*invstd)*B[i,j,s,d]*capacity_P[s,d];

subject to Flow2 {i in NODES, (s,d) in LINKS: i=s} : sum{(i,j) in LINKS}B[i,j,s,d] - sum{(j,i) in LINKS} B[j,i,s,d] = 1; 
subject to Flow3 {i in NODES, (s,d) in LINKS: i=d} : sum{(i,j) in LINKS}B[i,j,s,d] - sum{(j,i) in LINKS} B[j,i,s,d] = -1; 
subject to Flow1 {i in NODES, (s,d) in LINKS: i!=s and i!=d} : sum{(i,j) in LINKS}B[i,j,s,d] - sum{(j,i) in LINKS} B[j,i,s,d] = 0; 



