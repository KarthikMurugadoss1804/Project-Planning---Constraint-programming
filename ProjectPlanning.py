# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 04:04:17 2020

@author: karth
"""
# Importing relevant packages

from ortools.sat.python import cp_model
import pandas as pd

# Reading Data from the files

projects_data = pd.read_excel("Assignment_DA_1_data.xlsx", sheet_name = "Projects", index_col=0)
projects = projects_data.index.tolist()
print(projects)
months = projects_data.columns.tolist()
print(months)
contractors_data = pd.read_excel("Assignment_DA_1_data.xlsx", sheet_name = "Quotes", index_col=0)
contractors = contractors_data.index.tolist()
print(contractors)
dependencies_data = pd.read_excel("Assignment_DA_1_data.xlsx", sheet_name = "Dependencies", index_col = 0 )
value_data = pd.read_excel("Assignment_DA_1_data.xlsx", sheet_name = "Value", index_col = 0 )
values = value_data['Value'].tolist()
print(values)
jobs = contractors_data.columns.tolist()
print(jobs)

# Initializing Solution Printer

class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    

    def __init__(self, projects_taken , contractors_project , t):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.projects_taken_ = projects_taken
        self.contractors_project_ = contractors_project
        self.profit_margin_ = t
        self.__solution_count = 0
        

    def on_solution_callback(self):
        self.__solution_count += 1
        print("Solution {}  Profit Margin: {}".format(self.__solution_count,self.Value(self.profit_margin_)))
        
        
        for p in range(len(projects)):
            if self.Value(self.projects_taken_[p]):
                print("{} is Taken".format(projects[p]))
                print("______________________\n")
            else: 
                print("{} not taken".format(projects[p]))
                print("______________________\n")
                
            for m in range(len(months)):
                for c in range(len(contractors)):
                    if self.Value(self.contractors_project_[(p,m,c)]):
                        print("{} , {} done by {}\n".format(months[m],projects_data.loc[projects[p]][months[m]], contractors[c]))
#                        solution_df.loc[projects[p]][months[m]] = contractors[c]
                        
#        
     
        print()

    def solution_count(self):
        return self.__solution_count

def main():
    model = cp_model.CpModel()
    
########################################### Task A ##########################################
    
    
    
########## Contractor Skill set ########################################### 
    #Creating a dictionary of contractor as key and jobs the contractor can do as values
    contractors_skill_set = {}
    for ind in contractors_data.index:
        skills = []
        for col in contractors_data.columns: 
            if pd.notnull(contractors_data.loc[ind][col]):
                skills.append(col)
        contractors_skill_set[ind] = skills
#    print(contractors_skill_set)
    
####################################### Task B #################################################    
        
        
    ########## Creating decision Variables  ###################################
    # (i) Decision Variable for deciding to take a project or not
    projects_taken = {}
    for p in range(len(projects)):
        projects_taken[p] = model.NewBoolVar("P{}".format(projects[p].split(" ")[1])) 
    
    
    # (ii) Decision Variable for deciding which contractor is working on which project and when
    #  Considered only if the Contractor is skilled to work on that particular job of the project 
    # Considered that all projects does not run on all months
    contractor_project = {}
    for p in range(len(projects)):
        for m in range(len(months)):
            for c in range(len(contractors)):
                #Creation of boolVar for every combination of project,month and contractor
                contractor_project[(p,m,c)] = model.NewBoolVar('p%i_m%i_c%i'%(p,m,c))
                #Adding the constraint that if the job is in the skill set of the contractor then the boolVar 
                # Can have True or False.
                if projects_data.loc[projects[p]][months[m]] in contractors_skill_set[contractors[c]]: 
                    model.Add(contractor_project[(p,m,c)] <=1)
                # Else the combination of the 
                else:
                    model.Add(contractor_project[(p,m,c)] == 0)
                    
                    
######################################## Task C ######################################################
                    
                    
    # Constraint that Contractor cannot work on two projects simultaneously
    
    for c in range(len(contractors)): 
        for m in range(len(months)):
            model.Add( sum( contractor_project[(p,m,c)] for p in range(len(projects)))  <=1 )
#            
######################################## Task D ######################################################
#   #Constraint : if a project is accepted to be delivered then exactly one contractor per job of the project needs to work on it         
    for p in range(len(projects)):
        for m in range(len(months)):
            if pd.notnull(projects_data.loc[projects[p]][months[m]]):
                model.Add( sum( contractor_project[(p,m,c)]  for c in range(len(contractors))) == 1 ).OnlyEnforceIf(projects_taken[p])
           
                
######################################### Task E  #####################################################
    #Constraint: If a project is not taken then none of the jobs should be taken by any contractor
    for p in range(len(projects)):
        for m in range(len(months)):
            model.Add(sum(contractor_project[(p,m,c)]  for c in range(len(contractors))) == 0 ).OnlyEnforceIf(projects_taken[p].Not())

    
#    ####################################  Task F #########################################################
#    creating project dependencies 
    project_dependency = {}    
    for project in projects:
        variables = {}
        for p2 in projects:
            variables[p2] = model.NewBoolVar(project+p2)
        project_dependency[project] = variables
        
    #  Setting the project dependency Constraints
    for i in range(len(projects)):
        for j in range(len(projects)):
            if dependencies_data[projects[i]][projects[j]] == "x":
                model.AddBoolAnd([project_dependency[projects[i]][projects[j]]])
                 
            else:
                model.AddBoolAnd([project_dependency[projects[i]][projects[j]].Not()])
    
    #  Adding Constraint that a particular project can be taken only if the dependency is satisfied
    
    for i in range(len(projects)):
       for j in range(len(projects)):
           model.AddBoolAnd([projects_taken[i]]).OnlyEnforceIf([project_dependency[projects[i]][projects[j]]])
    ##################################### Task G #########################
    
    #Calculating the total value of all the projects
    value_of_all_projects_delivered = []
    for i in range(len(projects)):
        value_of_all_projects_delivered.append(projects_taken[i]*values[i])
    
    total_value = sum(value_of_all_projects_delivered)
    #Calculating the cost involved for each solution
    cost = [] 
    for p in range(len(projects)):
        for c in range(len(contractors)):
            for m in range(len(months)):
                if pd.notnull(projects_data.loc[projects[p]][months[m]]):
                    job = str(projects_data.loc[projects[p]][months[m]])
                    if pd.notnull(contractors_data.loc[contractors[c]][job]) and projects_taken[p]:
                        cost.append(contractor_project[(p,m,c)]* int(contractors_data.loc[contractors[c]][job]))
    
    total_cost = sum(cost)
    
    # Adding the constraint that the profit margin should atleast be 2500
    profit_margin = total_value - total_cost
    model.Add(profit_margin >= 2500)
    # Creating a new variable to pass it to the solution printer
    t = model.NewIntVar(0,sum(values), 't')
    model.Add(t == profit_margin)    
    
    
    ################################## Task H #######################################################
                              #### Solution Printer ####
    
    solver = cp_model.CpSolver()
    
    solution_printer = SolutionPrinter(projects_taken, contractor_project, t)
    solver.SearchForAllSolutions(model, solution_printer)
    print('Number of solutions found: %i' %(solution_printer.solution_count()))
    
#   
    

main()