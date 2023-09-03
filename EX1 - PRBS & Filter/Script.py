"""
@author: ErMezz
"""

import control as ct
import numpy as np
import matplotlib.pyplot as plt
import warnings
from math import pi,floor
from PRBS import PRBS_seq


plt.style.use('seaborn-v0_8-dark-palette')
plt.rcParams["font.family"] = "Serif"

# Generate the PRBS_seq class instance using defaults (PRBS13)
seq = PRBS_seq()
seq.PrintPol()
# Generates and sample the PRBS13 
sigFreq = 10*1e9
sampFreq = 20*sigFreq
t,y = seq.GenerateSampledSequence(True,sigFreq,sampFreq,0.4)

# Generates the low-pass filter using the 'control' package
w = 2*pi*sigFreq
num = np.array([1])
den = np.array([1/(w*w),2*0.68/w , 1])
H = ct.tf(num , den)
print(H)

# Calculates filter response to the signal. 
warnings.filterwarnings('ignore')
tt, yy = ct.forced_response(H,t,y,1e-22)

# Plot and save data
fig = plt.figure(figsize=[9,5])
ax1 = fig.add_subplot(111)
# Calculate number of points to get 100 symbols
sympts = floor(sampFreq / sigFreq) * 100
ax1.set_ylabel('Voltage [V]')
ax1.set_xlabel('Time [ns]', loc = 'center')
ax1.set_title('Original vs Filtered signal, first 100 symbols', loc = 'center')
ax1.plot(np.array(t[:sympts])*1e9,y[:sympts], 'black', label = 'Original', linewidth = 0.5)
ax1.plot(tt[:sympts]*1e9,yy[:sympts], 'darkred', label = 'Filtered', linewidth = 0.7)
plt.legend(loc = 'upper right')
ax1.xaxis.set_ticks(np.linspace(0, int(tt[sympts]*1e9), 11))
ax1.grid(axis = 'x', alpha = 0.8, linestyle = '--')
fig.savefig('Filtered_PRBS13_TimePlot.png', bbox_inches='tight')
# Prevents Spyder from forcefully showing figure because of interactive mode
plt.close(fig)
print('Figure saved as Filtered_PRBS13_TimePlot.png')