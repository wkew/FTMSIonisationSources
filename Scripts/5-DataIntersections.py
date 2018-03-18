# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 23:09:59 2017

@author: Will Kew
will.kew@gmail.com
"""


import pyupset as pyu
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import ticker
from matplotlib import cm
import seaborn as sns




path = "F:/Will/Dropbox/Documents/University/Edinburgh/FTICRMS/MixedIonisation3-formularity/"
#path = "C:/Users/Will/Dropbox/Documents/University/Edinburgh/FTICRMS/MixedIonisation3-formularity/"

outputdata = path+"Images/UpSets/"

df = pd.read_excel(path+"AllHits-Longform.xlsx",sheet_name="Sheet1")


staticolumns = ['C','H','O','OC','HC','Mass','DBE','AImod']
df2 = df.rename(columns={'id':'Count'}).groupby(['Polarity','Mode','Formula'],as_index=False)['Count'].count()
df2['Abundance'] = df.groupby(['Polarity','Mode','Formula'],as_index=False)['Abundance'].median()['Abundance']
df2['HeteroClass'] = df.groupby(['Polarity','Mode','Formula'],as_index=False)['HeteroClass'].first()['HeteroClass']
df2[staticolumns] = df.groupby(['Polarity','Mode','Formula'],as_index=False)[staticolumns].mean()[staticolumns]


writer = pd.ExcelWriter(path+'AllHits-Longform-SampleHitCounts.xlsx')
df2.to_excel(writer,"Data")
df3 = df2[df2['Count']>1]
df3.to_excel(writer,"More than 1")
df3 = df2[df2['Count']>2]
df3.to_excel(writer,"More than 2")
df3 = df2[df2['Count']>3]
df3.to_excel(writer,"More than 3")
writer.save()


modes = ["APCI","APPI","ESI","LDI"]

######## Negative ##########
df_dict_neg = {'APPI':df2[(df2['Polarity']=='Neg') & (df2['Mode']=='APPI')],
               'APCI':df2[(df2['Polarity']=='Neg') & (df2['Mode']=='APCI')],
               'ESI':df2[(df2['Polarity']=='Neg') & (df2['Mode']=='ESI')],
               'LDI':df2[(df2['Polarity']=='Neg') & (df2['Mode']=='LDI')]}

upset = pyu.plot(df_dict_neg,unique_keys=['Formula'],sort_by='degree')

plt.savefig(outputdata+"UpSetNeg.png",dpi=300)

intsets = upset['intersection_sets']
intsetkeys = []
for y in intsets:
    intsetkeys.append(y)

def plotcommontoall():
    df_common = intsets[intsetkeys[-1]]
    df_common = df_common.sort_values('Mass')
    glocmap = cm.viridis_r

    sns.set_style("white")
    sns.set_context("paper",font_scale=2)
    glocmap = cm.viridis_r

    scalefactor = (df_common['Abundance'].mean()/(df_common['Abundance'].sum()*len(df_common)))*2
    labelsize = 20
    xlim = (0,1.2)
    ylim = (0,2)
    clim=(0,800)
    fig, ax = plt.subplots(figsize=(8,6))
    im = ax.scatter(x=df_common['OC'], y=df_common['HC'],cmap=glocmap,c=df_common['Mass'],
               s=df_common['Abundance']*scalefactor,alpha=0.75,label='Common')


    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_xlabel("O/C",fontdict={'fontsize':labelsize})
    ax.set_ylabel("H/C",fontdict={'fontsize':labelsize})
    ax.tick_params(axis="both",which="major",left="on",bottom="on",top="off",right="off",labelsize=labelsize)
    ax.tick_params(axis="both",which="minor",left="on",bottom="on",top="off",right="off")
    ax.xaxis.set_major_locator(ticker.MaxNLocator(3))
    ax.yaxis.set_major_locator(ticker.MaxNLocator(3))
    ax.xaxis.set_tick_params(which='both', direction='out',width=1.25,length=8)
    ax.yaxis.set_tick_params(which='both', direction='out',width=1.25,length=8)
    color_bar = fig.colorbar(im, alpha=1)
    color_bar.set_label("Mass",size=labelsize)
    color_bar.set_alpha(1)
    color_bar.set_clim(clim)
    color_bar.draw_all()
    plt.tight_layout()
    plt.savefig(outputdata+"CommonToAll-VK.png",dpi=300) #saves the PNG (raster) at high DPI
    plt.show()


"""
df_pairwise = pd.DataFrame(index=modes,columns=["Neg","Pos","Common","Total","% Common"])
for x in modes:
    negform = df2[(df2['Polarity']=="Neg")&(df2['Mode']==x)]['Formula']
    posform = df2[(df2['Polarity']=="Pos")&(df2['Mode']==x)]['Formula']
    total = list(set(negform) | set(posform))
    uniquetoneg = list(set(negform) - set(posform))
    uniquetopos = list(set(posform) - set(negform))
    common = list(set(negform) & set(posform))

    df_pairwise.loc[x,"Neg"]=len(uniquetoneg)
    df_pairwise.loc[x,"Pos"]=len(uniquetopos)
    df_pairwise.loc[x,"Common"]=len(common)
    df_pairwise.loc[x,"Total"]=len(uniquetoneg)+len(uniquetopos)+len(common)
    df_pairwise.loc[x,"% Common"]=len(common)/(len(uniquetoneg)+len(uniquetopos)+len(common))

negform = df2[(df2['Polarity']=="Neg")]['Formula']
posform = df2[(df2['Polarity']=="Pos")]['Formula']
total = list(set(negform) | set(posform))
uniquetoneg = list(set(negform) - set(posform))
uniquetopos = list(set(posform) - set(negform))
common = list(set(negform) & set(posform))

df_pairwise.loc["Overall","Neg"]=len(uniquetoneg)
df_pairwise.loc["Overall","Pos"]=len(uniquetopos)
df_pairwise.loc["Overall","Common"]=len(common)
df_pairwise.loc["Overall","Total"]=len(uniquetoneg)+len(uniquetopos)+len(common)
df_pairwise.loc["Overall","% Common"]=len(common)/(len(uniquetoneg)+len(uniquetopos)+len(common))

df_pairwise.to_excel(path+"PairwiseIntersections.xlsx")
"""
""" ### THIS BLOCK DID CALCULATIONS OF INTERSECTIONS USING UPSET PACKAGE ####
##### PAIRWISE & Overall #####
df_pairwise = pd.DataFrame(index=modes,columns=["neg","pos","common"])
for x in modes:
    df_dict_pairwise = {x+' (+)':df2[(df2['Polarity']=='Pos') & (df2['Mode']==x)],
                        x+' (-)':df2[(df2['Polarity']=='Neg') & (df2['Mode']==x)]}


    upset = pyu.plot(df_dict_pairwise,unique_keys=['Formula'])
    intsets = upset['intersection_sets']
    intsetkeys = []
    for y in intsets:
        intsetkeys.append(y)
    df_pairwise["pos"][x] = len(intsets[intsetkeys[0]])
    df_pairwise["neg"][x] = len(intsets[intsetkeys[1]])
    df_pairwise["common"][x] = len(intsets[intsetkeys[2]])

df_pairwise.to_excel(path+"PairwiseIntersections.xlsx")

#plt.savefig(path+"UpSet.png",dpi=300)



######## POLARITY ##########
df_dict_polarities = {'Pos':df2[(df2['Polarity']=='Pos')].drop_duplicates(subset='Formula'),
               'Neg':df2[(df2['Polarity']=='Neg')].drop_duplicates(subset='Formula')}

upset = pyu.plot(df_dict_polarities,unique_keys=['Formula'],sort_by='degree')
plt.savefig(outputdata+"UpSetPolarity.png",dpi=300)


### END PAIRWISE BIT ####
"""


"""
######## Positive ##########
df_dict_pos = {'APPI':df2[(df2['Polarity']=='Pos') & (df2['Mode']=='APPI')],
               'APCI':df2[(df2['Polarity']=='Pos') & (df2['Mode']=='APCI')],
               'ESI':df2[(df2['Polarity']=='Pos') & (df2['Mode']=='ESI')],
               'LDI':df2[(df2['Polarity']=='Pos') & (df2['Mode']=='LDI')]}

upset = pyu.plot(df_dict_pos,unique_keys=['Formula'],sort_by='degree')

plt.savefig(outputdata+"UpSetPos.png",dpi=300)
"""
"""
### Both Polarities ####

df_dict_both = {'APPI (+)':df2[(df2['Polarity']=='Pos') & (df2['Mode']=='APPI')],
               #'APCI (+)':df2[(df2['Polarity']=='Pos') & (df2['Mode']=='APCI')],
               #'ESI (+)':df2[(df2['Polarity']=='Pos') & (df2['Mode']=='ESI')],
               'LDI (+)':df2[(df2['Polarity']=='Pos') & (df2['Mode']=='LDI')],
               'APPI (-)':df2[(df2['Polarity']=='Neg') & (df2['Mode']=='APPI')],
               #'APCI (-)':df2[(df2['Polarity']=='Neg') & (df2['Mode']=='APCI')],
               #'ESI (-)':df2[(df2['Polarity']=='Neg') & (df2['Mode']=='ESI')],
               'LDI (-)':df2[(df2['Polarity']=='Neg') & (df2['Mode']=='LDI')]}

upset = pyu.plot(df_dict_both,unique_keys=['Formula'],sort_by='degree')

"""



"""

staticolumns = ['C','H','O','OC','HC','Mass','DBE','AImod']
df3 = df.rename(columns={'id':'Count'}).groupby(['Polarity','Sample','Formula'],as_index=False)['Count'].count()
df3['Abundance'] = df.groupby(['Polarity','Sample','Formula'],as_index=False)['Abundance'].sum()['Abundance']
df3['HeteroClass'] = df.groupby(['Polarity','Sample','Formula'],as_index=False)['HeteroClass'].first()['HeteroClass']
df3[staticolumns] = df.groupby(['Polarity','Sample','Formula'],as_index=False)[staticolumns].mean()[staticolumns]

######## SAMPLE NEG ##########
df_dict_samples_neg = {'S14-1941':df3[(df2['Polarity']=='Neg') & (df3['Sample']=='S14-1941')],
               'S14-1944':df3[(df3['Polarity']=='Neg') & (df3['Sample']=='S14-1944')],
               'S14-1962':df3[(df3['Polarity']=='Neg') & (df3['Sample']=='S14-1962')],
               'S14-2196':df3[(df3['Polarity']=='Neg') & (df3['Sample']=='S14-2196')]}

upset = pyu.plot(df_dict_samples_neg,unique_keys=['Formula'],sort_by='degree')
#fig = upset.get('figure')
#ax = fig.get_axes()
plt.savefig(outputdata+"UpSetNegSamples.png",dpi=300)

######## SAMPLE POS ##########
df_dict_samples_pos= {'S14-1941':df3[(df2['Polarity']=='Pos') & (df3['Sample']=='S14-1941')],
               'S14-1944':df3[(df3['Polarity']=='Pos') & (df3['Sample']=='S14-1944')],
               'S14-1962':df3[(df3['Polarity']=='Pos') & (df3['Sample']=='S14-1962')],
               'S14-2196':df3[(df3['Polarity']=='Pos') & (df3['Sample']=='S14-2196')]}

upset = pyu.plot(df_dict_samples_pos,unique_keys=['Formula'],sort_by='degree')
#fig = upset.get('figure')
#ax = fig.get_axes()
plt.savefig(outputdata+"UpSetPosSamples.png",dpi=300)


######## SAMPLE Both ##########
df_dict_samples= {'S14-1941':df3[(df3['Sample']=='S14-1941')],
               'S14-1944':df3[(df3['Sample']=='S14-1944')],
               'S14-1962':df3[(df3['Sample']=='S14-1962')],
               'S14-2196':df3[(df3['Sample']=='S14-2196')]}

upset = pyu.plot(df_dict_samples,unique_keys=['Formula'],sort_by='degree')
#fig = upset.get('figure')
#ax = fig.get_axes()
plt.savefig(outputdata+"UpSetSamples.png",dpi=300)

"""
