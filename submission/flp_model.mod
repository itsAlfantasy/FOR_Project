# GENERAL PARAMETERS
param n >= 0; # Number of houses
param range >= 0; # Maximum range
param capacity >= 0; # Truck capacity
param Vc >= 0; # Distance fee
param Fc >= 0; # Fixed fee


# BASIC SET ------------------------------------------------------
set Houses := 1..n;


# HOUSE'S PARAMETERS ---------------------------------------------
param Cx{Houses}; # x coordinate
param Cy{Houses}; # y coordinate
param Dc{Houses}; # costruction cost
param usable{Houses}; # usable house or not

# Distance between Houses
param dist{i in Houses, i2 in Houses} := 
    sqrt((Cx[i2] - Cx[i])^2 + (Cy[i2] - Cy[i])^2);


# VARIABLES ------------------------------------------------------

# 1 if the house is installed as mini-market
# 0 otherwise
var installed{Houses} binary;

# OBJ FUNCTION ---------------------------------------------------

# minimize the installation cost
minimize obj:
    sum{i in Houses} installed[i] * Dc[i];


# CONSTRAINTS ----------------------------------------------------

# each house must be in the range on a mini-market
s.t. inRangeConstraint{i in Houses}:
	sum{j in Houses: dist[i,j] < range} installed[j] >= 1;

# a mini-market can be installed only on usable houses
# and on the depot location (1)
s.t. installOnlyOnUsabel{i in Houses: usable[i] = 0}:
	installed[i] = 0;
	
	s.t. depot:
	installed[1] = 1;