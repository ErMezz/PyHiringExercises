"""
@author: emezmat
"""
import matplotlib.pyplot as plt
from CTLE_Class import CTLE


# Draws CTLE a la IEEE 802.3. Used to check if class is implemented correctly

filt = CTLE()

ticks =[]
for j in range(1,filt.MaxPeaking()+1):
    pk = 0.5 + j/2
    filt.SetPeaking(pk)
    H = filt.H
    print(H)
    t = [100e6 + i * 100e6 for i in range(0,400)]
        
    if j == 1: Boss = H(0)
    
    x,y = filt.Bode()
    plt.xscale("log")
    plt.plot(x,y)
    ticks.append(-pk)
plt.legend()
plt.grid(True,'both')
plt.yticks(ticks)