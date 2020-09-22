# Project Planning - Constraint programming

The aim of the project is to develop a constraint satisfaction problem model for project planning. 

## Files

1. ProjectPlanning.py
        Main python file where the problem is solved using Google Operations Research tools. 
2. DataFile.xlsx      
        Where all details about projects, contractor details, quotes, dependencies and value of projects.
        The file contains four sheets:
        
        In the **Projects sheet** you will find a list of projects, for each projects the jobs that
        need to be carried out and the months this needs to happen (e.g. Project E required
        Job J in month M8 and Job A in month M9).
        
        - In the **Quotes sheet** you will find a list of contractors and their quotes for each of the
        jobs they are qualified to carry out (e.g. Contractor A charges €230 for Job A). A
        contractor can only work in one project at a time.
        
        - In the **Dependencies sheet** you will find a matrix of project dependencies indicating
        which projects are pre-requisites for the delivery of other projects (e.g. Project B can
        only be taken on, if also Project A is taken on).
        
        - In the **Value sheet** you will find the value of each project (e.g. Project A is worth
        €500)
  

deciding what projects can be taken on and what companies need to be contracted to deliver on these projects.
