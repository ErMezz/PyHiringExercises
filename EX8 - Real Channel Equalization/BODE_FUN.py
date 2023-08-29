"""
@author: emezmat
"""
import control as ct
import matplotlib.pyplot as plt
from math import pi,log10
from skrf import Network
from CTLE_Class import CTLE


ring_slot = Network('tx_test_ficture.s4p')
ring_slot.renumber([0, 1, 2, 3], [0, 2, 1, 3])  # pair ports as 1,3 and 2,4 to match experimental setup
ring_slot.se2gmm(p=2)
orig = ring_slot.s

filt = CTLE()

def MakeBode(freqs,discrH):
    bode = [abs(discrH[p][1][0]) for p in range(len(freqs))]
    return freqs,[20*log10(magg/max(bode)) for magg in bode]
    

def main():
    ticks =[]
    for j in range(1,filt.MaxPeaking()+1):
        pk = 0.5 + j/2
        filt.SetPeaking(pk)
        H = filt.H
        t = [100e6 + i * 100e6 for i in range(0,400)]
        ring_slot.s = orig
        for i in range(0,len(ring_slot.f)):
            if j != 0: ring_slot.s[i][1][0] = 1 * H(1j*ring_slot.f[i]*pi*2)
    
        x,y = MakeBode(ring_slot.f,ring_slot.s)
        plt.xscale("log")
        plt.plot(x, y, label = f'{j/2+0.5}')
        plt.show()
        
    plt.legend()
    plt.grid(True,'both')
