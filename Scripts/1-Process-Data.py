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

def dividor(X,Y):
    if Y == 0:
        return None
    else:
        return (X/Y)

path = "F:/Will/Dropbox/Documents/University/Edinburgh/FTICRMS/MixedIonisation3-formularity/"
#path = "C:/Users/Will/Dropbox/Documents/University/Edinburgh/FTICRMS/MixedIonisation3-formularity/"

inputdata = path+"Assignments/"
outputdata = path +"ReformAssignments/"
file = "Assignments.csv"

df = pd.read_csv(inputdata+file,index_col=0)

nsamples = len(df.T)-15 # how many samples are in this dataframe? 
samplenames = df.columns[15:].values.tolist() # Get the file names from the headers of the dataframe

"""
# This determines if the data is positive or negative mode, and if positive, adducts of assignment.
if file[:3] == "Neg":
    polarity = "neg"
    adduct = False
elif file[-6] == "-":
    polarity = "pos"
    if file[-5] == "H":
        adduct = False
    elif file[-5] == "K":
        adduct = 'K'
else:
    adduct = 'Na'
    polarity = "pos"
"""
polarity = "Neg"
df_mono = df[(df['Class']!="None") & (df['C13']==0)].copy() #avoid set with copy warning
df_iso = df[(df['Class']!="None") & (df['C13']!=0)].copy() #avoid set with copy warning      

# This adds a column containing the formulas
df_mono.loc[:,"Formula"] = df_mono.apply(lambda row: formulator(row['C'],row['H'],row['O']),axis=1)

#adds heteroatomic classes
df_mono.loc[:,"HeteroClass"] = df_mono.apply(lambda row: hetclasser(row['C'],row['H'],row['O']),axis=1)

totalpeaks = len(df) #how many peaks in dataframe
totalmonoassignments = len(df_mono) # how many monoisotopic hits in the dataframe
totalisoassignments = len(df_mono) # how many isotopologue hits in the dataframe
totalassignments = len(df_iso)+len(df_mono) #how many assigned in dataframe

#Generate a new dataframe for our statistics output
statscols = ["Polarity","Ionisation Source", "Sample","Total Peaks","Monoisotopic Hits","Isotopic Hits",
             "Unassigned","Percent Assigned","Percent Monoisotopic Assigned","Mean Error (ppm)","Std Error",
             "Deprotonated","Radicals","Monoisotopic Deprotonated","Monoisotopic Radicals"]

df_statistics = pd.DataFrame(index=samplenames,columns=statscols)

# This section computes statistics for assignments for each sample. 
for samplename in samplenames:
    
    df_new = df.copy() #create a new dataframe copy of our data to modify
    samplestopdrop = samplenames[:]
    samplestopdrop.remove(samplename)
    df_new.drop(samplestopdrop,axis=1,inplace=True) # remove other samples from this dataframe
    
    df_new = df_new[df_new[samplename]!=0] # This drops rows with 0 intensity for a peak - i.e. peaks not found in this sample.

    #add formula and heteroatomic classes
    df_new.loc[:,"Formula"] = df_new.apply(lambda row: formulator(row['C'],row['H'],row['O']),axis=1)
    df_new.loc[:,"HeteroClass"] = df_new.apply(lambda row: hetclasser(row['C'],row['H'],row['O']),axis=1)
    df_new.loc[:,"OC"] = df_new.apply(lambda row: dividor(row['O'],row['C']),axis=1)
    df_new.loc[:,"HC"] = df_new.apply(lambda row: dividor(row['H'],row['C']),axis=1)
    df_new.loc[:,"AImod"] = df_new.apply(lambda row: AIcalc(row['C'],row['H'],0,row['O'],0,0),axis=1) #CHNOSP and optional bool 'mod' switch
    df_new.loc[:,"DBE"] = df_new.apply(lambda row: DBEcalc(row['C'],row['H'],0),axis=1) #CHN and optional int X switch.

    df_statistics.loc[samplename,"Polarity"] = polarity
    df_statistics.loc[samplename,"Ionisation Source"] = samplename[:-13]
    df_statistics.loc[samplename,"Sample"] = samplename[-8:]

    df_statistics.loc[samplename,"Total Peaks"] = len(df_new)
    df_statistics.loc[samplename,"Monoisotopic Hits"] = len(df_new[(df_new['Class']!="None") & (df_new['C13']==0)])
    df_statistics.loc[samplename,"Isotopic Hits"] = len(df_new[(df_new['Class']!="None") & (df_new['C13']!=0)])
    df_statistics.loc[samplename,"Unassigned"] = len(df_new[(df_new['Class']=="None")])
    df_statistics.loc[samplename,"Percent Assigned"] = (len(df_new)-len(df_new[(df_new['Class']=="None")]))/ len(df_new)
    df_statistics.loc[samplename,"Percent Monoisotopic Assigned"] = len(df_new[(df_new['Class']!="None") & (df_new['C13']==0)]) / len(df_new)
    df_statistics.loc[samplename,"Mean Error (ppm)"] = df_new[(df_new['Class']!="None")]['Error_ppm'].abs().mean()
    df_statistics.loc[samplename,"Std Error"] = df_new[(df_new['Class']!="None")]['Error_ppm'].abs().std()
    
    
    df_statistics.loc[samplename,"Deprotonated"] = len(df_new[(df_new['State']=="H-")])
    df_statistics.loc[samplename,"Radicals"] = len(df_new[(df_new['State']==".-")])
    df_statistics.loc[samplename,"Monoisotopic Deprotonated"] = len(df_new[(df_new['State']=="H-") & (df_new['C13']==0)])
    df_statistics.loc[samplename,"Monoisotopic Radicals"] = len(df_new[(df_new['State']==".-") & (df_new['C13']==0)])
    #df_statistics.loc[samplename,"Percent Deprotonated"] = len(df_new[(df_new['State']=="H-")])/len(df_new)
    #df_statistics.loc[samplename,"Percent Radicals"] = len(df_new[(df_new['State']==".-")])/len(df_new[(df_new['Class']!="None") & (df_new['C13']==0)])

    writer = pd.ExcelWriter(outputdata+samplename+'.xlsx')
    df_new.to_excel(writer,'All Peaks')
    df_new_nohits = df_new[df_new['C']==0].copy() # This filters to leave only isotopic hits
    df_new_iso = df_new[df_new['C13']!=0].copy() # This filters to leave only isotopic hits
    df_new = df_new[(df_new['C']!=0) & (df['C13']==0)] # This filters to leave only monoisotopic hits
    df_new.to_excel(writer,'Hits')
    df_new_iso.to_excel(writer,'Isotopic Hits')
    df_new_nohits.to_excel(writer,'Unassigned')
    writer.save()
 
writer = pd.ExcelWriter(outputdata+"HitStatistics-Negative.xlsx") 
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
#worksheet.set_column('O:O', 29, percent_fmt)
#worksheet.set_column('P:P', 29, percent_fmt)
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
