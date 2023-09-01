# Signal generation

import json
import numpy as np
import scipy as sp
from math import pi,sin,cos,e,sqrt
import matplotlib.pyplot as plt
import control as ct

# t = np.linspace(0,1e-4,50000)
# y = [np.random.rand() for tt in t]


# plt.plot(sp.fft.fft(y))
f = open('Trace_Y_After_FIR.json')
y = json.load(f)['Trace_Y_After_FIR']

f = 100*1e6
wm = 2*pi*f
Q = 200

t = np.linspace(0,(len(y)/40)/f,len(y),False)
y = [cos(wm*tt) for tt in t]
# wm = wm - wm/1000
# w = [2*pi*(i)*1e7 for i in range(10000)]
# plt.figure(1)
# ct.bode_plot(H,omega = w)
plt.figure(2)
plt.subplot(311)
plt.plot(t,y)
plt.subplot(313)
zpI = [y[zz] * cos(wm*t[zz]) for zz in range(len(y))]
zmQ = [y[zz] * - sin(wm*t[zz]) for zz in range(len(y))]
wh = wm*0.1
H = ct.tf([wh],[1,wh])
# H = ct.tf([1],[1])

tttp,filpI = ct.forced_response(H,t,zpI)
tttm,filmQ = ct.forced_response(H,t,zmQ)
# plt.plot(np.fft.fftfreq(len(t),d=t[1]-t[0]),abs(sp.fft.fft(y)))
# plt.plot(np.fft.fftfreq(len(filpI),d=tttp[1]-tttp[0]),(sp.fft.fft(filpI).real))
plt.plot(np.fft.fftfreq(len(filmQ),d=tttm[1]-tttm[0]),(sp.fft.fft(filmQ).real))
plt.subplot(312)
plt.plot(t,y)
# plt.plot(t,zp)
# plt.plot(tttp,filp)
# plt.plot(t,zm)
# plt.plot(tttm,film)

newt,newpI,newmQ = [],[],[]
for i in range(len(tttp)):
    if i%100 == 0:
        newt.append(tttp[i])
        newpI.append(filpI[i])
        newmQ.append(filmQ[i])

# plt.plot(newt,newp,'x')
# plt.plot(newt,newm,'x')

# plt.subplot(313)
# plt.plot(np.fft.fftfreq(len(newt),d=newt[1]-newt[0]),sp.fft.fft(newp))
# plt.plot(np.fft.fftfreq(len(newt),d=newt[1]-newt[0]),sp.fft.fft(newm))

zout = [sqrt(newpI[ti]**2 + newmQ[ti]**2) * cos(wm*newt[ti] + np.arctan(newmQ[ti]/newpI[ti])) for ti in range(len(newt))]
plt.plot(newt,zout)

