import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt

panel_data = pd.read_csv('./VIX.csv')

date = panel_data['Date'].values
close_data = panel_data['Close'].values
#adjusted_close = panel_data['Adj. Close'].values
open_data = panel_data['Open'].values

vix_gt = 30
vix_incr_increase = 10
vix_decreas_multi = 0.33
buy_mult = 0.33
track = []
stack = ['Init']
pos_star = 100 #100% of the share at that price
buy_price = 10000000

for i in range(len(open_data)):
	if close_data[i] >= 30 and stack[-1] not in ['Buy','Buy More']:
		stack.append('Buy')
		buy_price = close_data[i]
		position = close_data[i] #sell short
	elif close_data[i]-buy_price >= 10 and stack[-1] not in ['Sell']:
		stack.append('Buy More')
		buy_price = (buy_price + close_data[i])/2
		position = buy_price
	elif close_data[i]/buy_price <= 0.66 and stack[-1] not in ['Sell']:
		stack.append('Sell')
		sell_price = -close_data[i]
		position = buy_price+sell_price
	else:
		continue
	track.append(position)

plt.plot(np.arange(len(track)),track)
plt.show()
	
	
