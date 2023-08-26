# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 09:08:28 2023

@author: emezmat
"""
from functools import reduce
import pandas as pd
import matplotlib.pyplot as plt
import control as ct
import numpy as np
from math import pi, sqrt
from skrf import Network, Frequency

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
        self.Nseq = pd.Series(seq,timescale)


plt.figure(1)
plt.subplot(211)

a,b = PRBS_seq(),PRBS_seq()
a.Sample_PAM4(50*1e9, 0.2)
b.Sample_PAM4(50*1e9, 0.2)
b.Nseq = -b.Nseq
# plt.plot(a.Nseq-b.Nseq)

ring_slot = Network('tx_test_ficture.s4p')

y,f,z = plt.magnitude_spectrum(a.Nseq-b.Nseq,Fs=500*1e9)
yy,ff,zz = plt.phase_spectrum(a.Nseq-b.Nseq,Fs=500*1e9)

fre,fact = ring_slot.f,ring_slot.s

appo = []
c=0
for i in fact:
    for j in i:
        if c == 0:
            appo.append(j[1])
        c+=1
        if c >= 4:
            c=0

reFact = [sqrt(j*j.conjugate()) for j in appo]
phFact = [(j+j.conjugate())/2 for j in appo]


plt.subplot(212)

plt.plot(fre,reFact)
plt.plot(fre,phFact)







plt.show()