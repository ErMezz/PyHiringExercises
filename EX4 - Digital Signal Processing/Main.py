# Signal generation

import numpy as np
import scipy as sp
from math import pi,sin
import matplotlib.pyplot as plt
import control as ct

t = np.linspace(0,1e-4,5000)
y = [np.random.rand() for tt in t]


# plt.plot(sp.fft.fft(y))

wm = 100*1e6
Q = 200



H = ct.tf([1e10/4*wm/Q],[1,wm/Q,wm**2])
w = [2*pi*(i)*1e2 for i in range(1000000)]
plt.figure(1)
ct.bode_plot(H,omega = w)
plt.figure(2)
plt.subplot(311)
plt.plot(t,y)
x,z = ct.forced_response(H,t,y)
plt.subplot(312)
plt.plot(x,z)
plt.subplot(313)
# plt.plot(sp.fft.fft(y))
plt.plot(sp.fft.fft(z))
z = [sin(2*pi*1e8*t[zz])*z[zz] for zz in range(len(z))]
plt.plot(sp.fft.fft(z))
plt.subplot(312)
plt.plot(x,z)