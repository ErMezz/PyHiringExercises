"""
@author: emezmat
"""
from math import pi,log10
import control as ct
import numpy as np

# Class to emulate the CTLE filter using Control library and provided data
class CTLE():

    Garr = [0.891251,0.841395,0.794328,0.749894,0.707946,0.668344,0.630957,0.595662,0.562341,0.530884,0.501187,0.473151,0.446684,0.421697,0.398107,0.375837,0.354813]
    P1,P2 = 26.5625*pi*2*1e9,14.1*pi*2*1e9
    Z1arr = [9.463748,9.248465,9.069645,8.640319,8.255665,7.906766,7.58765,7.076858,6.614781,6.193091,5.805801,5.448395,5.117337,4.809777,4.523367,4.256129,4.006377]
    Plf = 1.2*2*pi*1e9
    Zlfarr = [1.2,1.15,1.1,1.075,1.05,1.025,1,1,1,1,1,1,1,1,1,1,1]

    def __init__(self,peaking=1):
        pkn = int((peaking-0.5)*2)-1
        if pkn < 0: pkn = 0
        elif pkn >= len(self.Garr): pkn = len(self.Garr)-1
        self.pk = peaking
        G = self.Garr[pkn]
        Z1 = self.Z1arr[pkn]*2*pi*1e9
        Zlf = self.Zlfarr[pkn]*2*pi*1e9
        MG = (G*self.P1*self.P2*self.Plf) / (Z1*Zlf)
        num = np.array([MG,MG * (Z1+Zlf), MG * Z1 * Zlf])
        den = np.array([1,self.P1+self.P2+self.Plf,self.P1*self.P2 + self.P2*self.Plf + self.P1*self.Plf , self.P1*self.P2*self.Plf])
        self.H = ct.tf(num,den)
        
    def SetPeaking(self,peaking=1):
        self.__init__(peaking)
        
    def H(self,s):
        return self.H(s)
    
    def Bode(self):
        mag, ph, omega = ct.bode_plot(self.H,dB=False ,Hz = True, plot = False)
        mag2 = mag.tolist()
        maxmag = max(mag2)
        x = omega / (2*pi)
        y = [20*log10(magg/maxmag) for magg in mag]
        return x,y
    
    def MaxPeaking(self):
        return len(self.Garr)