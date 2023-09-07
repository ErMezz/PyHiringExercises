# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 16:08:27 2023

@author: emezmat
"""
from math import log10
from numpy import angle
from scipy import signal
import matplotlib.pyplot as plt

# Half-Band FIR
NN=32
bands = [0., .44, .56, 1.]
h2 = signal.remez(NN+1, bands, [1,0], [1,1],fs=2)
h2[abs(h2) <= 1e-4] = 0.
x2,y2 = signal.freqz(h2,fs=4*1e6,worN=512)
y2 = [20*log10(abs(yy)) for yy in y2]
ph2 = [angle(yy) for yy in y2]

# CIC
D=25
h3 = [1] + [0]*(D-1) + [-1]
h3den = [D,-D]
x3,y3 = signal.freqz(h3,h3den,fs=100*1e6,worN=512*25)
y3 = [20*log10(abs(yy**2)) for yy in y3]
ph3 = [angle(yy) for yy in y3]

# Post-CIC compensation FIR
a = 0.05
x4,y4 = signal.freqz([-a/(1-2*a),1/(1-2*a),-a/(1-2*a)],[1],fs=4*1e6,worN=512)
y4 = [20*log10(abs(yy**2)) for yy in y4]
ph4 = [angle(yy) for yy in y4]

y5 = [y2[i]+y3[i]+y4[i] for i in range(len(y4))]
ph5 = [(ph2[i]+ph3[i]+ph4[i]) for i in range(len(y4))]
# plt.plot(x4,y5)
plt.plot(x4,ph5)