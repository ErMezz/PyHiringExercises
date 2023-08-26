# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 11:01:03 2023

@author: emezmat
"""

import skrf as rf
import matplotlib.pyplot as plt
from skrf import Network, Frequency
from math import sin
import numpy as np

# %matplotlib qt

ring_slot = Network('tx_test_ficture.s4p')

ring_slot.renumber([0, 1, 2, 3], [0, 2, 1, 3])  # pair ports as 1,3 and 2,4 to match experimental setup

ring_slot.se2gmm(p=2)

tim = [i/(1000*10*1e9) for i in range(0,100000)]
fun = [sin(ttim*2*3.14*10*1e9) for ttim in tim]

# t,y = ring_slot.impulse_response()

# z = y[:,0,1]

# plt.plot(t,z)


# plt.plot(tim,fun)

rf.stylely()
# ring_slot.plot_s_smith()

# plt.title('Ring Slot $S_{21}$')

# for i in range(1,5):
#     for j in range(1,5):
#         if i != j:
#             exec(f"ring_slot.s{i}{j}.plot_s_db(label='S{i}{j}')")

ring_slot.s12.plot_s_db(label='Full Band Response')
ring_slot.s12['2-3ghz'].plot_s_db(lw=3,label='Band of Interest')

plt.show()