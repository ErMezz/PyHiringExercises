# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 16:08:27 2023

@author: emezmat
"""
from math import log10,pi
from scipy import signal
import matplotlib.pyplot as plt

A = 10 #CIC compensator taps
B= 1-A #CIC compensator taps
h1 = [A,B,A]
x1,y1 = signal.freqz(10,fs=2)
y1 = [20*log10(abs(yy)/(A+1)) for yy in y1]



NN=32
bands = [0., .44, .56, 1.]
h2 = signal.remez(NN+1, bands, [1,0], [1,1],fs=2)
h2[abs(h2) <= 1e-4] = 0.
x2,y2 = signal.freqz(h2,fs=2,worN=512)
y2 = [20*log10(abs(yy)) for yy in y2]


D=25
h3 = [1] + [0]*(D-1) + [-1]
h3den = [1,-1]
x3,y3 = signal.freqz(h3,h3den,fs=50,worN=512*25)
y3 = [20*log10(abs(yy**1)) for yy in y3]
y3 = [yy-y3[1] for yy in y3]

# x1 = x1/D
# x2 = x2/D
# plt.plot(x1,y1)
plt.plot(x2,y2)
plt.plot(x3,y3)
y4 = [y2[i]+y3[i] for i in range(len(y1))]
plt.plot(x1,y4)