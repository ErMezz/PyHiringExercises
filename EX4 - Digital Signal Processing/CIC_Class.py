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
    
    def update(self, inp, decimation):
        self.xnm = self.xn
        self.xn  = inp
        return (self.xn - self.xnm)/decimation
    
class CIC:
    def __init__(self,decim,order):
        self.integ = []
        for i in range(order):
            self.integ.append(integrator())
        self.comb = []
        for i in range(order):
            self.comb.append(comb())
        self.count = -1
        self.decim = decim
        self.gain = decim**order
    
    def update(self,inp):
        data = inp
        for integ in self.integ:
            data = integ.update(data)
        self.count += 1
        if self.count % self.decim == 0:
            self.count = 0
            for comb in self.comb:
                data = comb.update(data,self.decim)
            return True,data
        else: return False,data

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
            
if __name__  == '__main__':
    def inp_samp(x):
        z = 0
        z += 10 * random.randint(-10000,10000)/10000 # noise
        for fr in range(10):
            z += 1 * np.sin(2 * pi * (4000) * x + (5-fr)*100)
        z += 10 * np.sin(2 * pi * 4000 * x)
        return z
    
    
    decimation = 25
    N = 2
    gain = (decimation * 1) ** N
        
    NN=32
    bands = [0., .22, .28, .5]
    h = signal.remez(NN+1, bands, [1,0], [1,1])
    h[abs(h) <= 1e-4] = 0.
    TG = sum(h)
    
    FIL_Q = CIC(decimation,N)
    Q_FIR = Dig_FIL(h)
    
    samples = 1e5
    dT = 1e-6
    
    t = [tt*dT for tt in range(int(samples))]
    undert = [tt*dT*decimation*2 for tt in range(int(samples)//(decimation*2))]
    
    y = [inp_samp(x) for x in t]
    plt.plot(t,y)
    resample = []
    re = True
    for (s, v) in enumerate(y):
        sample,up = FIL_Q.update(v)
        if sample: 
            up = Q_FIR.update(up)/TG

            if re: 
                resample.append(up)
                re=False
            else: re=True
    
    plt.plot(undert,resample)