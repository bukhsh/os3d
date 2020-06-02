
import datetime
import pandas as pd
import itertools
import math



def writedata(datfile,test):

    xl = pd.ExcelFile(test)

    df_staff      = xl.parse("Staff")
    df_desks      = xl.parse("Seating")
    df_days       = xl.parse("Days")
    df_coor       = xl.parse("Coordinates")
    df_allocation = xl.parse("Allocation")



    f = open(datfile, 'w')
    #####PRINT HEADER--START
    f.write('#This is Python generated data file for Pyomo model\n')
    f.write('#_author_:W. Bukhsh\n')
    f.write('#Time stamp: '+ str(datetime.datetime.now())+'\n')

    #---set of staff---
    f.write('set S:=\n')
    for i in df_staff["Staff"]:
        f.write(str(i)+"\n")
    f.write(';\n')

    #---set of seating---
    f.write('set K:=\n')
    for i in df_desks["Seating"]:
        f.write(str(i)+"\n")
    f.write(';\n')

    #---set of days---
    f.write('set D:=\n')
    for i in df_days["Day"]:
        f.write(str(i)+"\n")
    f.write(';\n')

    # ---set of pairs of desks---
    desk_list = df_desks["Seating"].tolist()

    f.write('set Kpairs:=\n')
    for pair in itertools.combinations(desk_list, 2):
        f.write(str(pair[0])+' '+str(pair[1])+'\n')
    f.write(';\n')



    # param for staff allocation
    if (df_allocation.Flexible.isin([0]).any().any()):
        f.write('set SK:=\n')
        for i in df_allocation.index:
            if df_allocation['Flexible'][i]==0:
                for k in df_desks["Seating"]:
                    if (k!=df_allocation["Seating"][i]):
                        f.write(str(df_allocation['Staff'][i])+' '+str(k)+' '+str(df_allocation['Days'][i])+"\n")
        f.write(';\n')

    # param for distances

    f.write('param DK:=\n')
    for pair in itertools.combinations(desk_list, 2):
        x1 = df_coor["x"][df_coor["Seating"]==pair[0]].item()
        x2 = df_coor["x"][df_coor["Seating"]==pair[1]].item()
        y1 = df_coor["y"][df_coor["Seating"]==pair[0]].item()
        y2 = df_coor["y"][df_coor["Seating"]==pair[1]].item()
        dist = math.sqrt((x1-x2)**2+(y1-y2)**2)
        f.write(str(pair[0])+' '+str(pair[1])+' '+str(dist)+'\n')
    f.write(';\n')
    f.close()



def writeoutput(instance,results,xlsfile):
    instance.solutions.load_from(results)

    allocation = pd.DataFrame(columns={'Staff','Desk','Day'})
    ind = 0
    for s in instance.S:
        for k in instance.K:
            for d in instance.D:
                if instance.u[s,k,d].value==1:
                    allocation.loc[ind] = pd.Series({'Staff':s,'Desk':k,'Day':d})
                    ind += 1
    allocation = allocation.sort_values(['Staff','Desk'])

    print allocation

    # writer = pd.ExcelWriter('results.xlsx', engine ='xlsxwriter')
    # summary.to_excel(writer, sheet_name = 'summary',index=False)
    # bus.to_excel(writer, sheet_name = 'bus',index=False)
    # demand.to_excel(writer, sheet_name = 'demand',index=False)
    # generation.to_excel(writer, sheet_name = 'generator',index=False)
    # wind.to_excel(writer, sheet_name = 'wind',index=False)
    # branch.to_excel(writer, sheet_name = 'branch',index=False)
    # transformer.to_excel(writer, sheet_name = 'transformer',index=False)
    # writer.save()
