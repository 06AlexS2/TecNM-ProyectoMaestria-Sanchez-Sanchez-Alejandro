#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 21:31:14 2023

@author: alexs2
"""

from wordcloud import WordCloud, STOPWORDS , ImageColorGenerator
import pandas as pd
import matplotlib.pylab as plt
from PIL import Image
import numpy as np

stopwords = set(STOPWORDS)
# mask = np.array(Image.open('E:/twiiter.png'))

#we will read the text
data_file = pd.read_csv('Cuestionario de experiencia de uso (jugador).csv')
#wordcloud
wordcloud = WordCloud(stopwords = stopwords , width=1600 , height=800,background_color="White",colormap="Set2").generate(''.join(data_file['text']))
plt.figure(figsize=(20,10),facecolor='k')
plt.imshow(wordcloud,interpolation='bilinear')
plt.axis('off')
plt.tight_layout (pad=0)

#saving the image of wordcloud
wordcloud.to_file ('wordcloud1.png')
plt.show()