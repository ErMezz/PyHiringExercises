import control as ct
import numpy as np
import matplotlib.pyplot as plt
from math import pi
from math import cos
from math import sin

#%matplotlib qt

plt.figure(1)
plt.subplot(221)

f = 10
freq = 10 * 2 * pi
w = 2*pi*f
num = np.array([1])
den = np.array([1/w , 1])
H = ct.tf(num , den)
print (H)
t = [i/100 for i in range(-500,500)]

y = [sin(freq*z+0.000001) for z in t]
plt.plot(t,y)

plt.subplot(223)
plt.plot(np.fft.fftfreq(len(t),d=0.01),np.fft.fft(y))


plt.subplot(222)
y = [cos(freq*z) for z in t]
plt.plot(t,y)

plt.subplot(224)
plt.plot(np.fft.fftfreq(len(t),d=0.01),np.fft.fft(y))

# t, y = ct.forced_response(H,t,y)
# plt.plot(t,y)
# plt.title("Step Response")
plt.show()