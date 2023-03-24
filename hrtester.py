#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 00:03:44 2022

@author: alexs2
"""

import heartpy as hp
import pandas as pd
import matplotlib.pyplot as plt


fs = 50
df = pd.read_csv('loggerdata/biologger phase A 26.09.2022, 15:00:00.csv', header=None, usecols=[7])

dataline = df.to_csv('hrdftestreal1.csv', header=None, index=False)

data = hp.get_data('hrdftestreal1.csv')
scaled_data = hp.scale_data(data)
plt.figure(figsize=(12,4))
plt.plot(data)
plt.show()
plt.plot(scaled_data)
plt.show()

wd, m = hp.process(scaled_data, sample_rate = 50.0)

#set large figure
plt.figure(figsize=(40,16))

#call plotter
hp.plotter(wd, m)

#display measures computed
for measure in m.keys():
    print('%s: %f' %(measure, m[measure]))




# scaled_data = hp.scale_data(data, lower=0, upper=516)
# enhanced_data = hp.enhance_peaks(scaled_data)

# working_data, measures = hp.process(smooth_data, 50.0)
# hp.plotter(working_data, measures)


# working_data, measures = hp.process(data, welch_wsize=250, sample_rate=50.0)
# hp.plotter(working_data, measures)