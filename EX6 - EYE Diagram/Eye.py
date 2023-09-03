"""
@author: ErMezz
"""

import json
from matplotlib import patches,pyplot as plt
import scipy
from statistics import mean
from math import floor


def ZeroSrc(fitFunc,first_points = [0.4,0.6], target = 0,prec = 0.001):
    x0,x1=first_points
    while 1:
        y0,y1 = fitFunc(x0)-target,fitFunc(x1)-target
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

if __name__ == "__main__":
    plt.style.use('bmh')

    # Read the .json file
    f = open('Trace_Y_After_FIR.json')
    data = json.load(f)['Trace_Y_After_FIR']
    pps = 20 # Samples per UI
    
    # Plot the original data, plus a zoomed in sample of the first 100 symbols
    fig1 = plt.figure(1,figsize=(12, 8))
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()

    ax = [fig1.add_subplot(2,3,pl) for pl in range(1,7)]
    ax[0].plot(data)
    ax[3].plot(data[0:100*pps])
   
    newDat = []
    i=0
    # Use first crossing to set position for eyes
    for i in range(0,len(data)):
        if data[i]*data[i+1] < 0:
            data = data[i + floor(pps/2 + 0.51):]
            break
    
    Supp = []
    i,j=0,0
    # Resample the data in a list of list. Each of the sublists contains data 
    # relative to 2 UIs in order to draw the eye diagram
    for j in range(0,len(data)):
        Supp.append(data[j])
        i+=1
        if i>2*pps-1:
            Supp.append(data[j+1]) 
            Supp.append(data[j+2]) # Appends two point more / eye for better visualization
            newDat.append(Supp)
            i,Supp=0,[]
    
    
    # Prepare lists for the crossing points
    zeros1,zval1 = [],[]    
    zeros2,zval2 = [],[]    
    # Set the x axis limits
    ax[1].set_xlim([0,2])
    ax[2].set_xlim([0,1])
    ax[4].set_xlim([0,2])
    ax[5].set_xlim([0,1])
    # Prepares a normalized, 2 UI long x axis. Sets the middle point between
    # crossing points as the 0, assuming constant sample rate
    x = [i/(pps) - ((pps+1)%2)*(0.5/pps) for i in range(0,2*pps+2)]
    for eye in newDat:
        y = eye
        if y[0]*y[pps] < 0:
            # Prepare the fit function with a spline, find the zero and plot the data
            fit = scipy.interpolate.UnivariateSpline(x[0:pps],y[0:pps],k=5,s=1)
            zer = ZeroSrc(fit)
            zeros1.append(zer)
            zval1.append(fit(zer))
        if y[pps]*y[-1] < 0:
            fit = scipy.interpolate.UnivariateSpline(x[pps:-1],y[pps:-1],k=5,s=1)
            zer = ZeroSrc(fit,[1.1,1.8])
            zeros2.append(zer)
            zval2.append(fit(zer))
        ax[1].plot(x,y, c='b',alpha = 0.07)
    
    # Plot the fit values at the two crossing points
    ax[1].plot(zeros1,zval1,'o', color='g',alpha = 0.07)
    ax[1].plot(zeros2,zval2,'o', color='g',alpha = 0.07)
    # Plot their hystograms
    ax[4].hist(zeros1, bins=50, color='g')
    ax[4].hist(zeros2, bins=50, color='g')
    
    # Plots a 1 UI long eye plot using previous data
    x = [i/(pps) - ((pps+1)%2)*(0.5/pps) for i in range(0,pps+2)]
    for ee in range(len(newDat)-1):
        ax[2].plot(x,newDat[ee][:len(x)], c='b',alpha = 0.07)
        ax[2].plot(x,newDat[ee][len(x)-2:], c='b',alpha = 0.07)
        
    # Plots the zeros
    zeros3 = zeros1 + [zero2-1 for zero2 in zeros2]
    ax[2].plot(zeros3,zval1+zval2,'o', color='g',alpha = 0.07)

    # And plots the histogram
    ax[5].hist(zeros3, bins=50, color='r')

    # Set all plots' name
    titles = ["Raw data","Eye diagram","Crossing point","First 100 symbols","Two crossing points data","Single crossing point data"]
    for name in enumerate(titles): ax[name[0]].set_title(name[1])
    ylab = ["Voltage [V]","Voltage [V]","Voltage [V]","Voltage [V]","Samples [n]","Samples [n]"]
    for name in enumerate(ylab): ax[name[0]].set_ylabel(name[1])
    xlab = ["Sample index [n]","Time [UI]","Time [UI]","Sample index [n]","Time [UI]","Time [UI]"]
    for name in enumerate(xlab): ax[name[0]].set_xlabel(name[1])

    # Calculating and visualizing mean and variance
    m = round(mean(zeros3),7)
    var = round(mean([zero**2 for zero in zeros3]) - mean(zeros3)**2,7)
    lims = [ax[5].get_xlim(),ax[5].get_ylim()]
    xpos = lims[0][0]+(lims[0][1]-lims[0][0])*6/10
    ypos = lims[1][0]+(lims[1][1]-lims[1][0])*9/10
    xh = (lims[0][1]-lims[0][0])*4/10
    yh = (lims[1][1]-lims[1][0])*1/10
    rectangle = patches.Rectangle((xpos,ypos), xh, yh, edgecolor='black',facecolor="white",zorder=2)
    ax[5].add_patch(rectangle)
    rx, ry = rectangle.get_xy()
    cx = rx + rectangle.get_width()/2.0
    cy = ry + rectangle.get_height()/2.0
    ax[5].annotate(f"Average = {m} UI\nVariance = {var} UI$^2$", (cx, cy), color='black', fontsize=6, ha='center', va='center')
    plt.tight_layout()
    fig1.savefig('EYE_data.png')
    print("Figure saved as EYE_data.png")

    plt.show()

