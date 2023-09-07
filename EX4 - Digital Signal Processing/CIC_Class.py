"""
Created on Fri Sep  1 11:32:52 2023

@author: emezmat
"""
import random
import control as ct
from math import sin,pi,cos,e
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

class integrator:
    def __init__(self):
        self.yn  = 0
        self.ynm = 0
    
    def update(self, inp):
        self.ynm = self.yn
        self.yn  = (self.ynm + inp)
        return (self.yn)
        
class comb:
    def __init__(self):
        self.xn  = 0
        self.xnm = 0
    
    def update(self, inp):
        self.xnm = self.xn
        self.xn  = inp
        return (self.xn - self.xnm)
    
class CIC:
    def __init__(self,decim,order):
        self.integ = [integrator()]*order
        self.comb = [comb()]*order
        self.data = 0
        self.count = -1
        self.decim = decim
    
    def update(self,inp):
        data = inp
        for integ in self.integ:
            data = integ.update(data)
        self.count += 1
        if self.count % self.decim == 0:
            self.count = 0
            for comb in self.comb:
                data = comb.update(data)
            return data
        else: return False

class Dig_FIL:
    def __init__(self,taps=[]):
        self.taps = taps
        self.val = []
        
    def update(self,data):
        self.val.append(data)
        if (len(self.val)) > (len(self.taps)-1): self.val.pop(0)
        out = 0
        for i in range(len(self.taps)):
            if i > len(self.val)-1: break
            out += self.val[-i-1] * self.taps[i]
        return out
            
            
def inp_samp(x):
    z = 0
    z += 10 * random.randint(-10000,10000)/10000 # noise
    for fr in range(100):
        z += 1 * np.sin(2 * pi * (4000) * x + (50-fr)*100)
    z += 10 * np.sin(2 * pi * 4000 * x)
    return z


decimation = 25
N = 1
gain = (decimation * 1) ** N

A = 10 #CIC compensator taps
B= 1-A #CIC compensator taps
CG = A+A+B

NN=32
bands = [0., .22, .28, .5]
h = signal.remez(NN+1, bands, [1,0], [1,1])
h[abs(h) <= 1e-4] = 0.
TG = sum(h)

FIL_Q = CIC(decimation,N)
FIL_P = CIC(decimation,N)
Q_CICComp = Dig_FIL([A,B,A])
P_CICComp = Dig_FIL([A,B,A])
Q_FIR = Dig_FIL(h)
P_FIR = Dig_FIL(h)

samples = 1e5+1
dT = 1e-6

t = [tt*dT for tt in range(int(samples))]
undert = [tt*dT*decimation*2 for tt in range(int(samples)//(decimation*2))]

y = [inp_samp(x) for x in t]
yQ = [inp_samp(x)*e**(1j*2*pi*4000*x) for x in t]
yP = [inp_samp(x)*e**(-1j*2*pi*4000*x) for x in t]
# yQ = [inp_samp(x)*1j*sin(2*pi*4000*x) for x in t]
# yP = [inp_samp(x)*cos(2*pi*4000*x) for x in t]
# yQ = [1,2,3,4,5,6,7,8]
z = np.fft.fft(y)
z = (z/len(z)).tolist()
z = z [len(z)//2:] + z[:len(z)//2]
z = [zz.imag for zz in z]
ff = np.fft.fftfreq(len(t),dT).tolist()
ff = (ff[len(ff)//2:] + ff[:len(ff)//2])
plt.plot(ff,z)

rebuild_Q = []
ss = []
re = True
for (s, v) in enumerate(yQ):
    up = FIL_Q.update(v)
    if type(up) != bool: 
        up = Q_CICComp.update(up)/CG
        up = Q_FIR.update(up)/TG
        if re: 
            rebuild_Q.append(up/gain)
            re=False
        else: re=True
        ss.append(s)

rebuild_P = []
pp=[]
re = True
for (s, v) in enumerate(yP):
    up = FIL_P.update(v)
    if type(up) != bool: 
        up = P_CICComp.update(up)/CG
        up = P_FIR.update(up)/TG
        if re: 
            rebuild_P.append(up/gain)
            re=False
        else: re=True
        pp.append(s)

z = np.fft.fft(rebuild_Q).tolist()
z = z [len(z)//2:] + z[:len(z)//2]
z = [zz.imag for zz in z]
ff = np.fft.fftfreq(len(t)//decimation,dT*decimation).tolist()
ff = (ff[len(ff)//2:] + ff[:len(ff)//2])
# plt.plot(ff,z)

z = np.fft.fft(rebuild_P).tolist()
z = z [len(z)//2:] + z[:len(z)//2]
z = [zz.imag for zz in z]
ff = np.fft.fftfreq(len(t)//decimation,dT*decimation).tolist()
ff = (ff[len(ff)//2:] + ff[:len(ff)//2])
# plt.plot(ff,z)

rebuild = [rebuild_Q[tt]*e**(-1j*2*pi*4000*undert[tt]) + rebuild_P[tt]*e**(1j*2*pi*4000*undert[tt]) for tt in range(len(undert))]
# rebuild = [rebuild_Q[tt]*1j*sin(2*pi*4000*undert[tt]) + rebuild_P[tt]*cos(2*pi*4000*undert[tt]) for tt in range(len(undert))]
z = np.fft.fft(rebuild)
z = (z/len(z)).tolist()
z = z [len(z)//2:] + z[:len(z)//2]
z = [zz.imag for zz in z]
ff = np.fft.fftfreq(len(t)//(decimation*2),dT*decimation*2).tolist()
ff = (ff[len(ff)//2:] + ff[:len(ff)//2])
plt.plot(ff,z)


plt.figure(2)
plt.plot(t,y)
plt.plot(undert,rebuild)
