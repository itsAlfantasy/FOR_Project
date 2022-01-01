from collections import deque

def calc_saving(unrouted, i, distMatrix):
    savings = [ (distMatrix[i,0] + distMatrix[0,j] - distMatrix[i,j], - distMatrix[i,j], i, j) for j in unrouted if i != j ]
    savings.sort()
    return savings


def sequential_savings_init(distMatrix, demandList, truckCapacity = 1.0):
    
    C_EPS = 1e-10
    
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
    
            if truckCapacity and route_demand + demandList[j] - C_EPS > truckCapacity:
                continue # next savings
                
            # it is still a valid merge?
            do_left_merge = emerging_route_nodes[0] == i
            do_right_merge = emerging_route_nodes[-1] == i and\
                             len(emerging_route_nodes) > 1
            if not (do_left_merge or do_right_merge):
                continue # next savings
               
            
            # update the route demand
            route_demand += demandList[j]
            

            if do_left_merge:
                emerging_route_nodes.appendleft(j)
            if do_right_merge:
                emerging_route_nodes.append(j)

            unrouted.remove(j)
            
            # update the savings list
            savings += calc_saving(unrouted, j, distMatrix)
            savings.sort()
        
        
        emerging_route_nodes.append(0)
        solution += emerging_route_nodes
        emerging_route_nodes = None
                 
    return solution