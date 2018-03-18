# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 20:49:10 2018

@author: Will Kew
will.kew@gmail.com
"""

import pandas as pd

path = "F:/Will/Dropbox/Documents/University/Edinburgh/FTICRMS/MixedIonisation3-formularity/"
#path = "C:/Users/Will/Dropbox/Documents/University/Edinburgh/FTICRMS/MixedIonisation3-formularity/"
inputdata = path+"Assignments/"
#outputdata = path +"ReformAssignments/"


deproton = "Report-Deprotonated.csv"
radical = "Report-Radicals.csv"

df_depro = pd.read_csv(inputdata+deproton)
df_radical= pd.read_csv(inputdata+radical)

df_depro_assign = df_depro[df_depro['Class']!="None"].copy()
df_radical_assign = df_radical[df_radical['Class']!="None"].copy()
df_depro_assign['State'] = "H-"
df_radical_assign['State'] = ".-"

columns = list(df_depro_assign.columns)
columns = columns[:14]+[columns[-1]]+columns[14:-1]

df_assign = pd.concat([df_depro_assign,df_radical_assign])
df_assign = df_assign[columns]

df_unassign = df_depro.copy()
df_unassign = df_unassign.drop(df_assign['Mass'].index)


df = pd.concat([df_assign,df_unassign])
df = df[columns]
df = df.sort_values('Mass')

df.to_csv(inputdata+"Assignments.csv")
