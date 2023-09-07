"""
@author: ErMezz
"""

import numpy as np
import scipy as sp

class PID():
    lastErr = 0
    integral = 0
    
    def __init__(self,Kp,Ki,Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        
    def Reset(self):
        self.lastErr = 0
        self.integral = 0
    
    def Step(self,err,deltat):
        self.integral += self.Ki * err / deltat
        deriv = self.Kd * (err-self.lastErr) / (deltat)
        self.lastErr = err
        return self.Kp * err + self.integral + deriv
    
    def Simulate_1stDeg(self,start,deltat,steps,sys,start_p,set_p,start_var,var_range = []):
        """
        

        Parameters
        ----------
        start : float
            Start time in s.
        stop : float
            Stop time in s.
        deltat : float
            Number of steps.
        sys : func
            Function describing the system.
            Input format shall be t, y, manupulated var.
        start_p : float
            Start point.
        set_p : float
            Set point.
        start_var : float
            Starting value of the manipulated variable.

        Returns
        -------
        A tuple of lists: (Time,System status, Var status)

        """
        # Reset the PID before starting full simulation
        self.Reset()
        
        # Get first error data
        self.lastErr = set_p - start_p
        
        # Prepare some lists for elaboration
        times = [start]
        var_sol = [start_var,]
        y_sol = [start_p]
        
        # Check if there is a limit on maximum manipulated variable range. If
        # so, prepare some variables to use it
        if len(var_range) == 2: mi,ma,ch = var_range[0],var_range[1],True
        else: mi,ma,ch = 0,0,False
        
        # Main cycle: integrate system over the step, calculate PID reaction
        # and fill lists with data
        for i in range(1,steps+1):
            times += [start + i * deltat]
            int_t = np.linspace(times[i-1],times[i],100)
            var = self.Step(set_p-y_sol[-1], deltat)
            if ch: vart = max(min(var, ma), mi),
            else: vart = var,
            sol = sp.integrate.odeint(sys,y_sol[-1], int_t, args = vart, tfirst=True)
            var_sol.append(var)
            y_sol.append(sol[-1][0])
        
        # When elaboration ends, return time array, and observed variable and 
        # manipulated variable over time array
        return times,y_sol,var_sol