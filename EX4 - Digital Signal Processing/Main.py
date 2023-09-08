from Filter_Classes import CIC,Dig_FIL
from scipy import signal
from math import sin,pi
import matplotlib.pyplot as plt

def Filter_and_Decimate(dat,CIC,COMP,HB_FIR,HB_Samp = True):
    sample,z = CIC.update(dat)
    if sample:
        z = COMP.update(z)
        z = HB_FIR.update(z)
        if HB_Samp: return True,z
        else: return False,0
    else: return False,0
        

# CIC filter
CIC_decimation = 25
order = 1
CIC_Filter = CIC(CIC_decimation,order)

# CIC compensation
a = 0.05
taps = [-a/(1-2*a),1/(1-2*a),-a/(1-2*a)]
COMP_Filter = Dig_FIL(taps)

# Half-band filter, factor 2 decimation
NN=32
bands = [0., .22, .28, .5]
h = signal.remez(NN+1, bands, [1,0], [1,1])
h[abs(h) <= 1e-4] = 0.
TG = sum(h)
FIR_Filter = Dig_FIL(h)

# Example of effect of the filter-decimation with low frequency data
Fs_start = 100*1e6
Fs_end = 2*1e6
samples = 5000
t = [i/(Fs_start) for i in range(samples)]
t_down = [i/(Fs_end) for i in range(samples//50)]
y = [sin(0.2*1e6*2*pi*i) for i in t]

data_down = []
Samp = True
for datum in y:
    get,z = Filter_and_Decimate(datum, CIC_Filter, COMP_Filter, FIR_Filter, Samp)
    if get: data_down.append(z)
    Samp = not Samp


# Plot and save data
plt.figure(figsize=(10,6))
plt.plot(t,y,label = '100MSPS')
plt.plot(t_down,data_down,label = '2MSPS')
plt.title('Filter and decimation effects on 200 KHz sine')
plt.legend(loc = 'upper right')
plt.xlabel('Time [s]')
plt.tight_layout()
plt.savefig('Sample_signal.png')
print('Plot saved as Sample_signal.png')
plt.show()