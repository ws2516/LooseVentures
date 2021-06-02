import pandas as pd
import numpy as np

#data
data_qqq = pd.read_csv('ShortQQQ/QQQ.csv')
data_sqqq = pd.read_csv('ShortQQQ/SQQQ.csv')

close_qqq = data_qqq[['Date','Close']]
close_sqqq = data_sqqq[['Date','Close']]

combined_sqqq_qqq = close_sqqq.merge(close_qqq, on='Date')
combined_sqqq_qqq.columns = ['Date','SQQQ','QQQ']

#parameters

increment_threshold = 0.1
thresholds = np.linspace(0.1,0.25)
close_threshold = 0.5

#functions

def get_min_percentage(month_array,current,threshold):
    return (min(current/month_array) <=  (1- threshold))


for threshold in thresholds:
    #runners
    trigger = [np.NaN]*30
    for i in range(len(combined_sqqq_qqq['QQQ'].values)-30):
        month_array = combined_sqqq_qqq['QQQ'][i:i+30]
        current = combined_sqqq_qqq['QQQ'][i+30]
        if get_min_percentage(month_array,current,threshold) and trigger[-1]!='Buy':
            trigger.append('Buy')
        else:
            trigger.append('Hold')

    combined_sqqq_qqq['QQQ_Trigger'] = trigger

    counter, price, InitBuy, trade = 0, [1], False, []
    for i in range(len(combined_sqqq_qqq['QQQ'].values)-30):
        month_array = combined_sqqq_qqq['QQQ'][i:i+30]
        current = combined_sqqq_qqq['QQQ'][i+30]
        QQQ_Trigger = combined_sqqq_qqq['QQQ_Trigger'][i+30]
        sqqq = combined_sqqq_qqq['SQQQ'][i+30]
        if QQQ_Trigger == 'Buy' and not InitBuy:
            InitBuy = True
            price.append(current)
            trade.append(sqqq)
        elif InitBuy and price[-1]/current < 1 - increment_threshold and counter <3:
            combined_sqqq_qqq['QQQ_Trigger'][i+30] = 'Buy More'
            price.append(current)
            trade.append(sqqq)
            counter += 1
        elif sqqq/np.mean(trade) < 1 - close_threshold:
            combined_sqqq_qqq['QQQ_Trigger'][i+30] = 'Sell'
            trade = []
            InitBuy = False
            counter = 0
        else:
            combined_sqqq_qqq['QQQ_Trigger'][i+30] = np.NaN
    combined_sqqq_qqq = combined_sqqq_qqq.dropna()
    print(combined_sqqq_qqq)
