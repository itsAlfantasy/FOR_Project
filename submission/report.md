# Report

## **How To Run** 🏃🏻‍♂️
to run the file ```solution.py``` you'll need three parameters:  
• **arg1** : *absolute path of ampl environment*  
• **arg2** : *absolute path of the file model*  
• **arg3** : *absolute path of the data file*

the enter the command :
```
python3 solution.py arg1 arg2 arg3
```

## **Heuristic Description** 📖
the problem has been splitted in two parts :  
• Facility Location Problem (FLP)  
• Vehicle Routing Problem (VRP)

we first solved the FLP using the AMPL Python libraries (Amplpy) and then applied an heuristic for the VRP on the optiomal solution found by AMPL.

### **Vehicle Routing Problem Heuristic** 🚚

we use the Clarke Wright Saving Algorithm:

STEP 1:	Calculate the savings s(i, j) = d(D, i) + d(D, j) - d(i, j) for every pair (i, j) of demand points.  
STEP 2:	Rank the savings s(i, j) and list them in descending order of magnitude. This creates the "savings list." Process the savings list beginning with the topmost entry in the list (the largest s(i, j)).  
STEP 3:	For the savings s(i, j) under consideration, include link (i, j) in a route if no route constraints will be violated through the inclusion of (i, j) in a route, and if:
a. Either, neither i nor j have already been assigned to a route, in which case a new route is initiated including both i and j.

b. Or, exactly one of the two points (i or j) has already been included in an existing route and that point is not interior to that route (a point is interior to a route if it is not adjacent to the depot D in the order of traversal of points), in which case the link (i, j) is added to that same route.

c. Or, both i and j have already been included in two different existing routes and neither point is interior to its route, in which case the two routes are merged.

STEP 4:	If the savings list s(i, j) has not been exhausted, return to Step 3, processing the next entry in the list; otherwise, stop: the solution to the VRP consists of the routes created during Step 3. (Any points that have not been assigned to a route during Step 3 must each be served by a vehicle route that begins at the depot D visits the unassigned point and returns to D.)
