#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 19:41:33 2022

@author: alexs2
"""

import heartpy as hp
import pandas as pd
import matplotlib.pyplot as plt

##segmento del ppg
##cargar y limpiar datos

# fs = 50.0
# df = pd.read_csv('loggerdata/biologger phase A 05.10.2022, 16:00:00.csv', header=None, usecols=[7])
# df.drop(df.index[:2500], inplace=True)
# df.drop(df.index[30000:], inplace=True)
# df.clip(495, 525, inplace=True)

# # 
# plt.figure(1)
# plt.plot(df)
# plt.figure(figsize=(12,4))
# plt.show

# dataset = df.to_csv('processed/habibisaac_sansoreschale.csv', header=None, index=False)

# data = hp.get_data('processed/habibisaac_sansoreschale.csv')
# # data = hp.flip_signal(data, enhancepeaks=False, keep_range=True)
# data = hp.filter_signal(data, cutoff=[0.75,3.5], sample_rate=fs, order=3, filtertype='bandpass')
# data = hp.scale_data(data, lower=0, upper=1023)


# data = hp.enhance_peaks(data)



# wd,m = hp.process(data, sample_rate = fs)
# # 
# hp.plotter(wd, m)


##segmento del gsr
df = pd.read_csv('loggerdata/biologger phase A 05.10.2022, 16:00:00.csv', header=None, usecols=[6])
df.drop(df.index[30000:], inplace=True)
plt.figure(1)
plt.plot(df)
plt.figure(figsize=(20,8))
plt.show()

