import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
from datetime import date


def get_hold_time(date1, date2):
	d1split = date1.split('-')
	d2split = date2.split('-')
	d0 = date(int(d1split[0]), int(d1split[1]), int(d1split[2]))
	d1 = date(int(d2split[0]), int(d2split[1]), int(d2split[2]))
	delta = d1 - d0
	return delta.days

panel_data = pd.read_csv('./VIX.csv')

dater = panel_data['Date'].values
close_data = panel_data['Close'].values
#adjusted_close = panel_data['Adj. Close'].values
open_data = panel_data['Open'].values

#------------------- parameters ---------------------
vix_trigger = 30
inc_increment = 10
dec_target = 0.66
pos_multipler = 0.33
number_of_increments = 3
posit = 10000

#------------------- dummy variables and temps ---------------------
buy_price = 1000000
InitBuy = True
transaction, BBmS, Date, transaction_number, transaction_value = [], [], [], [], []
share_num , tester = [], []
counted = 0

for i in range(len(open_data)):
	if close_data[i] >= vix_trigger and InitBuy:
		counted += 1
		transaction += [close_data[i]]
		BBmS += ['Buy']
		Date += [dater[i]]
		buy_price = close_data[i]
		transaction_number += [counted]
		shares = (posit/number_of_increments)//buy_price
		share_num += [shares]
		transaction_value += [shares*buy_price]
		InitBuy = False
		counter = 1
		
	elif close_data[i]-buy_price >= inc_increment and not InitBuy and counter<number_of_increments:
		transaction += [close_data[i]]
		buy_price = (close_data[i]+counter*buy_price)/(counter+1) #fix this
		counter += 1
		BBmS += ['Buy More']
		transaction_number += [counted]
		shares += (posit/number_of_increments)//buy_price
		share_num += [shares]
		transaction_value += [shares*buy_price]
		Date += [dater[i]]
		
	elif close_data[i]/buy_price <= dec_target and not InitBuy:
		InitBuy = True
		transaction += [close_data[i]]
		BBmS += ['Sell']
		Date += [dater[i]]
		transaction_number += [counted]
		transaction_value += [shares*close_data[i]]
		share_num += [shares]
	else:
		continue

#--------------------------------------------------

df = pd.DataFrame({'Date':Date, 'Buy/BuyMore/Sell':BBmS, 'Price':transaction, 'Transaction Number':transaction_number, 'Transaction Value':transaction_value, "Number of Shares":share_num }).round(2)
df.to_csv('./PaperLedger.csv')


alt.Chart(df).mark_point(filled = True, size = 30).encode(
    x='Date:T',
    y='Price:Q',
    color='Buy/BuyMore/Sell:N',
    tooltip = ['Price','Buy/BuyMore/Sell']
).interactive().show()


#--------------------------------------------------
returns, tnumber, pos_used = [], [], []
for i in np.unique(df['Transaction Number'].values):
	newdf = df[df['Transaction Number'] == i]
	returns += [(newdf['Transaction Value'].values[-2] - newdf['Transaction Value'].values[-1])/newdf['Transaction Value'].values[-2]]
	tnumber += [i]
	pos_used += [round((len(newdf)-1)/number_of_increments,2)]

print(sum(returns)*100, len(returns), np.mean(returns), np.median(returns))

alt.Chart(pd.DataFrame({'Transaction Number':tnumber, 'Returns':returns, 'Position Used':pos_used})).mark_bar().encode(
    x='Transaction Number:O',
    y='Returns:Q',
    color='Position Used:O',
    tooltip = ['Transaction Number','Returns','Position Used']
).interactive().show()

#--------------------------------------------------
holdTime, datesHeld, startHold = [], [], []

df = df[df['Buy/BuyMore/Sell'] != 'Buy More']
for i in range(len(df.Date.values)//2):
	holdTime += [get_hold_time(df.Date.values[2*i],df.Date.values[2*i + 1])]
	datesHeld += [str(df.Date.values[2*i]) + ' to ' + str(df.Date.values[2*i + 1])]
	startHold += [df.Date.values[2*i]]


alt.Chart(pd.DataFrame({'datesHeld':datesHeld, 'holdTime':holdTime, 'Start':startHold})).mark_bar().encode(
    x='Start:T',
    y='holdTime:Q',
    tooltip=['Start','datesHeld','holdTime']
).interactive().show()


'''
Trade Stats: (On Close)

Hold Time between Buy and Sell: Mean 73 Days, Median 49 Days, Max 246, Min 3

Increase Position Frequency: ~23%

Percent Profitable: 100%

Average Profit per Trade: $12.9 on a base of one unit trades (~$30 entry)

Median Profit per Trade: $12.1 on a base of one unit trades (~$30 entry)






Trade Stats: (On Open)

Average Hold Time between Buy and Sell:

Increase Position Frequency:

Percent Profitable:

Average Profit per Trade:

Median Profit per Trade:






Trade Stats: (On Adjusted Close)

Average Hold Time between Buy and Sell:

Increase Position Frequency:

Percent Profitable:

Average Profit per Trade:

Median Profit per Trade:


'''