# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 09:08:28 2023

@author: emezmat
"""
from functools import reduce

class PRBS_seq():
    def __init__(self,taps = [13,12,2,1],start_val=1):
        """
        

        Parameters
        ----------
        taps : List, optional
            Define the monic polynomial used for generation in a list format.
            The list shall contain the exponent of non-zero terms. 
            The x^0 term is equal to start_val.
            The default is PRBS13 [13,12,2,1].
        start_val : 0 or 1, optional
            x^0 term. The default is 1.
        
        
        Returns
        -------
        None.

        """
        self.taps = taps
        self.startVal = start_val if start_val == 0 or start_val == 1 else 1
        
    def PrintPol(self):
        """
        Prints the monic polynomial.

        Returns
        -------
        None.

        """
        st = "Pol = "
        for t in self.taps:
            st += f'x^{t} + '
        if self.startVal:
            st += ' 1'
        else:
            st = st[:-2]
        print(st)
        
    def GenSequence(self,PAM4 = True):
        """
        

        Parameters
        ----------
        PAM4 : Bool, optional
            Generate a PAM4 sequence (PRBSQ). The default is True.

        Returns
        -------
        seq : list
            Returns the sequence as a list of 0,1 (NRZ) or 0,1,2,3 values (PAM4)

        """
        
        mask = pow(2,max(self.taps))-1
        curr = self.startVal
        i=0
        seq = [1]
        fexp=lambda x,y: x^y
        
        #Main cycle. Calcolo nuovo bit, lo inserisco in sequenza mascherata di lunghezza 2^max(tap)-1 per verificare se è ripetuta
        while (1):      
            newbit = reduce(fexp, [(curr & 1<<(tap-1))>>tap-1 for tap in self.taps] )  
            seq.append(newbit)
            curr = (curr << 1) | newbit
            curr = curr & mask
            i+=1
            if curr == self.startVal:
                seq.pop(len(seq)-1)
                break
        
        #Passo a PRBSQ per il PAM4
        if PAM4: 
            seq = seq + seq
            oseq = []
            i=0
            while i < len(seq)-1:
                oseq.append(((seq[i])<<1)+seq[i+1])
                i+=2
            seq = oseq
        
        #Restituisco la sequenza come lista di valori
        return seq
    
    
    def SampleSequence(self,b_seq,sig_freq,sample_freq,Vpeak,PAM4):
        """
        

        Parameters
        ----------
        b_seq : list
            The sequence to sample.
        sig_freq : float
            Frequency of the generated signal
        sample_freq : float
            Sampling frequency. Will use 2*sig_freq if sample_freq is lower
        Vpeak : float
            Maximum voltage of the signal. Signal is purely differential.
        PAM4 : bool
            Type of the sequence, NRZ or PAM4.

        Returns
        -------
        timestamps : list of floats
            List of x-axis sampling points in seconds
        sampled_seq : list of floats
            List of y-axis values of the sampled signal

        """
        
        sample_freq = sample_freq if sample_freq > 2*sig_freq else 2*sig_freq + 1
        sig_t = 1/sig_freq
        sam_t = 1/sample_freq
        seq = []
        ts = []
        t=0
        # Inserisco valori di peak e genero timestamp
        for i in b_seq:
            if PAM4: seq.append(round(((i-1.5)*Vpeak)/1.5,3))
            else: seq.append(round(((i-0.5)*Vpeak)/0.5,3))
            ts.append(t*sig_t)
            t+=1
        sampled_seq = []
        actT = 0
        res = 0
        timestamps = []
        # Campiono la sequenza originale
        while actT < ts[-1]:
            while actT >= ts[res+1]: res+=1
            sampled_seq.append(seq[res])
            timestamps.append(actT)
            actT += sam_t
        return timestamps,sampled_seq
    
    def GenerateSampledSequence(self,PAM4,sig_freq,sample_freq,Vpeak):
        """
        

        Parameters
        ----------
        PAM4 : bool
            Type of the sequence, NRZ or PAM4.
        sig_freq : float
            Frequency of the generated signal
        sample_freq : float
            Sampling frequency. Will use 2*sig_freq if sample_freq is lower
        Vpeak : float
            Maximum voltage of the signal. Signal is purely differential.

        Returns
        -------
        timestamps : list of floats
            List of x-axis sampling points in seconds
        sampled_seq : list of floats
            List of y-axis values of the sampled signal

        """
        return(self.SampleSequence(self.GenSequence(PAM4), sig_freq, sample_freq, Vpeak, PAM4))

        
