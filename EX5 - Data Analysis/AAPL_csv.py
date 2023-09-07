"""
@author: ErMezz
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Upload data from csv
data = pd.read_csv('stocks data.csv')
dates = pd.to_datetime(data['Date'])
# Choose last year's data
year = pd.Timedelta(365,unit='d')
for j in range(len(dates)):
    if dates[len(dates)-1] - dates[len(dates)-1-j] > year:
        break
# Prepare arrays for plotting
dates = [date.date() for date in dates[len(data)-j:len(data)-1]]
data = data['Adj Close'][len(data)-j:len(data)-1]
data = data.tolist()

# Prepare plot and labels
plt.style.use('seaborn-v0_8-dark-palette')
plt.rcParams["font.family"] = "Lato"

fig = plt.figure(figsize=[12,5])
fig.subplots_adjust(top=0.91, left=0.1, right=0.95)
ax1 = fig.add_subplot(111)
ax1.set_ylabel('Close [$]')
ax1.set_xlabel('Year-Month', loc = 'right')
ax1.set_title('AAPL - Last year', loc = 'center', weight = 'bold', fontsize = 18)

# Plot semitransparent y grid
plt.grid(axis = 'y', alpha = 0.3)

# Sets axis limits and create plot
ax1.plot(dates,data,'darkgreen', linewidth = 2)
ax1.axes.set_xlim(dates[0],dates[-1])
ax1.axes.set_ylim(min(data)*0.95,max(data)*1.05)

# Creates min/max/avg bars
avgd = [min(data),max(data),np.nanmean(data)]
avg = avgd[2]
for i in range(3): ax1.axhline(avgd[i], ls='--', color = ['r','g','c'][i])

# Color the graph
high,low = [],[]
for i in range(len(data)):
    test = data[i] < avg
    low.append(test)
    high.append(not test)
    
# Clean up crossing points colors
for i in range(1,len(low)-1):
    if low[i-1] and low[i+1] and not low[i]: high[i-1],high[i+1] = True,True
    if (not low[i-1] and not low[i+1]) and low[i]: low[i-1],low[i+1] = True,True

ax1.fill_between(dates, data, avg, color = 'g', alpha = 0.04, where = high)
ax1.fill_between(dates, data, avg, color = 'b', alpha = 0.04, where = low)


# Create y-axis clone for min/max/avg labels and move original to the right
newax = plt.twinx()

ax1.tick_params(axis='y', which='both', labelleft= False, labelright= True, left = False, right = True)
ax1.yaxis.set_label_position('right')
newax.tick_params(axis='y', which='both', labelleft= True, labelright= False, left = True, right = False)
newax.axes.set_ylim(min(data)*0.95,max(data)*1.05)
newax.yaxis.set_ticks(avgd,[f'Min: {round(avgd[0],1)}$',f'Max: {round(avgd[1],1)}$',f'Avg: {round(avgd[2],1)}$'], fontsize = 14)

# Set borders
for axis in ['bottom','right']:
    ax1.spines[axis].set_linewidth(1.5)
for axis in ['top','left']:
    ax1.spines[axis].set_alpha(0)
    newax.axes.spines[axis].set_alpha(0)


# Save figures
fig.savefig('AAPL_csv.png', bbox_inches='tight')
print('Figure saved as AAPL_csv.png')

# Show figures
plt.show()