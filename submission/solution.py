from amplpy import AMPL, Environment

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix

import sys
from collections import deque


def calc_saving(unrouted, i, distMatrix):
    savings = [ (distMatrix[i,0] + distMatrix[0,j] - distMatrix[i,j], - distMatrix[i,j], i, j) for j in unrouted if i != j ]
    savings.sort()
    return savings


def sequential_savings_init(distMatrix, demandList, truckCapacity = 1.0):
    
    supConst = 1e-10
    
    N = len(distMatrix)

    # nodes not in a route 
    # 0 = depot that will not be in a route
    unrouted = set(range(1, N))
    
    # generate a list of node's indices for route inititialization 
    customerIndices = list(range(1, N))
    customerIndices.sort(reverse = True, key = lambda i: ( distMatrix[0][i],i) )
    
    solution = [0]
    savings = None
    emerging_route_nodes = None

    while unrouted:

        # Initialize a new route
        if not savings:
            
            while True:
                customer = customerIndices.pop()
                if customer in unrouted:
                    break
                
            emerging_route_nodes = deque([customer])
            unrouted.remove(customer)
            
            route_demand = demandList[customer]
        
            savings = calc_saving(unrouted, customer, distMatrix)
        

        while len(savings) > 0:

            # i is the one to merge with
            # j is the candidate to be merged
            _, _, i, j = savings.pop()
            
            cw_saving = distMatrix[i,0] + distMatrix[0,j] - distMatrix[i,j]

            if cw_saving < 0.0:
                savings = []
                break
            
            if not j in unrouted:
                continue
    
            if truckCapacity and route_demand + demandList[j] - supConst > truckCapacity:
                continue
                
            # it is still a valid merge?
            do_left_merge = emerging_route_nodes[0] == i
            do_right_merge = emerging_route_nodes[-1] == i and\
                             len(emerging_route_nodes) > 1
            if not (do_left_merge or do_right_merge):
                continue
               
            # update the route demand
            route_demand += demandList[j]
            
            if do_left_merge:
                emerging_route_nodes.appendleft(j)
            if do_right_merge:
                emerging_route_nodes.append(j)

            unrouted.remove(j)

            savings += calc_saving(unrouted, j, distMatrix)
            savings.sort()
        
        
        emerging_route_nodes.append(0)
        solution += emerging_route_nodes
        emerging_route_nodes = None
                 
    return solution


def main():
    
    pathEnv = sys.argv[1]
    pathModel = sys.argv[2]
    pathData = sys.argv[3]

    ampl = AMPL(Environment("/Users/itsalfantasy/Documents/ampl_macos64"))
    #ampl = AMPL(Environment(pathEnv))
    
    ampl.option['ampl_include'] = 'models'
    ampl.option['solver'] = 'cplex'
    ampl.read('/Users/itsalfantasy/Documents/ampl_macos64/minimart_project/flp_model.mod')
    ampl.readData('/Users/itsalfantasy/Documents/ampl_macos64/minimart_project/minimart-I-50.dat')

    #ampl.read(pathModel)
    #ampl.readData(pathData)
    
    ampl.solve()


    # after AMPL solved the FLP
    # take the problem parameters
    n = ampl.getParameter('n').value()
    minimart_range = ampl.getParameter('range').value()
    Vc = ampl.getParameter('Vc').value()
    Fc = ampl.getParameter('Fc').value()
    capacity = ampl.getParameter('capacity').value()

    # now take the locations parameters
    Cx = ampl.getParameter('Cx').getValues().toList()
    Cy = ampl.getParameter('Cy').getValues().toList()
    Dc = ampl.getParameter('Dc').getValues().toList()
    installed = ampl.getVariable('installed').getValues().toList()

    
    # transforma into pandas DataFrame
    cx_df = pd.DataFrame(Cx)
    cy_df = pd.DataFrame(Cy)
    dc_df = pd.DataFrame(Dc)
    installed_df = pd.DataFrame(installed)

    # final form of the pandas DataFrame
    df = pd.DataFrame(columns=['Cx', 'Cy', 'Dc', 'installed'], dtype=np.float64)
    df['Cx'] = cx_df[1]
    df['Cy'] = cy_df[1]
    df['Dc'] = dc_df[1]
    df['installed'] = installed_df[1]


    # this contains the parameter of the installed locations
    inst_df = df[ df['installed'] == 1 ]


    # create a list of coordinate points of all installed locations
    coord_list = list()
    for _, row in inst_df.iterrows():
        new_point = [ row['Cx'], row['Cy'] ]
        coord_list.append(new_point)


    # create a list of the demands of the installed locations
    # 0 for the depot
    # 1 for each other node
    demand_list = list()
    demand_list.append(0)
    for _ in range(1, len(inst_df.index)):
        demand_list.append(1)
    

    # distance matrix between each installed location
    dist_matrix = distance_matrix(coord_list, coord_list)

    # FIND THE SOLUTION HERE <-----------------------------------------------------------
    # find the rounting solution based on the location installed
    routning_solution = sequential_savings_init(dist_matrix, demand_list, capacity)


    # FIND THE COSTS HERE <--------------------------------------------------------------
    # find the installation cost for all locations
    total_installation_cost = 0.0
    for _, row in inst_df.iterrows():
        total_installation_cost += row['Dc']

    # find refurbishment cost for alla locations
    total_refurbishment_cost = 0.0
    for i in range(1, len(routning_solution)):
        total_refurbishment_cost += dist_matrix[routning_solution[i-1], routning_solution[i]] * Vc
        if routning_solution[i] == 0:
            total_refurbishment_cost += Fc
    
    final_cost = total_installation_cost + total_refurbishment_cost

    # the indices of the installed locations
    index_list = list()
    for elem in inst_df.index:
        index_list.append(elem+1)
    
    # the routes list
    routes_list = list()
    for elem in routning_solution:
        routes_list.append(index_list[elem])
    

    # PRINTING FINAL RESULTS <-------------------------------------------------------------
    print('Installation Cost : ' + str(total_installation_cost))
    print('Refurbishment Cost : ' + str(total_refurbishment_cost))
    print('Total Cost : ' + str(final_cost))
    print('Installed Location : ' + str(index_list))
    print('Routes : ' + str(routes_list))


    result_dict = {
        'installation cost': total_installation_cost,
        'refurbishment cost': total_refurbishment_cost,
        'total cost': final_cost,
        'installed location': index_list,
        'routes': routes_list,
    }

    return result_dict


if __name__ == "__main__":
    main()