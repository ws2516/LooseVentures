import requests
from pprint import pprint
import quandl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
 
panel_data = pd.read_csv('~/Desktop/UVXY.csv')

initial_position = 100
day_change_window = 30
initial_increase_threshold = 0.5
secondary_increase_threshold = 0.33
position_allocation_multiplier = 0.33


#var defs
close = panel_data[['Close']]
indicator, save_buy, pos_allocated = [], [], []
array = []
stack = ['Init']


#indicator function
for i in range(len(close)):
	try:
		if close.iloc[i+day_change_window,:][0]/close.iloc[i,:][0] > 1+initial_increase_threshold:
			if stack[-1] not in ['Buy', 'Buy More']:
				stack += ['Buy']
				save_buy += [close.iloc[i+day_change_window,:][0]]
				pos_allocated += [initial_position * position_allocation_multiplier]
				initial_position = initial_position - pos_allocated[-1]
				indicator += [1]
				print('Bought at - ', save_buy[-1], ' - with $', pos_allocated[-1], ' with remaining funds of $', initial_position)
			elif stack[-1] != 'Buy' and save_buy[-1]/close.iloc[i+day_change_window,:][0] > 1+secondary_increase_threshold:
				stack += ['Buy More']
				save_buy += [close.iloc[i+day_change_window,:][0]]
				pos_allocated += [initial_position * position_allocation_multiplier]
				initial_position = initial_position - pos_allocated[-1]
				indicator += [1]
				print('Added more at - ', save_buy[-1], ' - with $', pos_allocated[-1], ' with remaining funds of $', initial_position)
			elif stack[-1] in ['Buy', 'Buy More'] and save_buy[-1]/close.iloc[i+5,:][0] > 1-secondary_increase_threshold:
				stack += ['Sell']
				save_buy += [close.iloc[i+day_change_window,:][0]]
				#cash_out += [1]
				initial_position = 100
				indicator += [1]
				print('Sold at - ', save_buy[-1], ' - with $', pos_allocated[-1], ' with remaining funds of $', initial_position)		
			else:
				indicator += [np.NaN]
		else:
			indicator += [np.NaN]
	except:
		indicator += [np.NaN]

print(len(indicator), len(close))
close['indicator'] = indicator
close['Date'] = panel_data[['Date']]
close = close.dropna()
pprint(close)
print(len(close))



'''

		if stack[-1] == 'Buy':
			/close.iloc[i,:][0] > secondary_increase_threshold
			
close = close['Close']

# Calculate the 20 and 100 days moving averages of the closing prices
short_rolling_msft = close.rolling(window=30).mean()
#long_rolling_msft = close.rolling(window=100).mean()

# Plot everything by leveraging the very powerful matplotlib package
plt.plot(close.index, close, label='UVXY')
plt.plot(short_rolling_msft.index, short_rolling_msft, label='20 days rolling')
#plt.bar(short_rolling_msft.index, indicator, label='100 days rolling')
plt.legend()
plt.show()
'''
