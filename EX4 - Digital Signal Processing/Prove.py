# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 11:32:52 2023

@author: emezmat
"""

import control as ct
import matplotlib.pyplot as plt

H = ct.tf([1],[1,-1])
print(H)

order = 2
N = 1

num = [1 if i==order else 0 for i in range(order+1)]
num.reverse()
den = [1 if i==order else 0 for i in range(order+1)]
den[-2] = -1
den.reverse()
num[-1] = -1
H = ct.tf(num,den,True)
H = H**N
# H = ct.tf([1,0,0,1],[1,0,0,0],True)
print(H)
# x,y = ct.impulse_response(H)

# plt.plot(x,y)
w = [i * 1e-1 for i in range(0,100000)]
ct.bode_plot(H,omega=w)