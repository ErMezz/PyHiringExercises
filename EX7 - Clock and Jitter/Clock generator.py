"""
@author: ErMezz
"""

from math import sin,pi
from matplotlib import pyplot as plt, patches
import scipy
import numpy as np
import sys, os
cdir = (os.getcwd())
dir_c = os.path.dirname(cdir)
sys.path.append(os.path.join(dir_c,'EX6 - EYE Diagram'))
from Eye import ZeroSrc

fig1 = plt.figure(1,figsize=(12, 8))
figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()
ax = [fig1.add_subplot(3,1,pl) for pl in range(1,4)]


# Prepare a simple function for a sinusoidal clock generation
fu = lambda A,x: A*sin(x)

f = 1e8 # Clock frequency
fn = 1e6 # Noise frequency

w = 2*pi*f # Clock angular frequency
wn = 2*pi*fn # Noise angular frequency

Amp = 1 # Clock amplitude
AmpN = 1 # Noise amplitude

periods = 1000 # Full clock periods to sample
steps = 10*periods # Sampling frequency

# Prepare the x axis
t = np.linspace(0, periods/(f),steps,False)

# Generate clock only
y = [fu(Amp,tt*w) for tt in t]
# Generate noise only
yn = [fu(AmpN,tt*wn) for tt in t]
# Generate noisy signal as A*sin(wclock t + B*sin(wnoise t))
yt = [fu(Amp,w*tt+fu(AmpN,wn*tt)) for tt in t]

# Prepare data, similarly to eye diagram, for crossing point study
newDat = []
eye = []
i,j=0,0
for dat in yt:
    eye.append(dat)
    i+=1
    j+=1
    if i>(steps / periods) - 1:
        try:
            i=0
            eye.append(yt[j])
            newDat.append(eye)
            eye = []
        except: pass

# Plot the clock
ax[0].plot(t,yt,label = "Noisy signal")
ax[0].plot(t,yn, label = "Pure noise")
ax[0].set_xlim([0,10/f])
ax[0].legend(loc="upper right")

# Find and plot the crossing points
ax[1].set_xlim([0,1])
x = [i/(len(newDat[0])-1) for i in range(0,len(newDat[0]))]

zeros = []
for dat in newDat:
    y = dat
    i,j,k = 0,0,0
    found = False
    # Checks where to search for the zero
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
    lims = [x[i],x[j]]
    # Leaving some leeway for failure at zero search for high noise levels
    if lims[1]-lims[0] > 0:
        try:
            fit = scipy.interpolate.UnivariateSpline(x,y,k=5,s=2)
            zeros.append(ZeroSrc(fit,lims,prec = 1e-8)/f)
            ax[1].plot(x,y,alpha = 0.07,label=f'{i}',color = 'b')
        except: pass
    
# Plot the crossing point histogram

ax[2].hist(zeros, density = False, bins=29)

# Calculate and visualize the peak-peak periodic jitter from data
PJpp = (max(zeros)-min(zeros))
lims = [plt.xlim(),plt.ylim()]
xpos = lims[0][0]+(lims[0][1]-lims[0][0])*8/10
ypos = lims[1][0]+(lims[1][1]-lims[1][0])*9/10
xh = (lims[0][1]-lims[0][0])*2/10
yh = (lims[1][1]-lims[1][0])*1/10
rectangle = patches.Rectangle((xpos,ypos), xh, yh, edgecolor='black',facecolor="white",zorder=2)
ax[2].add_patch(rectangle)
rx, ry = rectangle.get_xy()
cx = rx + rectangle.get_width()/2.0
cy = ry + rectangle.get_height()/2.0
ax[2].annotate(f"PJpp = {round(PJpp*1e9,3)} ns", (cx, cy), color='black', fontsize=6, ha='center', va='center')
# Set some labels
titles = ["Generated clock, detail","Crossing point study","Crossing point data"]
for name in enumerate(titles): ax[name[0]].set_title(name[1])
ylab = ["Voltage [V]","Voltage [V]","Samples [n]"]
for name in enumerate(ylab): ax[name[0]].set_ylabel(name[1])
xlab = ["Time [s]","Time [UI]","Time [s]"]
for name in enumerate(xlab): ax[name[0]].set_xlabel(name[1])

# Save plots
plt.tight_layout()
fig1.savefig('Clock.png')
print("Figure saved as Clock.png")

# Show plots
plt.show()