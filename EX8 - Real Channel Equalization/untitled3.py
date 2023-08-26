import control as ct
import numpy as np
import matplotlib.pyplot as plt
from math import pi
import skrf
from skrf import Network
from functools import reduce
import pandas as pd

class PRBS_seq():
    
    def __init__(self,taps = [13,12,2,1],start_val=1,PRBSQ=True):
        mask = pow(2,max(taps))-1
        curr = start_val
        i=0
        self.seq = 1
        while (1):            
            newbit = reduce(lambda x,y: x^y, [(curr & 1<<(tap-1))>>tap-1 for tap in taps] )  
            self.seq = (self.seq<<1) | newbit
            curr = (curr << 1) | newbit
            curr = curr & mask
            i+=1
            if curr == start_val:
                self.size = i
                break
        if PRBSQ: self.seq = (self.seq << self.size) | self.seq
        self.Nseq = pd.Series('')
            
    def Sample_PAM4(self,sig_freq,Vpeak):
        sig_t = 1/sig_freq
        timescale =  [0]
        seq = []
        i=0
        MUL = 10
        while i < self.size:
            seq = seq + [round((((((0b11 << i) & self.seq)>>i)-1.5)*Vpeak)/1.5,3)]*MUL
            if MUL != 1: timescale = timescale + [timescale[-1]+sig_t*j for j in range(0,MUL)]
            else: timescale = timescale + [timescale[-1]+sig_t]
            i+=2

        timescale.pop(0)
        self.Nseq = seq
        return timescale



Garr = [0.891251,0.841395,0.794328,0.749894,0.707946,0.668344,0.630957,0.595662,0.562341,0.530884,0.501187,0.473151,0.446684,0.421697,0.398107,0.375837,0.354813]
P1,P2 = 26.5625*pi*2*1e9,14.1*pi*2*1e9
Z1arr = [9.463748*2*pi,9.248465*2*pi,9.069645*2*pi,8.640319*2*pi,8.255665*2*pi,7.906766*2*pi,7.58765*2*pi,7.076858*2*pi,6.614781*2*pi,6.193091*2*pi,5.805801*2*pi,5.448395*2*pi,5.117337*2*pi,4.809777*2*pi,4.523367*2*pi,4.256129*2*pi,4.006377*2*pi]
Plf = 1.2*2*pi*1e9
Zlfarr = [1.2*2*pi,1.15*2*pi,1.1*2*pi,1.075*2*pi,1.05*2*pi,1.025*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi]

a = PRBS_seq()
ts = a.Sample_PAM4(50*1e9, 0.4)

f = 10
freq = 10 * 2 * pi
w = 2*pi*f

plt.figure(1)
plt.subplot(211)

i=1
G = Garr[i]
Z1 = Z1arr[i]*1e9
Zlf =Zlfarr[i]*1e9
MG = (G*P1*P2*Plf) / (Z1*Zlf)
num = np.array([MG,MG * (Z1+Zlf), Z1*Zlf*MG])
den = np.array([1,P1+P2+Plf,P1*P2 + P2*Plf + P1*Plf , P1*P2*Plf])
H = ct.tf(num , den)
pp = [p/1e13 for p in range(-100000,100001)]
ppy = [0 for p in pp]
for i in range(0,len(pp)):
    if pp[i] == 0: 
        ppy[i-1],ppy[i],ppy[i+1]=100,100,100
tt, yy = ct.step_response(H)


ring_slot = Network('tx_test_ficture.s4p')

ring_slot.renumber([0, 1, 2, 3], [0, 2, 1, 3])  # pair ports as 1,3 and 2,4 to match experimental setup

ring_slot.se2gmm(p=2)
t,y = ring_slot.impulse_response(pad=10000)
y = y[:,0,1]


plt.plot(t,y)
plt.subplot(212)
plt.plot(np.convolve(y,yy))
# # for i in range(0,18):
# i=1
# G = Garr[i]
# Z1 = Z1arr[i]*1e9
# Zlf =Zlfarr[i]*1e9
# MG = (G*P1*P2*Plf) / (Z1*Zlf)
# num = np.array([MG,MG * (Z1+Zlf), Z1*Zlf*MG])
# den = np.array([1,P1+P2+Plf,P1*P2 + P2*Plf + P1*Plf , P1*P2*Plf])
# H = ct.tf(num , den)
# tt, yy = ct.impulse_response(H)

# plt.plot(np.convolve(OU,yy))

# plt.legend()
plt.show()