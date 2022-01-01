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

