 GENERAL PARAMETERS
param n >= 0; # Number of houses
param range >= 0; # Maximum range
param Vc >= 0;
param Fc >= 0;
param capacity >= 0;


set Houses := 1..n;

param Cx{Houses}; # x coordinate
param Cy{Houses}; # y coordinate
param Dc{Houses}; # costruction cost
param usable{Houses}; # usable house or not

# Distance between Houses
param dist{i in Houses, i2 in Houses} := 
    sqrt((Cx[i2] - Cx[i])^2 + (Cy[i2] - Cy[i])^2);


# MINI-MARKET SET ------------------------------------------------
set Minimarket := setof{i in Houses: usable[i] = 1} (i);


# VARIABLES ------------------------------------------------------

# 1 if the house is installed as mini-market
# 0 otherwise
var installed{Minimarket} binary;

# 1 if house i is connected to mini-market j
var connected{Houses, Minimarket} binary;


# OBJ FUNCTION ---------------------------------------------------

# minimize the installation cost
minimize obj:
    sum{j in Minimarket} installed[j] * Dc[j];


# CONSTRAINTS ----------------------------------------------------

# a house cannot be connected to an uninstalled mini-market
s.t. cannotConnectToUnistalledMinimarket {i in Houses, j in Minimarket} :
    connected[i,j] <= installed[j];

# a mini-market cannot be installed on an unavailable house
s.t. cannotInstallOnUnavailableHouse {j in Minimarket} :
    installed[j] <= usable[j];

# a house must be connected to just one mini-market
s.t. justOneConnection {i in Houses} :
	sum{j in Minimarket} connected[i,j] = 1;

# if connected, the house must be in the range of the mini-market
s.t. const4 {i in Houses, j in Minimarket} :
	connected[i,j] ==> ((range - dist[i,j]) >= 0);