"""
@author: ErMezz
"""

import math
from math import sin,pi
import matplotlib.pyplot as plt
import scipy
import numpy as np


def ZeroSrc(func,first_points = [0.4,0.6], target = 0,prec = 0.001):
    x0,x1=first_points
    while 1:
        y0,y1 = func(x0)-target,func(x1)-target
        if y0 * y1 >= 0:
            print('Fail')
            return None
        x2 = (x0+x1)/2
        y2 = func(x2)
        delta = y2 - target
        if abs(delta) < prec:
            break
        if (y0) * (y2-target) < 0: x1 = x2
        else: x0 = x2
    return x2

fu = lambda A,x: A*sin(x)
fuN = lambda A,x: A*sin(x)

f = 1e8
fn = 1e6

w = 2*pi*f
wn = 2*pi*fn

Amp = 1
AmpN = 1

periods = 1000
steps = 20000

t = np.linspace(0, periods/f,steps)
y = [fu(Amp,tt*w) for tt in t]
yt = [fu(Amp,w*tt+fuN(AmpN,wn*tt)) for tt in t]
yn = [fuN(AmpN,tt*wn) for tt in t]


newDat = []
lol = []
i=0
for dat in yt:
    lol.append(dat)
    i+=1
    if i>(steps / periods) - 1:
        i=0
        newDat.append(lol)
        lol = []


plt.figure(1)
plt.subplot(311)
plt.plot(t,yt)
plt.plot(t,yn)

plt.subplot(312)

zeros = []
mini,maxi = [],[]
for dat in newDat:
    try:
        x,y = [i/(len(dat)-1) for i in range(0,len(dat))],dat
        i,j,k = 0,0,0
        found = False
        for yy in y:
            if yy>0.1 and (not found): i,found = k,True
            if yy<-0.1 and found: 
                j = k
                break
            k+=1
        
        if k==len(y):
            found = False
            for yy in y:
                if yy<0.1 and (not found): i,found = k,True
                if yy>-0.1 and found: 
                    j = k
                    break
                k+=1
        mi = x[i]
        ma = x[j]
        mini.append(mi)
        maxi.append(ma)
        fit = scipy.interpolate.UnivariateSpline(x,y,k=5,s=2)
        zeros.append(ZeroSrc(fit,[mi,ma]))
        plt.plot(x,y,alpha = 0.07,label=f'{i}')
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

plt.hist(zeros, density = False, bins=49)
plt.hist

print('PJpp =' + f'{max(zeros)-min(zeros)}')

plt.show()