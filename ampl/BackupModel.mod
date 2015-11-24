#########################################################
#			SETS  NAD PARAMETERS DEFINITION				#
#########################################################
param n >= 0;

set NODES = 1..n;	# set of nodes
#set PATHS = 1..2;

set LINKS within (NODES cross NODES);		# set of links between nodes

param link_paths {LINKS};

param backup_paths {LINKS};

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

#var B{NODES,NODES,NODES,NODES} binary; #binary variable to define if backup link is active or not

var Y{LINKS,PATHS} binary;

#########################################################
#					MODEL DEFINITION					#
# The objective is to minimize the backup capcity		#
#########################################################

minimize BackupCapacity: sum{(i,j) in LINKS} CB[i,j];

#subject to

subject to Capacity {(i,j) in LINKS}: CB[i,j] >= sum{k in PATHS}(mean[i,j]+variance[i,j])*Y[i,j,k];

subject to UniquePath{(s,d) in LINKS}: sum{k in PATHS}Y[s,d,k] = 1;

#subject to Flow2 {i in NODES, (s,d) in LINKS: i=s} : sum{(i,j) in LINKS}B[i,j,s,d] - sum{(j,i) in LINKS} B[j,i,s,d] = 1; 
#subject to Flow3 {i in NODES, (s,d) in LINKS: i=d} : sum{(i,j) in LINKS}B[i,j,s,d] - sum{(j,i) in LINKS} B[j,i,s,d] = -1; 
#subject to Flow1 {i in NODES, (s,d) in LINKS: i!=s and i!=d} : sum{(i,j) in LINKS}B[i,j,s,d] - sum{(j,i) in LINKS} B[j,i,s,d] = 0; 



