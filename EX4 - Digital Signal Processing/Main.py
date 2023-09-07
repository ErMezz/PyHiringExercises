from CIC_Class import CIC,Dig_FIL
from scipy import signal

# CIC filter
CIC_decimation = 25
order = 1
CIC_filter = CIC(CIC_decimation,order)

# CIC compensation
NN=32
bands = [0., .22, .28, .5]
h = signal.remez(NN+1, bands, [1,0], [1,1])
h[abs(h) <= 1e-4] = 0.
TG = sum(h)
FIR_Filter = Dig_FIL(h)

# Half-band filter
