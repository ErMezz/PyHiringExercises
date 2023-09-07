# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 10:23:32 2023

@author: emezmat
"""

from math import e,log
import matplotlib.pyplot as plt

# Test script for the CIC compensator filter
A = -4
f = [i*0.001 for i in range(10000)]
c1 = -A/2
c2 = [(1-A) * e**(-1j*ww) for ww in f]
c3 = [A/2 * e**(-2j*ww) for ww in f]
y = [20*log(abs(c1+c2[i]+c3[i])) for i in range(len(f))]



plt.plot(f,y)
f = [i*0.001 for i in range(10000)]
y2 = [20*log(abs((1+e**(-3*1j*ff)) / (e**(-1j*ff)+1))) for ff in f]

# plt.plot(f,y2)

y3 = [y[i]+y2[i] for i in range(len(f))]

# plt.plot(f,y3)
