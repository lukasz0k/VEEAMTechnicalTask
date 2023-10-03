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

This function creates lists of sub folders in the source and replica folders and then subjects  
them to the same processes as the main folders.  

# 03.10 Updates

Another problem turned out to be managing files inside subfolders. The synchronizer function was not good at managing them.  
It created subfolders in the replica folder when they appeared in the source folder. Any changes occurring inside the   
subfolders were not recorded by the synnchronizer function.

I decided to create a synchronize_subfolders function that creates a list of subfolders and updates them in a loop.  
By creating new subfolders, copying files and deleting them from the replica folder.  
This function creates lists of sub folders in the source and replica folders and then subjects them to the same processes as the main folders.  

The problem in implementing this solution was the correct navigation of subfolder paths inside the main folders.
After solving this problem, I decided to move the while loop to the main function.   
This allowed for better management of logger entries and better supervision of the operation of two functions.
