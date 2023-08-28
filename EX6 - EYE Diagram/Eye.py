"""
@author: ErMezz
"""

import json
import matplotlib.pyplot as plt
import scipy
from statistics import mean
from math import floor


def ZeroSrc(fitFunc,first_points = [0.4,0.6], target = 0,prec = 0.001):
    x0,x1=first_points
    while 1:
        y0,y1 = fitFunc(x0),fitFunc(x1)
        if y0 * y1 >= 0:
            return None
        x2 = (x0+x1)/2
        y2 = fitFunc(x2)
        delta = y2 - target
        if abs(delta) < prec:
            break
        if (y0-target) * (y2-target) < 0: x1 = x2
        else: x0 = x2
    return x2

def main():
    plt.style.use('bmh')
    
    f = open('Trace_Y_After_FIR.json')
    data = json.load(f)['Trace_Y_After_FIR']
    plt.figure(1)
    plt.subplot(221)
    plt.plot(data)
    plt.subplot(223)
    plt.plot(data[0:2000])
   
    pps = 20
    
    newDat = []
    i=0
    # Use first crossing to set position for eyes
    for i in range(0,len(data)):
        if data[i]*data[i+1] < 0:
            data = data[i + floor(pps/2 + 0.51):]
            break
    
    Supp = []
    i,j=0,0
    for j in range(0,len(data)):
        Supp.append(data[j])
        i+=1
        if i>2*pps-1:
            Supp.append(data[j])
            Supp.append(data[j+1])
            newDat.append(Supp)
            i,Supp=0,[]
    
    zeros1,zval1 = [],[]    
    zeros2,zval2 = [],[]    
    
    plt.subplot(222)
    
    plt.xlim([0,2])
    
    for eye in newDat:
        x,y = [i/(pps) - ((pps+1)%2)*(0.5/pps) for i in range(0,2*pps+2)],eye
        if y[0]*y[pps] < 0:
            fit = scipy.interpolate.UnivariateSpline(x[0:pps],y[0:pps],k=5,s=1)
            zer = ZeroSrc(fit)
            zeros1.append(zer)
            zval1.append(fit(zer))
        if y[pps]*y[-1] < 0:
            fit = scipy.interpolate.UnivariateSpline(x[pps:-1],y[pps:-1],k=5,s=1)
            zer = ZeroSrc(fit,[1.1,1.8])
            zeros2.append(zer)
            zval2.append(fit(zer))
        plt.plot(x,y, c='b',alpha = 0.07)
        
    plt.plot(zeros1,zval1,'o', color='g',alpha = 0.07)
    plt.plot(zeros2,zval2,'o', color='g',alpha = 0.07)
        
    plt.subplot(224)
    
    plt.hist(zeros1, bins=30, color='g')
    plt.hist(zeros2, bins=30, color='g')
    zeros3 = zeros1 + [zero2-1 for zero2 in zeros2]
    plt.hist(zeros3, bins=50, color='r')
    plt.xlim([0,2])
    # m = mean(zeros)
    # var = mean([zero**2 for zero in zeros]) - mean(zeros)**2
    print(zeros1)
    plt.show()

if __name__ == "__main__":
    main()