# Project Planning - Constraint programming

The aim of the project is to develop a constraint satisfaction problem model for project planning. 

## Files

 1. ProjectPlanning.py

    Main python file where the problem is solved using Google Operations Research tools. 
    
 2. Data File.xlsx     
 
      Where all details about projects, contractor details, quotes, dependencies and value of projects.
        
       The file contains four sheets:
      
 
 - In the **Projects sheet** you will find a list of projects, for each 
   projects the jobs that need to be carried out and the months this   
   needs to happen (e.g. Project E required Job J in month M8 and Job A 
   in month M9). 
 - In the **Quotes sheet** you will find a list of contractors and their quotes for each of the jobs they are qualified to carry out
   (e.g. Contractor A charges €230 for Job A). A contractor can only   
   work in one project at a time.    
           
 - In the **Dependencies sheet** you will find a matrix of project dependencies indicating which projects are pre-requisites for
   the delivery of other projects (e.g. Project B can only be taken on, 
   if also Project A is taken on).        
       
- In the **Value sheet** you will find the value of each project (e.g. Project A is worth €500).

##  Problem Statement
The goal is to determine which projects can be delivered and what subcontractors should be contracted while making sure that the overall profit margin is at least €2500. 

## Solution
Below are the tasks carried out in the ProjectPlanning.py file. 

- **Task A**. 
Load the excel file data.xlsx and extract all relevant information. No values are hardcoded and everything is extracted and stored in as pandas dataframe. 

- **Task B**. 
Identifying and creating the decision variables in a CP-SAT model that we need to decide what projects to take on. Also identifying and creating the decision variables we need to decide, which contractor is working on which project and when. Making sure to consider that not all contractors are qualified to work on all jobs and that projects do not run over all months. 

- **Task C.** 
Define and implement the constraint that a contractor cannot work on two projects simultaneously . 

- **Task D**
Define and implement the constraint that if a project is accepted to be delivered then exactly one contractor per job of the project needs to work on it.
- **Task E**
 Define and implement the constraint that if a project is not taken on then no one should be contracted to work on it.
-  **Task F**
Define and implement the project dependency constraints. 
- **Task G**
 Define and implement the constraint that the profit margin, i.e. the difference between the value of all delivered projects and the cost of all required subcontractors, is at least €2500. 
 - **Task H**
  Solve the CP-SAT model and determine how many possible solutions satisfy all the constraints . For each solution, determine what projects are taken on  which contractors work on which projects in which month , and what is the profit margin.
