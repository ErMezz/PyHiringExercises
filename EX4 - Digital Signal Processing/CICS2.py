# A simple script to help me understand CIC filters.
# The decimation rate and stages are selectable.
#
# George Smart, M1GEO. 16 August 2019.
# Downloaded from https://github.com/m1geo/CIC-Filter

class integrator:
    def __init__(self):
        self.yn  = 0
        self.ynm = 0
    
    def update(self, inp):
        self.ynm = self.yn
        self.yn  = (self.ynm + inp)
        return (self.yn)
        
class comb:
    def __init__(self):
        self.xn  = 0
        self.xnm = 0
    
    def update(self, inp):
        self.xnm = self.xn
        self.xn  = inp
        return (self.xn - self.xnm)
    
class CIC:
    def __init__(self,decim,order):
        self.integ = [integrator()]*order
        self.comb = [comb()]*order
        self.data,self.count = 0,decim-1
        self.decim = decim
    
    def update(self,inp):
        self.data = inp
        for integ in self.integ:
            self.data = integ.update(self.data)
        self.count += 1
        if self.count % self.decim == 0:
            self.count = 0
            for comb in self.comb:
                self.data = comb.update(self.data)
            return self.data
        else: return False

class InCIC:
    def __init__(self,decim,order):
        self.integ = [integrator()]*order
        self.comb = [comb()]*order
        self.data = 0
        self.decim = decim
    
    def update(self,inp):
        self.data = inp
        for comb in self.comb:
            self.data = comb.update(self.data)
        newseq = [self.data] + [0]*(self.decim-1)
        print(newseq)

        for seq in range(len(newseq)):
            self.data = newseq[seq]
            for integ in self.integ:
                self.data = integ.update(self.data)
            newseq[seq] = self.data
        return newseq
    
## If this code is run (as opposted to called as a class)
if __name__ == "__main__":
    import time
    import random
    import math
    import matplotlib.pyplot as plt
    import numpy as np
    np.random.seed(0xBABECAFE)
    
    print("\n\nSimple CIC decimating filter demonstation")
    print(" Written in Python3. George Smart, M1GEO ")
    print("george-smart.co.uk       github.com/m1geo\n\n")

    ## Configuration
    samples            = 50000+1    # extra one to ensure the combs run on the final iteration.
    decimation         = 25         # any integer; powers of 2 work best.
    stages             = 1            # pipelined I and C stages

    ## Function to generate an input sample
    def inp_samp(x):
        z = 1 * random.randint(-10000,10000)/10000 # noise
        z += 1 * np.sin(2 * np.pi * 39500 * x)
        z += 1 * np.sin(2 * np.pi * 39000 * x)
        z += 1 * np.sin(2 * np.pi * 41000 * x)
        z += 100 * np.sin(2 * np.pi * 40000 * x)
        return z
    
    ## Calculate normalising gain
    gain = (decimation * 1) ** stages

    ## Seperate Stages - these should be the same unless you specifically want otherwise.
    c_stages = stages
    i_stages = stages

    ## Generate Input/Output Vectors
    print("Generating input vector... ", end="")
    input_samples    = [inp_samp(a/5000) for a in range(samples)]
    output_samples   = []
    print("Done")
    
    input_samples_Q = [input_samples[i] * math.sin(2 * np.pi * 40000 * i/5000) for i in range(len(input_samples))]
    input_samples_P = [input_samples[i] * math.cos(2 * np.pi * 40000 * i/5000) for i in range(len(input_samples))]

    ## Generate Integrator and Comb lists (Python list of objects)
    intes = [integrator() for a in range(i_stages)]
    combs = [comb()          for a in range(c_stages)]

    CICS =  CIC(decimation,stages)

    rebuild_Q = []
    
    for (s, v) in enumerate(input_samples_Q):
        z = CICS.update(v)
        if z != False: rebuild_Q.append(z/gain)

    rebuild_P = []

    for (s, v) in enumerate(input_samples_P):
        z = CICS.update(v)
        if z != False: rebuild_P.append(z/gain)
    
    trebuild = []
                
    ## Crude function to FFT and slice data, with 20log10 result
    def fft_this(data):
        N = len(data)
        return (20*np.log10(np.abs(np.fft.fft(data)) / N)[:N // 2])

    ## Plot some graphs
    print("Preparing graphs... ", end="")
    plt.figure(1)
    plt.suptitle("Simple Test of Decimating CIC filter")
    plt.subplot(2,2,1)
    plt.title("Time domain input")
    plt.plot(input_samples_P)

    plt.grid()

    plt.subplot(2,2,3)
    plt.title("Frequency domain input")
    plt.plot(fft_this(input_samples_P))

    plt.grid()

    plt.subplot(2,2,2)
    plt.title("Time domain output")
    plt.plot(rebuild_P)
    plt.grid()

    plt.subplot(2,2,4)
    plt.title("Frequency domain output")
    plt.plot(fft_this(rebuild_P))
    plt.grid()
    print("Done")
    
    ## Try to calculate the frequency rolloff. Just for indication!
    ## These much match signals in the "inp_samp()" function.
    print("")
    fos = fft_this(output_samples)
    try:
        f = 40
        f2 = f * 10
        print("Filtered Output, bin %4d = %f" % (f,  fos[f]))
        print("Filtered Output, bin %4d = %f" % (f2, fos[f2]))
        print("Difference %f in a decade" % (fos[40] - fos[400]))
    except:
        print("*** Error: Cannot FFT bins must be chosen to match decimation and frequencies in the inp_samp() function.")
        pass

    ## Show graphs
    plt.show()