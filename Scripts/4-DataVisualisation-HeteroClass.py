# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 15:04:37 2017

@author: Will Kew
will.kew@gmail.com
"""

import pandas as pd
import itertools

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

#from matplotlib import cm
#from matplotlib import ticker
import re
#import numpy as np

#This sorts HeteroClassatomic class into logical orders.
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', s)]

path = "F:/Will/Dropbox/Documents/University/Edinburgh/FTICRMS/MixedIonisation3-formularity/"
path = "C:/Users/Will/Dropbox/Documents/University/Edinburgh/FTICRMS/MixedIonisation3-formularity/"

#inputdata = path +"ReformAssignments/"
outputdata = path+"Images/HeteroatomicDists/"

df1 = pd.read_excel(path+"AllHits-Longform.xlsx",sheet_name="Sheet1")
norm = False
#df1 = pd.read_excel(path+"AllHits-Longform-Norm.xlsx")
#norm = True
df1 = df1[df1['Mass']<800]
df1 = df1[df1['O']<20]
"""
sns.set_style("white")
sns.set_context("paper",font_scale=2)
glocmap = cm.viridis_r
"""

""" ### THIS IS PLAYING WITH PLOTTING DISTRIBUTIONS AS A KDE INSTEAD OF A BARPLOT.
df3 = pd.DataFrame(df2[df2['HeteroClass']!="CH"]['HeteroClass'])
df3['Mode'] = pd.DataFrame(df2[df2['HeteroClass']!="CH"]['Mode'])

hetclasses = list(df3['HeteroClass'])

hetclasses = [int(x.split('O')[1]) for x in hetclasses]
df3['O'] = hetclasses

sns.distplot(df3[df3["Mode"]=="APPI"]['O'])
plt.show()
"""


plt.rcdefaults()

order= list(set(df1['HeteroClass']))
order.sort(key=natural_sort_key) # this natural sort function ensures a logical order to your barplot.
CHOorder = [x for x in order if 'CH' not in x]


### THIS DOES THE SET/UNIQUE FORMULA COUNTING STEP ####
staticolumns = ['C','H','O','OC','HC','Mass','DBE','AImod']
df2 = df1.rename(columns={'id':'Count'}).groupby(['Mode','Formula'],as_index=False)['Count'].count()
df2['Abundance'] = df1.groupby(['Mode','Formula'],as_index=False)['Abundance'].median()['Abundance']
df2['HeteroClass'] = df1.groupby(['Mode','Formula'],as_index=False)['HeteroClass'].first()['HeteroClass']
df2[staticolumns] = df1.groupby(['Mode','Formula'],as_index=False)[staticolumns].mean()[staticolumns]
def HeteroClassplot(df):
    #This produces a HeteroClassatomic class plot, posoitive above, negative below, no class or sample info.
    g = sns.factorplot(x='HeteroClass',data=df,
                   #row = 'Polarity',#hue='Mode',
                   kind='count',order=CHOorder,#ax=ax,
                   size = 4,aspect=2,
                   #palette = sns.color_palette("Set1", len(CHOorder)))
                   palette=sns.cubehelix_palette(int(len(CHOorder)),dark=0,light=0.6,rot=0,reverse=True))
    [plt.setp(ax.get_xticklabels(), rotation=90) for ax in g.axes.flat]
    plt.subplots_adjust(hspace=0.4)
    fig = g.fig
    fig.savefig(outputdata+"HeteroClassPlot.png",dpi=300)

    #### THIS PRODUCES THE Plot with Mode Hue #####
    g = sns.factorplot(x='HeteroClass',data=df,
           hue='Mode',#row = 'Polarity',
           kind='count',order=CHOorder,#ax=ax,
           alpha=0.5,
           #size = 2,
           #aspect=2,
           #facecolor=(0,0,0),
           #edgecolor=sns.color_palette("Set1", 4),legend=False)
           edgecolor=['k']*40,
           palette = sns.color_palette("Set1", 4),legend=False)
                   #palette=sns.cubehelix_palette(int(len(CHOorder)),dark=0,light=0.6,rot=0,reverse=True))
    (g.set_axis_labels("Heteroatomic Class", "Count")
    .set_titles(""))
    #.despine(left=True))
    plt.xticks(rotation=90)
    plt.legend(loc=1)
    [plt.setp(ax.get_xticklabels(), rotation=90) for ax in g.axes.flat]
    fig = g.fig
    fig.set_size_inches(3.25*2,4)
    plt.tight_layout()
    fig.savefig(outputdata+"HeteroClassPlot-byMode.png",dpi=300)
    plt.show()


def HeteroClassplot2(df):
    #### THIS PRODUCES THE Plot with Mode Hue #####
    a_val=1
    colors = sns.color_palette("Paired", 4)
    g = sns.factorplot(x='HeteroClass',data=df,
           hue='Mode',#row = 'Polarity',
           kind='count',order=CHOorder,#ax=ax,
           #alpha=a_val,
           #size = 2,
           #aspect=2,
           #facecolor=(0,0,0),
           #edgecolor=sns.color_palette("Set1", 4),legend=False)
           edgecolor=['k']*40,
           palette = colors,legend=False)
                   #palette=sns.cubehelix_palette(int(len(CHOorder)),dark=0,light=0.6,rot=0,reverse=True))
    (g.set_axis_labels("Heteroatomic Class", "Count")
    .set_titles(""))
    #.despine(left=True))
    """
    num_locations = len(df['HeteroClass'].unique())
    hatches = itertools.cycle(['////', '\\\\\\', '----', 'xxx',  '*', 'o', 'O', '.'])
    for i, bar in enumerate(g.ax.patches):
        if i % num_locations == 0:
            hatch = next(hatches)
        bar.set_hatch(hatch)

    #hatches = ['////']*19+['\\\\\\']*18+['----']*18+['xxx']*19
    hatches = {colors[0]:'////',
               colors[1]:'\\\\\\',
               colors[2]:'----',
               colors[3]:'xxx'}
    for i,thisbar in enumerate(g.ax.patches):
        # Set a different hatch for each bar
        #thisbar.properties()['facecolor']
        thisbar.set_hatch(hatches[thisbar.properties()['facecolor']])
    """
    hatches = ['////']*20+['\\\\\\']*18+['----']*18+['xxx']*20
    for i,thisbar in enumerate(g.ax.patches):
        # Set a different hatch for each bar
        thisbar.set_hatch(hatches[i])
    plt.xticks(rotation=90)
    circ1 = mpatches.Patch( facecolor=colors[0],alpha=a_val,hatch='////',label='APCI')
    circ2= mpatches.Patch( facecolor=colors[1],alpha=a_val,hatch='\\\\\\',label='APPI')
    circ3 = mpatches.Patch(facecolor=colors[2],alpha=a_val,hatch='----',label='ESI')
    circ4 = mpatches.Patch(facecolor=colors[3],alpha=a_val,hatch='xxx',label='LDI')

    plt.legend(handles = [circ1,circ2,circ3,circ4],loc=1)
    #plt.legend(loc=1)
    [plt.setp(ax.get_xticklabels(), rotation=90) for ax in g.axes.flat]
    fig = g.fig
    fig.set_size_inches(3.25*2,4)
    plt.tight_layout()
    fig.savefig(outputdata+"HeteroClassPlot-byMode.png",dpi=300)
    plt.show()

sns.set_context('paper',rc={'figure.figsize':(8,6)})
plt.rcdefaults()
#sns.set(rc={'figure.figsize':(20,10)})
HeteroClassplot2(df2)


"""
#Stacked Bar Plot Experiments. - its gross.
modes = ["APCI","APPI","ESI","LDI"]
pal = sns.color_palette("Set1", len(modes))
colors = {'APCI':pal[0], 'APPI':pal[1], 'ESI':pal[2], 'LDI':pal[3]}

df_total = df2['HeteroClass'].value_counts()
df_APCI = df2[df2['Mode']=='APCI']['HeteroClass'].value_counts()
df_APPI = df2[df2['Mode']=='APPI']['HeteroClass'].value_counts()
df_ESI = df2[df2['Mode']=='ESI']['HeteroClass'].value_counts()
df_LDI = df2[df2['Mode']=='LDI']['HeteroClass'].value_counts()

sns.barplot(x = df_total.index, y = df_total.values, color = colors['APPI'],order=CHOorder)

LDI = sns.barplot(x = df_LDI.index, y = df_LDI.values, color = colors['LDI'],order=CHOorder,alpha=0.5,linewidth=2.5,edgecolor='k')
APCI = sns.barplot(x = df_APCI.index, y = df_APCI.values, color = colors['APPI'],order=CHOorder,alpha=0.5)
APPI = sns.barplot(x = df_APPI.index, y = df_APPI.values, color = colors['APCI'],order=CHOorder,alpha=0.5)
ESI = sns.barplot(x = df_ESI.index, y = df_ESI.values, color = colors['ESI'],order=CHOorder,alpha=0.5)

LDI = sns.barplot(x = df_LDI.index, y = df_LDI.values, order=CHOorder,linewidth=2.5,facecolor=(1,1,1,0),edgecolor=['k']*20)
APCI = sns.barplot(x = df_APCI.index, y = df_APCI.values,  order=CHOorder,linewidth=2.5,facecolor=(1,0,0,0.5),edgecolor=['k']*20)
APPI = sns.barplot(x = df_APPI.index, y = df_APPI.values,  order=CHOorder,linewidth=2.5,facecolor=(0,1,0,0.5),edgecolor=['k']*20)
ESI = sns.barplot(x = df_ESI.index, y = df_ESI.values,  order=CHOorder,linewidth=2.5,facecolor=(0,0,1,0.5),edgecolor=['k']*20)
plt.show()




"""
"""
#This will plot KDEs for the O class
modes = ['APCI','APPI','ESI','LDI']
for mode in modes:
    sns.distplot(df1[df1['Mode']==mode]['O'],hist=False,kde_kws={'bw':1})

"""
