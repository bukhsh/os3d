# Optimal staff scheduling with social distancing constraints (os3d)



## Introduction

It is likely that for most of us the return to work will be gradual with a degree of social distancing in effect. I have been looking at how mathematical modelling can help us plan, design and operate better workplaces while adhering to the social distancing guidelines from the government.

I have build an optimisation model that maximises the occupancy of a building subject to a social distancing constraint. (x,y) coordinates of a seating plan are required as an input to the model. The model calculates the distances between the staff and provides an optimal schedule for a given time horizon (e.g a day, a week or a month). I have tested this model in an office space where I am based [(TIC-Level 4)](figures/TIC-L4.jpg). With 2 m social distancing, the optimal occupancy is approximately 34% and [here](figures/TIC-L4-solution.jpg) is what a solution looks like. See a graph [here](figures/OptimalOccupancy.png) for a relationship between occupancy and social distancing parameter.

I have provided a high-level view of the optimisation in a section below. Please refer to my lecture [(here)](https://drive.google.com/file/d/0Bzq9B9vW0gM0M1JkNnhYSHA2Rnc/view?usp=sharing) for mathematical details of some standard scheduling problems. I found that implementing a social distancing constraint is a real pain in a sceduling algorithm. I'm glad it worked out well in the end. Please get in touch if you have any ideas regarding the use of this model or if you'd like to collaborate on extending this model for a specific application (see the sections on 'extensions' and 'other ideas' below)

The model can be used to answer the following questions:

* Scheduling staff for a given number of days (i.e. weekly/monthly)

* Scheduling staff with flexible working hours

* Identifying the problem areas in the seating plan

* Dependence of the social distancing parameter on occupancy level


* Can 'hot desking' increase occupancy? The answer to this questions is yes. But only if the staff is willing to stagger their working hours or willing to work particular days (e.g. 2 days a week). If the staff is not flexible, then hot desking does not help with occupancy. With hot desking cleaning regime would need to be improved.

## Dependencies
This model has following two dependencies:

* Python based modelling language - PYOMO
* A mixed integer programming solver (e.g. CPLEX, gurobi)


## Optimisation model

This is a scheduling algorithm with a set of social distancing constraints. The resulting model is a mixed-integer linear programming (MILP) problem.



<a href="https://www.codecogs.com/eqnedit.php?latex=u_{s,k,d}=\left\{\begin{matrix}&space;1&space;&&space;\text{if&space;staff&space;`s'&space;occupies&space;desk&space;`k'&space;on&space;day&space;`d'}&space;&&space;\\&space;0&\text{otherwise}&space;&&space;\end{matrix}\right." target="_blank"><img src="https://latex.codecogs.com/gif.latex?u_{s,k,d}=\left\{\begin{matrix}&space;1&space;&&space;\text{if&space;staff&space;`s'&space;occupies&space;desk&space;`k'&space;on&space;day&space;`d'}&space;&&space;\\&space;0&\text{otherwise}&space;&&space;\end{matrix}\right." title="u_{s,k,d}=\left\{\begin{matrix} 1 & \text{if staff `s' occupies desk `k' on day `d'} & \\ 0&\text{otherwise} & \end{matrix}\right." /></a>



I am not going to go into too much mathematical detail but please feel free to get in touch if you have any questions. The mathematical model is implemented in an algebraic modelling language called PYOMO.

## Inputs and Outputs
The input to the model is via Excel spreadsheet. See 'cases' folder for an example of the data. The user is expected to input the coordinates of the seating arrangement. The model will calculate the distances between the staff members. The social distancing constraint will ensure that the desks which are less than a given social distancing parameters are not occupied at the same time.

The optimal schedule is written on a spreadsheet 'results.xlsx'.


## How this model can be used?
This model can be used for planning the staff members that can safely be accommodated in a building on a given day. The look-ahead (weekly/monthly) feature of this model enables the decision-makers to make an informed judgement about scheduling overtime.

There are two important parameters in this model that can be tuned to quantify the impact of different policies. These parameters are the social distancing (&rho;) and hot-desking (Flex).


&rho; (meters): social distancing parameter

Flex<sub>s,l</sub> (0 or 1): Flex is a parameter that assigns a staff member to a particular desk. If all flex parameters are equal to 1, that models the hot-desking and the model decides where a staff member would sit on a particular day.


## Extensions

### Flexible working hours
The scheduling time-horizon of the model here is over days. However, it is possible to scheduling staff over hourly time-periods with a fix working-hours window. This will model the situation where working hours could be staggered to optimise the number of staff at any given time.


### Herd immunity constraints

Currently, there is no evidence on herd-immunity of Covid-19. However, the government is planning to introduce immunity certificates. In the current version of the model, the social distancing constraint applies to all staff members. However, it is possible to partition the set of staff into two subsets: immune and not-immune.



## Other ideas

### Space optimisation
Some workplaces may be able to rearrange their seating to optimise occupancy. How can we model space optimisation with the social distancing constraints? I'd do a 2-stage optimisation model in which the 1st stage is to model the space optimisation and that remains fixed for the 2nd stage that models the daily/hourly staff scheduling. There may be a better way of doing this.

### Use of office facilities
I am interested in an online web-based solution that provides the staff with an allocated time for using facilities. For example, when a staff member needs to use the kitchen (or rest-room) they go and log in their request, the online system allocates the facility which is least busy or a time window when they can use the facility. Similarly, when they need to enter or exit the building, a route of minimal traffic. Such a solution needs a live feed of sensor-data - very doable but needs time and effort.
