# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 11:01:03 2023

@author: emezmat
"""

import skrf as rf
import matplotlib.pyplot as plt
from skrf import Network, Frequency

ring_slot = Network('tx_test_ficture.s4p')

rf.stylely()
# ring_slot.plot_s_smith()

plt.title('Ring Slot $S_{21}$')

for i in range(1,5):
    for j in range(1,5):
        if i == j:
            exec(f"ring_slot.s{i}{j}.plot_s_db(label='S{i}{j}')")

# ring_slot.s44.plot_s_db(label='Full Band Response')
# ring_slot.s11['2-3ghz'].plot_s_db(lw=3,label='Band of Interest')