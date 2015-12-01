#########################################################
#			SETS  NAD PARAMETERS DEFINITION				#
#########################################################
param n >= 0;

set NODES = 1..n;	# set of nodes
set LINKS within (NODES cross NODES);		# set of links between nodes
set PATHS;

set PSD{LINKS};
set PIJ{LINKS};

param capacity_P {LINKS} >= 0;         		# capacity of each link at primary network  

param mean {PATHS} >= 0;         		# capacity of each link at primary network  

param std {PATHS} >= 0;         		# capacity of each link at primary network  

param nlinks >= 0;

param p >=0;

param epsilon >= 0;

param invstd >=0;

#########################################################
# 				VARIABLES DEFINITION					#
#########################################################

var CB{(i,j) in LINKS};	#capacity per backup link

var Y{PATHS} binary;

var U{(i,j) in LINKS} >=0;
var R{NODES,NODES,PATHS} >=0;
#########################################################
#					MODEL DEFINITION					#
# The objective is to minimize the backup capcity		#
#########################################################

minimize BackupCapacity: sum{(i,j) in LINKS} CB[i,j];

#subject to

subject to UniquePath{(s,d) in LINKS}: sum{bp in PSD[s,d]}Y[bp] = 1;

subject to Capacity {(i,j) in LINKS}: CB[i,j] >= sum{pth in PIJ[i,j]}mean[pth]*Y[pth] + U[i,j]*invstd;;
#subject to Capacity {(i,j) in LINKS}: CB[i,j] >= sum{pth in PIJ[i,j]}mean[pth]*sum{bp in PSD[i,j]}Y[bp] + U[i,j]*invstd;;

subject to Reformulation{(i,j) in LINKS}: sum{pth in PIJ[i,j]}R[i,j,pth]^2 <= U[i,j]^2;

subject to Reformulation2{(i,j) in LINKS, pth in PIJ[i,j]}: std[pth]*Y[pth] = R[i,j,pth];
#subject to Reformulation2{(i,j) in LINKS, pth in PIJ[i,j]}: std[pth]*sum{bp in PSD[i,j]}Y[bp] = R[i,j,pth];


