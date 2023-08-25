import control as ct
import numpy as np
import matplotlib.pyplot as plt
from math import pi,floor,log10
from PRBS import PRBS_seq
#%matplotlib qt
import pandas as pd
import scipy as sp
from skrf import Network



Garr = [0,0.891251,0.841395,0.794328,0.749894,0.707946,0.668344,0.630957,0.595662,0.562341,0.530884,0.501187,0.473151,0.446684,0.421697,0.398107,0.375837,0.354813]
P1,P2 = 26.5625*pi*2*1e9,14.1*pi*2*1e9
Z1arr = [1,9.463748*2*pi,9.248465*2*pi,9.069645*2*pi,8.640319*2*pi,8.255665*2*pi,7.906766*2*pi,7.58765*2*pi,7.076858*2*pi,6.614781*2*pi,6.193091*2*pi,5.805801*2*pi,5.448395*2*pi,5.117337*2*pi,4.809777*2*pi,4.523367*2*pi,4.256129*2*pi,4.006377*2*pi]
Plf = 1.2*2*pi*1e9
Zlfarr = [1,1.2*2*pi,1.15*2*pi,1.1*2*pi,1.075*2*pi,1.05*2*pi,1.025*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi]

for j in range(1,len(Garr)):
    G = Garr[j]
    Z1 = Z1arr[j]*1e9
    Zlf = Zlfarr[j]*1e9
    # MG = (G*P1*P2*Plf) / (Z1*Zlf)
    MG=1
    
    num = np.array([MG,MG * (Z1+Zlf), MG * Z1 * Zlf])
    den = np.array([1,P1+P2+Plf,P1*P2 + P2*Plf + P1*Plf , P1*P2*Plf])
    if j==0: H = ct.tf([1],[1])
    else: H = ct.tf(num , den)
    t = [100e6 + i * 100e6 for i in range(0,400)]
    
    # plt.yscale("log")
    NF = P1 / (2*pi*2)
    
    if j == 1: Boss = H(0)
    
    # plt.plot(t,[H(tt) for tt in t],label = f'{j/2+0.5}')
    mag, ph, omega = ct.bode_plot(H,dB=False ,Hz = True, plot = False)
    mag2 = mag.tolist()
    maxmag = max(mag2)
    omega = omega / (2*pi)
    plt.xscale("log")

    plt.plot(omega/1e9,[20*log10(magg/maxmag) for magg in mag], label = f'{j/2+0.5}')
    print("doneso")
plt.legend()
