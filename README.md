# VEEAMTechnicalTask

This repository was created to provide a solution to a technical task for Veeam

The solution to the task is located in the Synchronizer.py file, to run it, run the Synchronizer.py program in the console window, providing the required input data:  
    1.Source folder path  
    2.Replica folder path  
    3.Period time beetween synchronizations (time in seconds)  
    4.Log file path  
  
Due to the fact that the program contains a solution to the recruitment task, there is also a TaskDecription.pdf file containing documentation regarding the solved problem. The documentation includes a description of individual parts of the code, as well as a description of the steps in solving the problem, along with any resulting problems.

# 02.10 Updates  

The first version of the code was sent on 01.10  

The changes which have been made in main function, they are checking and validating inputs data path.  
Just now, the function also check whether the source folder and logger file are not in the replica folder.  
Also, function check that paths to source folder and replica folder are not the same.
