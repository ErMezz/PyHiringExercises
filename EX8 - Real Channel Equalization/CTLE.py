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

# Finds PAM4 eye height
def EyeSrc(Eyes,xscale):
    """
    

    Parameters
    ----------
    Eyes : list of lists
        A list containing a list of 1 UI long signals.
    xscale : list
        X scale in seconds.

    Returns
    -------
    eye_h : list of tuples
        Used to construct vertical lines. Format: ([freq,freq],[(y1,y2,abs(y1-y2))]).

    """
    # Rotate Eyes to obtain a list of lists containing all points in ascending order, per time
    by_t = [[] for p in range(len(xscale))]
    for datum in Eyes:
        for et in range(len(xscale)-1):
            by_t[et].append(datum[et])
    heights = []
    # Calculates the eyes height by finding maximum gap between points of eye
    for et in range(len(xscale)-1):
        diff_arr = []
        by_t[et].sort(reverse = True)
        for dat in range(len(by_t[et])-1):
            diff_arr.append((by_t[et][dat], by_t[et][dat+1], by_t[et][dat] - by_t[et][dat+1]))
            diff_arr.sort(reverse = True,key=lambda x: x[2])
        heights.append(diff_arr[:3])
    # Rearranges and return data
    eye_h = []
    srcarr = [dat[0][2] for dat in heights]
    eye_p = srcarr.index(max(srcarr))
    eye_h = (([xscale[eye_p],xscale[eye_p]] , heights[eye_p]))
    return eye_h

# Setting some plt parameters
plt.style.use('seaborn-v0_8-dark-palette')
plt.rcParams["font.family"] = "Arial"

warnings.filterwarnings('ignore')

# Generating signal
sigFreq = 1*26.5625*1e9
sampling = 10*sigFreq
a = PRBS_seq([13,12,2,1]) # PRBS13Q
t2,y2 = a.GenerateSampledSequence(True,sigFreq,sampling,0.4)
# Uploads channel using skrf
ring_slot = Network('tx_test_ficture.s4p')
ring_slot.renumber([0, 1, 2, 3], [0, 2, 1, 3])  # pair ports as 1,3 and 2,4 to match experimental setup
ring_slot.se2gmm(p=2)
# Reduce to two port network, considering only differential mode terms
news,newz = [],[]
for fr in range(len(ring_slot.f)):
    app = []
    for param in ring_slot.s[fr][:2]:
        app.append(param[:2].tolist())
    newz.append(ring_slot.z0[fr][:2].tolist())
    news.append(app)
ring_slot = Network(f=ring_slot.f/1e9,s=news,z0=newz)
ring_slot.frequency.uniy = 'MHz'
orig = ring_slot.s # Saves data for later

# Creates filter class instance
filt = CTLE()

# Prepare plots
ax = [[] for n in range(19)]
axb = [[] for n in range(19)]

fig1 = plt.figure(1,figsize = (16,8))
for axi in range(1,4):
    for axj in range(1,7):
        ax[6*(axi-1)+axj] = fig1.add_subplot(3,6,6*(axi-1)+axj)
       
fig2 = plt.figure(2,figsize = (16,8))
for axi in range(1,4):
    for axj in range(1,7):
        axb[6*(axi-1)+axj] = fig2.add_subplot(3,6,6*(axi-1)+axj)

fig1.subplots_adjust(top=0.91, left=0.02, right=0.98)
fig2.subplots_adjust(top=0.91, left=0.02, right=0.98)

# Main cycle
for j in range(0,filt.MaxPeaking()+1):
# for j in range(0,3):
    print(j)
    # Create CTLE filter
    pk = 0.5 + j/2
    filt.SetPeaking(pk)
    H = filt.H
    ring_slot.s = orig
    # Calculate discrete H function applying filter and use it as s-params
    # since when load is equal to system Z0, Sxy(f) = Vy(f)/Vx(f)
    for i in range(0,len(ring_slot.f)):
        if j != 0: ring_slot.s[i,0,1] = ring_slot.s[i,0,1] * H(1j*ring_slot.f[i]*pi*2)
    
    # Calculate impulse response. Pad a bit for improved IFFT and generating enough point for convolution
    t,y = ring_slot.impulse_response(n= floor((sampling / (ring_slot.f[1] - ring_slot.f[0]))),pad=10000)
    # Select channel of interest (port 1 to port 2)
    z = y[:,0,1]
    
    # Convolve sampled PRBS signal and impulse response
    convo = np.convolve(y2,z,'valid')

    # Remove some points for better binning
    nconvo = convo[1000:-1000]
    
    # Rotate a bit for visualization
    rot = 2
    nconvo = np.append(nconvo[rot:],nconvo[:rot])
    
    # Prepare eye diagram and x scale
    eEyeT = np.linspace(0, 1, floor(sampling/sigFreq))
    lol,newDat = [],[]
    for dat in nconvo:
        lol.append(dat)
        i+=1
        if i>=sampling/sigFreq:
            i=0
            newDat.append(lol)
            lol = []
            
    # Remove some more points for better looking graphs and possible tails
    newDat = newDat[50:-50]
    
    # Search for eyes heights
    eye_h = EyeSrc(newDat,eEyeT)
    
    # Prepare and plot eye diagrams
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
    
    # Prepare and plot bode diagrams
    x,y = MakeBode(ring_slot.f,ring_slot.s[:,0,1])
    axb[j+1].set_xscale("log")
    axb[j+1].grid(True)
    axb[j+1].set_xticks([1e-2,1e-1,1,1e1])
    axb[j+1].set_xlabel("GHz")
    st = f'{j/2+0.5}'
    axb[j+1].plot(x/1e9, y, label = st)
    vert = [-50, 10]
    axb[j+1].axvline(sigFreq/(2*1e9), color = 'r', linewidth = 0.5, linestyle = '--')

# Save figures
fig1.tight_layout()
fig2.tight_layout()
fig1.savefig('Simulated_Signals.png')
fig2.savefig('Bode_Plots.png')

# Show figures
plt.show()
