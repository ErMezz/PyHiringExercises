# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 09:08:28 2023

@author: emezmat
"""
from functools import reduce
import matplotlib.pyplot as plt
import control as ct
import numpy as np
from math import pi

class PRBS_seq():
    def __init__(self,taps = [13,12,2,1],start_val=1):
        self.taps = taps
        self.startVal = start_val
        
    def PrintTaps(self):
        st = "Pol = "
        for t in self.taps:
            st += f'x^{t} + '
        if self.startVal:
            st += ' 1'
        else:
            st = st[:-2]
        print(st)
        
    def GenSequence(self,PAM4 = True):
        mask = pow(2,max(self.taps))-1
        curr = self.startVal
        i=0
        seq = [1]
        fexp=lambda x,y: x^y
        
        #Main cycle. Calcolo nuovo bit, lo inserisco in sequenza mascherata di lunghezza 2^max(tap)-1 per verificare se è ripetuta
        while (1):      
            newbit = reduce(fexp, [(curr & 1<<(tap-1))>>tap-1 for tap in self.taps] )  
            seq.append(newbit)
            curr = (curr << 1) | newbit
            curr = curr & mask
            i+=1
            if curr == self.startVal:
                seq.pop(len(seq)-1)
                break
        
        #Passo a PRBSQ per il PAM4
        if PAM4: 
            seq = seq + seq
            oseq = []
            i=0
            while i < len(seq)-1:
                oseq.append(((seq[i])<<1)+seq[i+1])
                i+=2
            seq = oseq
        
        #Restituisco la sequenza come lista di valori
        return seq
    
    
    def SampleSequence(self,b_seq,sig_freq,sample_freq,Vpeak,PAM4):

        sig_t = 1/sig_freq
        sam_t = 1/sample_freq
        seq = []
        ts = []
        t=0
        # Inserisco valori di peak e genero timestamp
        for i in b_seq:
            if PAM4: seq.append(round(((i-1.5)*Vpeak)/1.5,3))
            else: seq.append(round(((i-0.5)*Vpeak)/0.5,3))
            ts.append(t*sig_t)
            t+=1
        sampled_seq = []
        actT = 0
        res = 0
        timestamps = []
        # Campiono la sequenza originale
        while actT < ts[-1]:
            while actT >= ts[res+1]: res+=1
            sampled_seq.append(seq[res])
            timestamps.append(actT)
            actT += sam_t
        return timestamps,sampled_seq
    
    def GenerateSampledSequence(self,PAM4,sig_freq,sample_freq,Vpeak):
        return(self.SampleSequence(self.GenSequence(PAM4), sig_freq, sample_freq, Vpeak, PAM4))

        

sigFreq = 10*1e9

a = PRBS_seq()
tt,yy = a.GenerateSampledSequence(False,sigFreq,sigFreq*2.5,0.4)

plt.plot(tt[0:100],yy[0:100])


w = 2*pi*10*1e9
num = np.array([1])
den = np.array([1/(w*w),2*0.68/w , 1])
H = ct.tf(num , den)
print (H)
t, y = ct.forced_response(H,tt,yy,1*1e-22)
plt.plot(t[0:100],y[0:100])

plt.show()