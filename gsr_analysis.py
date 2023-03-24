#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 20:34:45 2023

@author: alexs2
"""

import matplotlib.pyplot as plt #used for visualization purposes in this tutorial.
import numpy as np
import pandas as pd
import pysiology
import csv
import emd
from matplotlib.ticker import LinearLocator, FuncFormatter
from datetime import datetime as dt
print(pysiology.__version__)
plt.style.use('default')
%matplotlib inline

##paso 0: cargar y mostrar el raw data
df = pd.read_csv('loggerdata/biologger phase A 05.10.2022, 16:00:00.csv', header=None, usecols=[6])
df.drop(df.index[30000:], inplace=True)
plt.figure(1)
plt.title('GSR Raw Data')
plt.xlabel('Sample Number')
plt.ylabel('GSR avg activity (bit unit)')
plt.plot(df)
plt.figure(figsize=(20,8))
plt.show()

##paso 1: crear un nuevo dataframe con los datos originales
gsrdf = df.copy()
gsrdf.columns = ['gsr_raw']

##paso 2: convertir el raw data a ohms mediante la formula
#ohms = ((1024+2*Serial_Port_Reading)*10000)/(512-Serial_Port_Reading)
gsrdf['gsr_ohms'] = ((1024 + (2*gsrdf['gsr_raw']))*10000)/(512-gsrdf['gsr_raw'])

##paso 3: invertir eso para dar lugar a los microsiemens
gsrdf['gsr_us'] = 1 / gsrdf['gsr_ohms']

##paso 3.5: convertir numero de samples a tiempo
max_time = (gsrdf['gsr_us'].size/50)/60 #sample rate
time_steps = np.linspace(0, max_time, gsrdf['gsr_us'].size)

##paso 4: graficar y ver resultados
#ohms
# plt.figure(2)
# plt.title('Impedancia de la piel en Ohms')
# plt.xlabel('tiempo (minutos)')
# plt.ylabel('Ohms')
# plt.plot(time_steps, gsrdf['gsr_ohms'])
# plt.figure(figsize=(20,8))

plt.show()

#microsiemens
plt.figure(3)
plt.title('Conductancia de la piel en siemens')
plt.xlabel('tiempo (minutos)')
plt.ylabel('Siemens')
plt.plot(time_steps, gsrdf['gsr_us'])
plt.figure(figsize=(20,8))
plt.show()

##paso 5: calcular promedio movil de microsiemens
gsrdf['MA_300'] = gsrdf['gsr_us'].rolling(300).mean()
gsrdf['MA_3000'] = gsrdf['gsr_us'].rolling(3000).mean()


##paso 6: graficar con el promedio movil la conductancia
# plt.figure(3)
# plt.title('Promedio movil de conductancia')
# plt.xlabel('tiempo (minutos)')
# plt.ylabel('Siemens')
# plt.plot(time_steps, gsrdf['gsr_us'],c = 'gray', label = 'EDA')
# plt.plot(time_steps, gsrdf['MA_300'], c = 'blue', label = 'PROMEDIO MOVIL 300')
# plt.plot(time_steps, gsrdf['MA_3000'], c = 'red',label = 'PROMEDIO MOVIL 3000')
# plt.legend()
# plt.figure(figsize=(20,8))
# plt.show()

#normalizar cada señal entre 0 y 1 los microsiemens
#luego promediar
#obtener mediana
#y sacar derivada

##paso 7: crear un tercer dataframe y copiar todos los datos de los 16 participantes
# gsr_prom = pd.DataFrame()
# gsr_prom['subject1'] = gsrdf['MA_300'].copy()
# #normalizar el dataframe
# gsr_prom = (gsr_prom - gsr_prom.min())/(gsr_prom.max() - gsr_prom.min())

# #guardar archivo (y cambios) en un csv para su posterior uso
# gsr_prom.to_csv('gsr_data/ma300_dummytest.csv', encoding='utf-8', index=False)

# #paso 7.5: guardar de nuevo los datos siguientes en el csv
# dummy_df = pd.read_csv('gsr_data/ma300_all_gsr.csv')
# dummy_df['subject16'] = gsrdf['MA_300'].copy()
# dummy_df['subject16'] = (dummy_df['subject16'] - dummy_df['subject16'].min())/(dummy_df['subject16'].max() - dummy_df['subject16'].min())
# dummy_df.to_csv('gsr_data/ma300_all_gsr.csv', index=False)

##paso 8: eliminar nans del dataframe

ma300gsr = pd.read_csv('gsr_data/ma300_all_gsr.csv')
ma300gsr = ma300gsr.dropna()

# ##paso 9: promediar todas las columnas y hacer un solo grafico con el promedio de cada fila
ma300gsr['all_mean'] = ma300gsr.mean(axis=1)

# ##paso 10: graficar columna de promedio

mean_max_time = (ma300gsr['all_mean'].size/50)/60 #sample rate
mean_time_steps = np.linspace(0, mean_max_time, ma300gsr['all_mean'].size)

plt.figure(4)
plt.title('Media de todas las mediciones de GSR (S)')
plt.xlabel('time (minutes)')
plt.ylabel('normalized_data')
plt.plot(mean_time_steps, ma300gsr['all_mean'],c = 'blue', label = 'EDA')
plt.legend()
plt.figure(figsize=(20,8))
plt.show()

##paso 11: obtener rolling mean del promedio normalizado de todas las mediciones
ma_normalized = pd.DataFrame()
ma_normalized['MA_1000'] = ma300gsr['all_mean'].copy().rolling(1000).mean()

##paso 12: graficar el rolling mean 300 de los datos normalizados y promediados
plt.figure(5)
plt.title('Media de todas las mediciones de GSR (S)')
plt.xlabel('time (minutes)')
plt.ylabel('normalized_data')
plt.plot(mean_time_steps, ma300gsr['all_mean'],c = 'blue', label = 'EDA')
plt.plot(mean_time_steps, ma_normalized['MA_1000'], c = 'red', label = 'R.A. (1000)')
plt.legend()
plt.figure(figsize=(20,8))
plt.show()

# ##paso 13: utilizar EMD para obtener los picos de la señal normalizada y promediada
sr = 50
imf = emd.sift.sift(ma300gsr['all_mean'])
print(imf.shape)

IP, IF, IA = emd.spectra.frequency_transform(imf, sr, 'hilbert')

emd.plotting.plot_imfs(imf)

plt.figure(6)
plt.title('IMF-8')
plt.xlabel('time (minutes)')
plt.ylabel('Signal Influence (Normalized Data)')
plt.plot(mean_time_steps, imf[:,7])
plt.figure(figsize=(20,8))
plt.show()

plt.figure(7)
plt.title('IMF-7')
plt.xlabel('time (minutes)')
plt.ylabel('Signal Influence (Normalized Data)')
plt.plot(mean_time_steps, imf[:,6])
plt.figure(figsize=(20,8))
plt.show()

plt.figure(8)
plt.title('IMF-6')
plt.xlabel('time (minutes)')
plt.ylabel('Signal Influence (Normalized Data)')
plt.plot(mean_time_steps, imf[:,5])
plt.figure(figsize=(20,8))
plt.show()

##paso 14: sumar señales IMF 8+7, 8+6, 8+7+6

imfdf = pd.DataFrame()
imfdf['imf87'] = imf[:,7] + imf[:,6]
imfdf['imf86'] = imf[:,7] + imf[:,5]
imfdf['imf876'] = imf[:,7] + imf[:,6] + imf[:,5]

plt.figure(9)
plt.title('IMF-8 + IMF-7')
plt.xlabel('time (minutes)')
plt.ylabel('Signal Influence (Normalized Data)')
plt.plot(mean_time_steps, imfdf['imf87'])
plt.figure(figsize=(20,8))
plt.show()

plt.figure(10)
plt.title('IMF-8 + IMF-6')
plt.xlabel('time (minutes)')
plt.ylabel('Signal Influence (Normalized Data)')
plt.plot(mean_time_steps, imfdf['imf86'])
plt.figure(figsize=(20,8))
plt.show()

plt.figure(11)
plt.title('IMF-8 + IMF-7 + IMF-6')
plt.xlabel('time (minutes)')
plt.ylabel('Signal Influence (Normalized Data)')
plt.plot(mean_time_steps, imfdf['imf876'])
plt.figure(figsize=(20,8))
plt.show()

##paso 15: derivar IMF-8, IMF-8+7, IMF-8+7+6
#nota: aparentemente el gradiente es el equivalente numérico a la solución diferencial de un arreglo
#se crea un array de las columnas con los resultados de las IMF obtenidas anteriormente
imf_87 = imfdf[['imf87']].to_numpy()
imf_86 = imfdf[['imf86']].to_numpy()
imf_876 = imfdf[['imf876']].to_numpy()

#se crean arrays para el rango del gradiente con base en los arrays de valores de imf anteriormente
#creados

alfa = np.arange(imf_87.size)
beta = np.arange(imf_86.size)
gamma = np.arange(imf_876.size)

#ahora si, se utiliza la función de gradiente

der87 = np.gradient(imf_87, alfa, axis=0)
der86 = np.gradient(imf_86, beta, axis=0)
der876 = np.gradient(imf_876, gamma, axis=0)

#graficar las derivadas de los imfs
plt.figure(12)
plt.title('Derivada de IMF-8 + IMF-7')
plt.xlabel('time (minutes)')
plt.ylabel('Derivated Sum of Comps. (Normalized Data)')
plt.plot(mean_time_steps, der87)
plt.axvline(x=0, c="red", label="x=0")
plt.axhline(y=0, c="red", label="y=0")
plt.figure(figsize=(20,8))
plt.show()

plt.figure(13)
plt.title('Derivada de IMF-8 + IMF-6')
plt.xlabel('time (minutes)')
plt.ylabel('Derivated Sum of Comps. (Normalized Data)')
plt.plot(mean_time_steps, der86)
plt.axvline(x=0, c="red", label="x=0")
plt.axhline(y=0, c="red", label="y=0")
plt.figure(figsize=(20,8))
plt.show()

plt.figure(14)
plt.title('Derivada de IMF-8 + IMF-7 + IMF-6')
plt.xlabel('time (minutes)')
plt.ylabel('Derivated Sum of Comps. (Normalized Data)')
plt.plot(mean_time_steps, der876)
plt.axvline(x=0, c="red", label="x=0")
plt.axhline(y=0, c="red", label="y=0")
plt.figure(figsize=(20,8))
plt.show()


##paso 16: obtener el porcentaje de datos positivos y negativos para cada derivada
res_der87 = (len([ele for ele in der87 if ele >= 0]) / len(der87)) * 100
print("el porcentaje de datos positivos en la derivada numérica de IMF-8 + IMF-7 es:", res_der87)
print("y la cantidad de tiempo (max: 10 min) respecto a ese porcentaje es de: ", 10*(res_der87/100), "minutos.")

res_der86 = (len([ele for ele in der86 if ele >= 0]) / len(der86)) * 100
print("el porcentaje de datos positivos en la derivada numérica de IMF-8 + IMF-6 es:", res_der86)
print("y la cantidad de tiempo (max: 10 min) respecto a ese porcentaje es de: ", 10*(res_der86/100), "minutos.")

res_der876 = (len([ele for ele in der876 if ele >= 0]) / len(der876)) * 100
print("el porcentaje de datos positivos en la derivada numérica de IMF-8 + IMF-7 + IMF-6 es:", res_der876)
print("y la cantidad de tiempo (max: 10 min) respecto a ese porcentaje es de: ", 10*(res_der876/100), "minutos.")

 
