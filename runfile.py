# Run file
import pandas as pd
from write_data import writedata,writeoutput
from pyomo.environ import *
from pyomo.opt import SolverFactory
from pyomo.opt import SolverStatus, TerminationCondition
from models.scheduling import model



dat_file   = 'datafile.dat'
testcase   = 'Data/TIC-L4-Example.xlsx'
# testcase   = 'Data/example_small.xlsx'
outputfile = 'results.xlsx'

writedata(dat_file,testcase)
solver = 'cplex'


optimise = SolverFactory(solver)
instance = model.create_instance(dat_file)
instance.dual = Suffix(direction=Suffix.IMPORT)
results = optimise.solve(instance,tee=True)
writeoutput(instance, results,outputfile)

# # for s in instance.S:
# #     for k in instance.K:
# #         for d in instance.D:
#
# print sum(instance.u[s,k,d].value for (s,k,d) in instance.S*instance.K*instance.D)/((sum(1 for s in instance.S)*sum(1 for d in instance.D)))*100
#
# # for (k1,k2) in instance.Kpairs:
# #     print (k1,k2, instance.indicator[k1,k2].value)
# #
# # for s in instance.S:
# #     for k in instance.K:
# #         for d in instance.D:
# #             print (s,k,d,instance.u[s,k,d].value)
# #
# #
# # for (k1,k2) in instance.Kpairs:
# #     for d in instance.D:
# #         print k1,k2,d, sum(instance.u[s,k1,d].value+instance.u[s,k2,d].value for s in instance.S)
