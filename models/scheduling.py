#==================================================================
# scheduling.py
# PYOMO model file for a scheduling model
# ---Author---
# W. Bukhsh,
# wbukhsh@gmail.com
#==========Import==========
from __future__ import division
from pyomo.environ import *
#==========================

model = AbstractModel()
# --- sets ---
model.S      = Set()  # set of staff
model.K      = Set()  # set of seating
model.D      = Set()  # set of days
model.Kpairs = Set(within=model.K*model.K)  # set of pairs of desks

# --- parameters ---
model.SK = Set(within=model.S*model.K*model.D)  #staff seating allocation
# line matrix
model.DK = Param(model.Kpairs)       # distance between seats

# --- variables ---
model.u         = Var(model.S*model.K*model.D, within=Binary)# binary variable for allocation
model.indicator = Var(model.Kpairs,within=Binary)

# --- cost function ---
def objective(model):
    obj = sum(model.u[s,k,d] for (s,k,d) in model.S*model.K*model.D)
    return obj
model.OBJ = Objective(rule=objective, sense=maximize)

# --- seating constraint: only one desk for a staff member ---
def one_staffperseat(model,s,d):
    return sum(model.u[s,k,d] for k in model.K)<=1
model.SeatingConst1 = Constraint(model.S,model.D, rule=one_staffperseat)

# --- seating constraint: one staff member per desk ---
def one_staffperseat(model,k,d):
    return sum(model.u[s,k,d] for s in model.S)<=1
model.SeatingConst = Constraint(model.K,model.D, rule=one_staffperseat)

# ---social distance constraint ---
def SocialDistancingConst(model,k1,k2,d):
    return model.indicator[k1,k2]*model.DK[k1,k2]+(1-model.indicator[k1,k2])*10000>=4
model.SocialDistancing = Constraint(model.Kpairs,model.D, rule=SocialDistancingConst)

# ---indicator variable constraint ---
def indicator_variable(model,k1,k2,d):
    return sum(model.u[s,k1,d]+model.u[s,k2,d] for s in model.S)-1 <= model.indicator[k1,k2]
model.IndicatorVarConstraint = Constraint(model.Kpairs,model.D,rule=indicator_variable)

# ---Fix seating---
def fix_seating(model,s,k,d):
    return model.u[s,k,d]==0
model.FixSeatingConst = Constraint(model.SK,rule=fix_seating)

# ---constraints on number of days---
def staff_min_attendence(model,s):
    return sum(model.u[s,k,d] for (k,d) in model.K*model.D) >=2
# model.FixSeatingConst = Constraint(model.S,rule=staff_min_attendence)
