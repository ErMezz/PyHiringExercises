import control as ct
import numpy as np
import matplotlib.pyplot as plt
from math import pi
from math import cos
from math import sin

#%matplotlib qt

plt.figure(1)
plt.subplot(311)

G = 0.9
P1,P2 = 26.5625*pi*2,14.1*pi*2
Z1 = 9.4*2*pi
Plf,Zlf = 1.2*2*pi,1.2*2*pi

MG = (G*P1*P2*Plf) / (Z1*Zlf)

f = 10
freq = 10 * 2 * pi
w = 2*pi*f
num = np.array([MG,MG * (Z1+Zlf), MG])
den = np.array([1,P1+P2+Plf,P1*P2 + P2*Plf + P1*Plf , P1*P2*Plf])
H = ct.tf(num , den)
print (H)
t = [i/100 for i in range(-5000,5000)]
y = np.random.normal(loc = 0, scale = 1, size = 10000)
# plt.plot(t,y)

# tt, yy = ct.forced_response(H,t,y)
t,y = ct.impulse_response(H)
plt.plot(t,y)

# plt.plot(tt,yy)

plt.subplot(312)

plt.plot(np.fft.fftfreq(len(t),d=0.01),np.fft.fft(y))

plt.subplot(313)

plt.plot(np.fft.fftfreq(len(tt),d=0.01),np.fft.fft(yy))



plt.show()