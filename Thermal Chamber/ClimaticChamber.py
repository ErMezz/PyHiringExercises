# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

time = 0
integral = 0
time_prev = -1e-6
e_prev = 0

Pi,Ii,Di = [],[0],[0]

# %matplotlib inline

def PID(Kp, Ki, Kd, setpoint, measurement):
    global time, integral, time_prev, e_prev, Pi, Ii, Di

    
    # PID calculations
    e = setpoint - measurement
        
    P = Kp*e
    integral = integral + Ki*e*(time - time_prev)
    D = Kd*(e - e_prev)/(time - time_prev)

    Pi.append(P)
    Ii.append(integral)
    Di.append(D)
    # calculate manipulated variable - MV 
    MV = P + integral + D
    
    # update stored data for next iteration
    e_prev = e
    time_prev = time
    return MV

def CCModel(t,currT,Th):
    
    Qcoeff = 100 # W/m2K Forced heat convection from resistor
    Rarea = 1e-2 # m2 Resitor area
    kflux = Qcoeff * Rarea
    
    Qflux = (Th - currT) / kflux
    
    Vol = 1 #m3 Climatic chamber volume
    Dair = 1.29 # kh/m3 Air density @Patm
    Cair = 1.012*1e3 # J/KgK Specific heat capacity
    Mair = Dair * Vol
    
    dTdt = Qflux / (Mair * Cair)
    return dTdt

# number of steps
n = 36000
time_prev = 0
y0 = 0
deltat = 1
y_sol = [y0]
t_sol = [time_prev]
# Tq is chosen as a manipulated variable

Th = 0,
q_sol = [Th[0]]
setpoint = 100
integral = 0

Pi.append(10)

for i in range(1, n):
    time = i * deltat
    tspan = np.linspace(time_prev, time, 100)
    Th = min(PID(0.1, 0.001, 0, setpoint, y_sol[max(-3,-len(y_sol))]),400),
    yi = sp.integrate.odeint(CCModel,y_sol[-1], tspan, args = Th, tfirst=True)
    t_sol.append(time)
    y_sol.append(yi[-1][0])
    q_sol.append(Th[0])
    time_prev = time

plt.figure(1)
plt.subplot(211)
plt.plot(t_sol, y_sol)
plt.plot(t_sol, q_sol)
plt.subplot(212)
plt.plot(t_sol, Pi)
plt.plot(t_sol, Ii)
plt.plot(t_sol, Di)
plt.xlabel('Time')
plt.ylabel('Temperature')

plt.show()