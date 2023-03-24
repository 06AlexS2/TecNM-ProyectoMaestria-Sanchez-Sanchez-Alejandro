#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 11:48:11 2022

@author: alexs2
"""

from scipy import stats
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import statistics
from scipy.stats import norm

#videogame
#generar valores
vg_a = [38,
        37,
        42,
        53,
        44,
        44,
        55,
        37,
        44,
        39,
        46,
        47,
        45,
        46,
        42,
        40]

vg_b = [45,
        40,
        42,
        46,
        48,
        44,
        51,
        37,
        44,
        52,
        44,
        50,
        42,
        48,
        53,
        41]

#make a dataframe
df = pd.DataFrame(np.concatenate((np.vstack((vg_a, np.array(['a']*len(vg_a)))).T, 
                                  np.vstack((vg_a, np.array(['b']*len(vg_b)))).T)), columns = ['value', 'group'])


##valores de distribucion normal
df['value'] = df['value'].astype('float')
std1 = df['value'].std()
print("standard deviation:", std1)
mean1 = df['value'].mean()
print("mean:", mean1)

# Calculating probability density function (PDF)
pdf1 = stats.norm.pdf(df['value'].sort_values(), mean1, std1)

print("probability density function: ", pdf1)

##plotting normal distr
# Drawing a graph
plt.plot(df['value'].sort_values(), pdf1)
plt.xlim([30,70])  
plt.xlabel("STAI scores", size=16)    
plt.ylabel("Frequency", size=16)                
plt.grid(True, alpha=0.3, linestyle="--")
plt.show()

ax = sns.swarmplot(data = df, x = 'group', y = 'value', s = 8)
plt.ylim(bottom=0, top = df.value.max() + 2)
plt.show()

t_test = stats.ttest_rel(vg_a, vg_b)
print("videogame results: ", t_test)




#control
control_a = [33,
             40,
             39,
             51,
             39,
             39,
             40,
             45,
             43,
             36,
             49,
             43,
             45,
             48]

control_b = [31,
             47,
             36,
             48,
             41,
             44,
             43,
             46,
             41,
             42,
             47,
             49,
             49,
             52]

#concatenar y transponer arrays
df_2 = pd.DataFrame(np.concatenate((np.vstack((control_a, np.array(['a']*len(control_a)))).T, 
                                  np.vstack((control_a, np.array(['b']*len(control_b)))).T)), columns = ['value', 'group'])

df_2['value'] = df_2['value'].astype('float')
ax = sns.swarmplot(data = df_2, x = 'group', y = 'value', s = 8)
plt.ylim(bottom=0, top = df_2.value.max() + 2)
plt.show()

t_test_2 = stats.ttest_rel(control_a, control_b)
print("control results:", t_test_2)

