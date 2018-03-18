# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 16:16:10 2018

@author: s1457548
"""

import pandas as pd
#import seaborn as sns

#This creates a string Formula for us
def formulator(C,H,O):
    if C == 0:
        return None
    formula = "C"+str(C)+"H"+str(H)
    if O > 0:
        formula = formula+"O"+str(O)
    return formula

#This calculates the heteroatomic class
def hetclasser(C,H,O):
    if C == 0:
        return None
    if O>0:
        hetclass = "O"+str(O)
    else:
        hetclass = "CH"
    return hetclass

# Aromaticity Index calculation. Unlike DBE, this factors in O and S. Taken from DOI: 10.1002/rcm.2386
# Added switch for using the "modified" aromaticity index instead of the normal one. This halves #O on basis/assumption only half will be pi-bound. 
def AIcalc(C,H,N,O,S,P,mod=True):
    if C == 0:
        return None
    if mod==True:
        O = O/2
    top = 1+C-O-S-(0.5*H)
    btm = C-O-S-N-P
    if btm == 0:
        AI = 0
    else:
        AI = top/btm
    if AI < 0:
        AI = 0
    return AI

# Calculates DBE
def DBEcalc(C,H,N,X=0):
    if C == 0:
        return None
    DBE = (C+1-(H/2)-(X/2)+(N/2))
    return DBE

#divides without a division by zero error
def dividor(X,Y):
    if Y == 0:
        return None
    else:
        return (X/Y)

#counts number of 0s within a row (of 4)    
def countnonzeros(data):
    if 0 in data.value_counts():
        return 4 - data.value_counts()[0]
    else:
        return 4

path = "F:/Will/Dropbox/Documents/University/Edinburgh/FTICRMS/MixedIonisation3-formularity/"
#path = "C:/Users/Will/Dropbox/Documents/University/Edinburgh/FTICRMS/MixedIonisation3-formularity/"

inputdata = path+"Assignments/"
outputdata = path +"GroupedAssignments/"
file = "Assignments.csv"
polarity = "Neg"
ionisationsources = ["APCI","APPI","LDI","ESI"]

df = pd.read_csv(inputdata+file,index_col=0)


nsamples = len(df.T)-15 # how many samples are in this dataframe? 
samplenames = df.columns[15:].values.tolist() # Get the file names from the headers of the dataframe

# This section computes statistics for assignments for each sample. 
for source in ionisationsources:
    samplestopdrop = [x for x in samplenames if not source in x]
    samplename = [x for x in samplenames if source in x]
    df_new = df.copy() #create a new dataframe copy of our data to modify
    df_new.drop(samplestopdrop,axis=1,inplace=True) # remove other samples from this dataframe
    
    #this sums the intensities of our ionisation sources - i.e. making one column to check if peaks found in these samples
    df_new.loc[:,"SumInt"] = df_new.apply(lambda row: (row[-4:].sum()),axis=1)
    df_new = df_new[df_new["SumInt"]!=0] #remove rows where peaks werent found in given samples. 
    df_new.loc[:,"TimesFound"] = df_new.apply(lambda row: countnonzeros(row[-4:]),axis=1)

    #add formula and heteroatomic classes
    df_new.loc[:,"Formula"] = df_new.apply(lambda row: formulator(row['C'],row['H'],row['O']),axis=1)
    df_new.loc[:,"HeteroClass"] = df_new.apply(lambda row: hetclasser(row['C'],row['H'],row['O']),axis=1)
    df_new.loc[:,"OC"] = df_new.apply(lambda row: dividor(row['O'],row['C']),axis=1)
    df_new.loc[:,"HC"] = df_new.apply(lambda row: dividor(row['H'],row['C']),axis=1)
    df_new.loc[:,"AImod"] = df_new.apply(lambda row: AIcalc(row['C'],row['H'],0,row['O'],0,0),axis=1) #CHNOSP and optional bool 'mod' switch
    df_new.loc[:,"DBE"] = df_new.apply(lambda row: DBEcalc(row['C'],row['H'],0),axis=1) #CHN and optional int X switch.
    
    writer = pd.ExcelWriter(outputdata+source+"-"+polarity+'.xlsx')
    df_new.to_excel(writer,'All Peaks')
    df_new_nohits = df_new[df_new['C']==0].copy() # This filters to leave only isotopic hits
    df_new_iso = df_new[df_new['C13']!=0].copy() # This filters to leave only isotopic hits
    df_new = df_new[(df_new['C']!=0) & (df['C13']==0)] # This filters to leave only monoisotopic hits
    df_new.to_excel(writer,'Hits')
    df_new_iso.to_excel(writer,'Isotopic Hits')
    df_new_nohits.to_excel(writer,'Unassigned')
    writer.save()
    
"""
#Generate a new dataframe for our statistics output
statscols = ["Polarity","Ionisation Source", "Sample","Total Peaks","Monoisotopic Hits","Isotopic Hits",
             "Unassigned","Percent Assigned","Percent Monoisotopic Assigned","Mean Error (ppm)","Std Error",
             "Deprotonated","Radicals","Monoisotopic Deprotonated","Monoisotopic Radicals"]
df_statistics = pd.DataFrame(index=samplenames,columns=statscols)

for sample in samplenames:
    samplestopdrop = [x for x in samplenames if not sample in x]
    #samplename = [x for x in samplenames if source in x]
    df_new = df.copy() #create a new dataframe copy of our data to modify
    df_new.drop(samplestopdrop,axis=1,inplace=True) # remove other samples from this dataframe
    df_new = df_new[df_new[sample]!=0]
    df_statistics.loc[sample,"Polarity"] = polarity
    df_statistics.loc[sample,"Ionisation Source"] = sample[:-13]
    df_statistics.loc[sample,"Sample"] = sample[-8:]

    df_statistics.loc[sample,"Total Peaks"] = len(df_new)
    df_statistics.loc[sample,"Monoisotopic Hits"] = len(df_new[(df_new['Class']!="None") & (df_new['C13']==0)])
    df_statistics.loc[sample,"Isotopic Hits"] = len(df_new[(df_new['Class']!="None") & (df_new['C13']!=0)])
    df_statistics.loc[sample,"Unassigned"] = len(df_new[(df_new['Class']=="None")])
    df_statistics.loc[sample,"Percent Assigned"] = (len(df_new)-len(df_new[(df_new['Class']=="None")]))/ len(df_new)
    df_statistics.loc[sample,"Percent Monoisotopic Assigned"] = len(df_new[(df_new['Class']!="None") & (df_new['C13']==0)]) / len(df_new)
    df_statistics.loc[sample,"Mean Error (ppm)"] = df_new[(df_new['Class']!="None")]['Error_ppm'].abs().mean()
    df_statistics.loc[sample,"Std Error"] = df_new[(df_new['Class']!="None")]['Error_ppm'].abs().std()
    df_statistics.loc[samplename,"Deprotonated"] = len(df_new[(df_new['State']=="H-")])
    df_statistics.loc[samplename,"Radicals"] = len(df_new[(df_new['State']==".-")])
    df_statistics.loc[samplename,"Monoisotopic Deprotonated"] = len(df_new[(df_new['State']=="H-") & (df_new['C13']==0)])
    df_statistics.loc[samplename,"Monoisotopic Radicals"] = len(df_new[(df_new['State']==".-") & (df_new['C13']==0)])
    
    
writer = pd.ExcelWriter(path+"Hit Statistics/"+"HitStatistics.xlsx") 
df_statistics.to_excel(writer,"Statistics")
# Get access to the workbook and sheet
workbook = writer.book
worksheet = writer.sheets['Statistics']
# Add a percent format with 1 decimal point
percent_fmt = workbook.add_format({'num_format': '0.0%', 'bold': False})
float_fmt = workbook.add_format({'num_format': '0.000', 'bold': False})

# Quota percent columns
worksheet.set_column('I:I', 16, percent_fmt)
worksheet.set_column('J:J', 29, percent_fmt)
#fix column widths
worksheet.set_column('A:A', 20)
worksheet.set_column('C:C', 17)
worksheet.set_column('E:E', 10)
worksheet.set_column('F:F', 17)
worksheet.set_column('G:G', 12)
worksheet.set_column('H:H', 10)
worksheet.set_column('K:K', 16,float_fmt)
worksheet.set_column('L:L', 10,float_fmt)

writer.save()
"""
