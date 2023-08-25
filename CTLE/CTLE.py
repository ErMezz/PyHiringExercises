import control as ct
import numpy as np
import matplotlib.pyplot as plt
from math import pi,floor
from PRBS import PRBS_seq
#%matplotlib qt
import pandas as pd
import scipy as sp
from skrf import Network


sigFreq = 1.5*26.5625*1e9
sampling = 10*sigFreq
# a = PRBS_seq([13,12,2,1])
a = PRBS_seq([11,9])
t2,y2 = a.GenerateSampledSequence(True,sigFreq,sampling,0.4)
# plt.plot(t2,y2)

w = 2*pi*10*1e9
num = np.array([1])
den = np.array([1/(w*w),2*0.68/w , 1])
H = ct.tf(num , den)



ring_slot = Network('tx_test_ficture.s4p')

ring_slot.renumber([0, 1, 2, 3], [0, 2, 1, 3])  # pair ports as 1,3 and 2,4 to match experimental setup

ring_slot.se2gmm(p=2)



orig = ring_slot.s


Garr = [0,0.891251,0.841395,0.794328,0.749894,0.707946,0.668344,0.630957,0.595662,0.562341,0.530884,0.501187,0.473151,0.446684,0.421697,0.398107,0.375837,0.354813]
P1,P2 = 26.5625*pi*2*1e9,14.1*pi*2*1e9
Z1arr = [1,9.463748*2*pi,9.248465*2*pi,9.069645*2*pi,8.640319*2*pi,8.255665*2*pi,7.906766*2*pi,7.58765*2*pi,7.076858*2*pi,6.614781*2*pi,6.193091*2*pi,5.805801*2*pi,5.448395*2*pi,5.117337*2*pi,4.809777*2*pi,4.523367*2*pi,4.256129*2*pi,4.006377*2*pi]
Plf = 1.2*2*pi*1e9
Zlfarr = [1,1.2*2*pi,1.15*2*pi,1.1*2*pi,1.075*2*pi,1.05*2*pi,1.025*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi,1*2*pi]

t,y = ring_slot.impulse_response()

z = y[:,1,0]

# plt.plot(t,z)

# for j in range(len(Garr)):
for j in [0,15]:
    plt.figure(j)
    G = Garr[j]
    Z1 = Z1arr[j]*1e9
    Zlf = Zlfarr[j]*1e9
    MG = (G*P1*P2*Plf) / (Z1*Zlf)
    # MG=1

    num = np.array([MG,MG * (Z1+Zlf), MG * Z1 * Zlf])
    den = np.array([1,P1+P2+Plf,P1*P2 + P2*Plf + P1*Plf , P1*P2*Plf])
    if j==0: H = ct.tf([1],[1])
    else: H = ct.tf(num , den)

    print(H)

    ring_slot.s = orig

    for i in range(0,len(ring_slot.f)):
        ring_slot.s[i][1][0] = ring_slot.s[i][1][0] * H(ring_slot.f[i]*pi)
        # ring_slot.s[i][1][0] = H(ring_slot.f[i]*2*pi)
        # ring_slot.s[i][1][0] = 1
        pass
    
    t,y = ring_slot.impulse_response(n= floor((1e-7)*sampling),pad=10000)
    z = y[:,1,0]
    
    convo = np.convolve(y2,z,'valid')

    nconvo = convo[1000:300000]
    rot = 2
    nconvo = np.append(nconvo[rot:],nconvo[:rot])
    lol,newDat = [],[]
    for dat in nconvo:
        lol.append(dat)
        i+=1
        if i>=1*sampling/sigFreq:
            i=0
            newDat.append(lol)
            lol = []
            
    eEyeT = np.linspace(0, 1, floor(sampling/sigFreq))
            
    newDat = newDat[10:2000]

    
    newt =[jj/(6*1e10) for jj in range(len(convo))]
    plt.subplot(211)
    for bro in newDat:
        plt.plot(eEyeT,bro,'b',alpha = 0.05)
    plt.subplot(212)
    plt.plot(nconvo)
    # plt.plot(ring_slot.f,ring_slot.s[:,1,0])
    # plt.plot(t,y[:,1,0])


plt.show()