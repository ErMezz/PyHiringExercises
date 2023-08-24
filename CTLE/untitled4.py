# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 16:25:57 2023

@author: emezmat
"""

import scipy as sp
from skrf import Network
import numpy as np
import matplotlib.pyplot as plt
from array import array
from math import pi
import control as ct

ring_slot = Network('tx_test_ficture.s4p')
ring_slot.renumber([0, 1, 2, 3], [0, 2, 1, 3])  # pair ports as 1,3 and 2,4 to match experimental setup
ring_slot.se2gmm(p=2)


Garr = [0.891251,0.841395,0.794328,0.749894,0.707946,0.668344,0.630957,0.595662,0.562341,0.530884,0.501187,0.473151,0.446684,0.421697,0.398107,0.375837,0.354813]
P1,P2 = 26.5625*pi*2*1e9,14.1*pi*2*1e9
Z1arr = [9.463748*2*pi,9.248465*2*pi,9.069645*2*pi,8.640319*2*pi,8.255665*2*pi,7.906766*2*pi,7.58765*2*pi,7.076858*2*pi,6.614781*2*pi,6.193091*2*pi,5.805801*2*pi,5.448395*2*pi,5.117337*2*pi,4.809777*2*pi,4.523367*2*pi,4.256129*2*pi,4.006377*2*pi]
Plf = 1.2*2*pi*1e9
Zlfarr = [1.2*2*pi,1.15*2*pi,1.1*2*pi,1.075*2*pi,1.05*2*pi,1.025*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi]

i=4
G = Garr[i]
Z1 = Z1arr[i]*1e9
Zlf =Zlfarr[i]*1e9
MG = (G*P1*P2*Plf) / (Z1*Zlf)
num = [MG,MG * (Z1+Zlf), Z1*Zlf*MG]
den = [1,P1+P2+Plf,P1*P2 + P2*Plf + P1*Plf , P1*P2*Plf]
# num = [1]
# den = [1,2,1]
sys = (num,den)
H = ct.tf(num,den)
tau = [i*1e6 for i in range(0,50000)]
t=tau
y = [H(tt) for tt in t]
# t,y = sp.signal.impulse(sys,T=tau)

plt.plot(t,y)