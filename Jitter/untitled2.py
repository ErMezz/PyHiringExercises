# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 09:34:21 2023

@author: emezmat
"""

from math import sin
from math import pi
import matplotlib.pyplot as plt
import scipy


def ZeroSrc(func,first_points = [0.4,0.6], target = 0,prec = 0.001):
    x0,x1=first_points
    while 1:
        y0,y1 = func(x0),func(x1)
        if y0 * y1 >= 0:
            print('Fail')
            return None
        x2 = (x0+x1)/2
        y2 = func(x2)
        delta = y2 - target
        if abs(delta) < prec:
            break
        if (y0-target) * (y2-target) < 0: x1 = x2
        else: x0 = x2
    return x2


fu = lambda A,x: A*sin(x)

f = 1e8
fn = 1e6

w = 2*pi*f
wn = 2*pi*fn

Amp = 100
AmpN = 1

t = [i/(100*f) for i in range(-50000,50000)]
y = [fu(Amp,tt*w) for tt in t]
yn = [fu(AmpN,tt*wn) for tt in t]
# yt = [y[i] + yn[i] for i in range(0,len(t))]
yt = [fu(10000,w*tt+fu(0.001,wn*tt)) for tt in t]

newDat = [[]]
lol = []
i=0
for dat in yt:
    lol.append(dat)
    i+=1
    if i>99:
        i=0
        newDat.append(lol)
        lol = []


plt.figure(1)
plt.subplot(311)
plt.plot(t,y)
plt.plot(t,yn)

plt.subplot(312)
# i=0
# for datum in newDat:
#     try:
#         print(datum)
#         plt.plot([i/len(datum) for i in range(0,len(datum))],datum)
#     except:
#         pass

zeros = []
for bo in newDat:
    try:
        x,y = [i/(len(bo)) for i in range(0,len(bo))],bo
        fit = scipy.interpolate.UnivariateSpline(x,y)
        zer = ZeroSrc(fit)
        zeros.append(zer)
        # x.append(zer)
        # y.append(fit(zer))
            
        plt.plot(x,y, c='b',alpha = 0.07)
    except:
        pass

remo = []
for i in range(0,len(zeros)):
    if zeros[i] == None:
        remo.append(i)
count = 0
for i in remo:
    zeros.pop(i-count)
    count += 1
     
plt.subplot(313)

plt.hist(zeros, bins=100)


plt.show()