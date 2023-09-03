import warnings
import numpy as np
import matplotlib.pyplot as plt
from math import pi,floor
from skrf import Network
from CTLE_Class import CTLE
import control as ct


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

j=3
filt = CTLE()
pk = 0.5 + j/2
filt.SetPeaking(pk)
H = filt.H
dH = ring_slot.s[:,0,1]

tt,yy = ring_slot.impulse_response()
a,b = ct.forced_response(H,tt,yy[:,0,1])
plt.plot(a,b)
# plt.plot(np.convolve(y[:,0,1],b,'valid')/5e11)

dH = ring_slot.s[:,0,1]
# Calculate discrete H function applying filter
for i in range(0,len(ring_slot.f)):
    if j != 0: ring_slot.s[i,0,1] = dH[i] * H(1j*ring_slot.f[i]*pi*2)

t,y = ring_slot.impulse_response()
plt.plot(t,y[:,0,1])