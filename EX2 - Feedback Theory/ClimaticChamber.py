"""
@author: ErMezz
"""

def CCModel(t,currT,vart):
    
    # Simplified Climatic Chamber model. Assumed that cooling and heating
    # behave similarly
    
    Qcoeff = 50 # W/m2K Forced heat convection from resistor
    Rarea = 1e-2 # m2 Resitor area
    kflux = Qcoeff * Rarea
    
    # Calculating heat flux
    Qflux = (vart - currT) / kflux
    
    Vol = 1 #m3 Climatic chamber volume
    Dair = 1.29 # kh/m3 Air density @Patm
    Cair = 1.012*1e3 # J/KgK Specific heat capacity
    Mair = Dair * Vol
    
    # Differential equation dT/dt = k(Th-T)
    dTdt = Qflux / (Mair * Cair)
    return dTdt

