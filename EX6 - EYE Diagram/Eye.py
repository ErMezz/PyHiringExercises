"""
@author: ErMezz
"""

import json
import matplotlib.pyplot as plt
import scipy
from statistics import mean


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
    
    newDat = []
    lol = []
    i=0
    for i in range(len(data)):
        if data[i]*data[i+1] < 0:
            data = data[i+10:]
            print(i)
            break
    i=0
    for dat in data:
        lol.append(dat)
        i+=1
        if i>39:
            i=0
            newDat.append(lol)
            lol = []
    
    zeros,zval = [],[]
    
    
    plt.figure(1)
    plt.subplot(221)
    plt.plot(data)
    plt.subplot(223)
    plt.plot(data[0:2000])
    
    plt.subplot(222)
    
    for bo in newDat:
        try:
            x,y = [i/19 for i in range(0,40)],bo
            # if y[0]*y[39] < 0:
            #     fit = scipy.interpolate.UnivariateSpline(x,y,k=5,s=1)
            #     zer = ZeroSrc(fit)
            #     zeros.append(zer)
            #     zval.append(fit(zer))
            plt.plot(x,y, c='b',alpha = 0.07)
        except:
            pass
        
    plt.plot(zeros,zval,'o', color='g',alpha = 0.07)
        
    plt.subplot(224)
    
    # plt.hist(zeros, bins=50, color='g')
    # m = mean(zeros)
    # var = mean([zero**2 for zero in zeros]) - mean(zeros)**2
    
    plt.show()

if __name__ == "__main__":
    main()