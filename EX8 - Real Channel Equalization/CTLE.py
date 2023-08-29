"""
@author: ErMezz
"""
import warnings
import numpy as np
import matplotlib.pyplot as plt
import sys, os
cdir = (os.getcwd())
dir_c = os.path.dirname(cdir)
sys.path.append(os.path.join(dir_c,'EX1 - PRBS & Filter'))
from PRBS import PRBS_seq
from math import pi,floor
from skrf import Network
from BODE_FUN import MakeBode
from CTLE_Class import CTLE

def EyeSrc(Eyes,xscale):
    by_t = [[] for p in range(len(xscale))]
    for datum in Eyes:
        for et in range(len(xscale)-1):
            by_t[et].append(datum[et])
    heights = []
    for et in range(len(xscale)-1):
        diff_arr = []
        by_t[et].sort(reverse = True)
        for dat in range(len(by_t[et])-1):
            diff_arr.append((by_t[et][dat], by_t[et][dat+1], by_t[et][dat] - by_t[et][dat+1]))
            diff_arr.sort(reverse = True,key=lambda x: x[2])
        heights.append(diff_arr[:3])
    eye_h = []
    srcarr = [dat[0][2] for dat in heights]
    eye_p = srcarr.index(max(srcarr))
    eye_h = (([xscale[eye_p],xscale[eye_p]] , heights[eye_p]))
    return eye_h


plt.style.use('seaborn-v0_8-dark-palette')
plt.rcParams["font.family"] = "Lato"

warnings.filterwarnings('ignore')

sigFreq = 1*26.5625*1e9
sampling = 10*sigFreq
a = PRBS_seq([13,12,2,1])
t2,y2 = a.GenerateSampledSequence(True,sigFreq,sampling,0.4)

ring_slot = Network('tx_test_ficture.s4p')
ring_slot.renumber([0, 1, 2, 3], [0, 2, 1, 3])  # pair ports as 1,3 and 2,4 to match experimental setup
ring_slot.se2gmm(p=2)

orig = ring_slot.s
filt = CTLE()

ax = [[] for n in range(19)]
axb = [[] for n in range(19)]
fig1 = plt.figure(1)
for axi in range(1,4):
    for axj in range(1,7):
        ax[6*(axi-1)+axj] = fig1.add_subplot(3,6,6*(axi-1)+axj)
        
figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()

fig2 = plt.figure(2)
for axi in range(1,4):
    for axj in range(1,7):
        axb[6*(axi-1)+axj] = fig2.add_subplot(3,6,6*(axi-1)+axj)

figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()

fig1.subplots_adjust(top=0.91, left=0.02, right=0.98)
fig2.subplots_adjust(top=0.91, left=0.02, right=0.98)

for j in range(0,filt.MaxPeaking()+1):
    pk = 0.5 + j/2
    filt.SetPeaking(pk)
    H = filt.H

    print(H)

    ring_slot.s = orig

    for i in range(0,len(ring_slot.f)):
        if j != 0: ring_slot.s[i][1][0] = ring_slot.s[i][1][0] * H(1j*ring_slot.f[i]*pi*2)
    
    t,y = ring_slot.impulse_response(n= floor((sampling / (ring_slot.f[1] - ring_slot.f[0]))),pad=10000)
    z = y[:,1,0]
    
    convo = np.convolve(y2,z,'valid')

    nconvo = convo[1000:-1000]
    rot = 2
    nconvo = np.append(nconvo[rot:],nconvo[:rot])
    
    lol,newDat = [],[]
    for dat in nconvo:
        lol.append(dat)
        i+=1
        if i>=sampling/sigFreq:
            i=0
            newDat.append(lol)
            lol = []
            
    eEyeT = np.linspace(0, 1, floor(sampling/sigFreq))
            
    newDat = newDat[1000:-1000]
    
    eye_h = EyeSrc(newDat,eEyeT)
    if j == 0: ax[1].set_title('Channel signal')
    else: ax[j+1].set_title(f'Peaking = {pk}')
    
    for line in eye_h[1]:
        ax[j+1].plot(eye_h[0],[line[0],line[1]])
        st = f'{round(line[2],3)}'
        ax[j+1].annotate(st, xy = [eye_h[0][0]+0.01, (line[0] + line[1])/2], textcoords='offset points', fontsize = 6, color = 'r')
    
    for graph in newDat:
        ax[j+1].plot(eEyeT,graph,'b',alpha = 0.05)
    
    if j == 0: axb[1].set_title('Channel Bode')
    else: axb[j+1].set_title(f'Peaking = {pk}')

    x,y = MakeBode(ring_slot.f,ring_slot.s)
    plt.xscale("log")
    st = f'{j/2+0.5}'
    axb[j+1].plot(x/1e9, y, label = st)
    vert = [-50, 10]
    axb[j+1].axvline(sigFreq/(2*1e9), color = 'r', linewidth = 0.5, linestyle = '--')

plt.show()