"""
@author: Mattia
"""

from ClimaticChamber import CCModel as syst
from PID import PID
from matplotlib import pyplot as plt

# Generate PID class instances and simulate system

noInt_PID = PID(1, 0, 0)

start = 0
deltat = 1
steps = 5000
sys = syst
start_p = 0
set_p = 100
start_var = 0
resistor_range = [0,400] # Assuming resistor temperature cannot go below 0 and above 400 °C
t1,y11,y12 = noInt_PID.Simulate_1stDeg(start, deltat, steps, sys, start_p, set_p, start_var,resistor_range)

int_PID = PID(1, 0.002, 0)

t2,y21,y22 = int_PID.Simulate_1stDeg(start, deltat, steps, sys, start_p, set_p, start_var,resistor_range)

# Plot and save data

fig = plt.figure(figsize=[18,5])
fig.subplots_adjust(top=0.92, left=0.05, right = 0.98)
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
ax1.set_ylabel('Temperature [°C]')
ax1.set_xlabel('Time [s]')
ax2.set_ylabel('Temperature [°C]')
ax2.set_xlabel('Time [s]')
ax1.set_title('Kp = 1, Ki = 0, Kd = 0', loc = 'center', fontsize=18, weight = 'bold')
ax2.set_title('Kp = 1, Ki = 0.002, Kd = 0', loc = 'center', fontsize=18, weight = 'bold')

ax1.plot(t1, y11, label = 'Chamber T')
ax1.plot(t1, y12, label = 'Controller T', linestyle = '--')
ax2.plot(t2, y21, label = 'Chamber T')
ax2.plot(t2, y22, label = 'Controller T', linestyle = '--')
ax1.legend(loc = 'lower right')
ax2.legend(loc = 'lower right')
plt.tight_layout()
fig.savefig('Climatic_Chmaber_PID.png', bbox_inches='tight')
# Prevents Spyder from forcefully showing figure because of interactive mode
# plt.close(fig)
print('Figure saved as Climatic_Chmaber_PID.png')