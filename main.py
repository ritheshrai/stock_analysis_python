import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import the csv file into dataframe.
dataset = pd.read_csv("stocks_info.csv")
dataset['Date'] = pd.to_datetime(dataset['Date'])
print('max_close_price =', dataset['Close Price'].max())
print('min_close_price =', dataset['Close Price'].min())
print('Average_close_price =', dataset['Close Price'].mean())


# avrage price for n days
def avgprice(n):
    start_date = pd.to_datetime('13-5-2019') - pd.Timedelta(n, unit='D')
    averageprice = dataset[dataset['Date'] >= start_date]['Close Price'].mean()
    print('average price over {0} days={1}'.format(n, averageprice))


# funtion for profi percentage of stock profit/loss
def percentchange(n):
    start_date = pd.to_datetime('13-5-2019') - pd.Timedelta(n, unit='D')
    required = dataset[dataset['Date'] >= start_date]['Close Price']
    required = required.to_numpy()
    percent_change = ((required.max() - required.min()) / required.min()) * 100
    if percent_change > 0:
        print('Profit : percent change over {0} days={1}'.format(n, percent_change))
    else:
        print('Loss : percent change over {0} days={1}'.format(n, percent_change))


# n = 7 for 1 week and n= 30 for a month n=365 for a year
n = int(input("avrage price and profit loss of number of days ,peaseenter the day ( 7 for 1 week and  30 for a month 365 for a year)"))
avgprice(n)
percentchange(n)
# ceating a new column
dataset = dataset.assign(Day_Perc_Change=np.nan)
dataset['Day_Perc_Change'] = dataset['Close Price'].pct_change() * 100
dataset1 = dataset.drop(0)
# creating a new column “Trend”
dataset1 = dataset1.assign(Trend=np.nan)
# filling content to the "Trend" column to market term
dataset1.loc[(dataset1['Day_Perc_Change'] >= -0.5) & (dataset1['Day_Perc_Change'] <= 0.5), 'Trend'] = 'Slight or No Change'
dataset1.loc[(dataset1['Day_Perc_Change'] >= 0.5) & (dataset1['Day_Perc_Change'] <= 1), 'Trend'] = 'Slight positive'
dataset1.loc[(dataset1['Day_Perc_Change'] >= -1) & (dataset1['Day_Perc_Change'] <= -0.5), 'Trend'] = 'Slight negative'
dataset1.loc[(dataset1['Day_Perc_Change'] >= 1) & (dataset1['Day_Perc_Change'] <= 3), 'Trend'] = 'Positive'
dataset1.loc[(dataset1['Day_Perc_Change'] >= -3) & (dataset1['Day_Perc_Change'] <= -1), 'Trend'] = 'Negative'
dataset1.loc[(dataset1['Day_Perc_Change'] >= 3) & (dataset1['Day_Perc_Change'] <= 7), 'Trend'] = 'Among top gainers'
dataset1.loc[(dataset1['Day_Perc_Change'] >= -7) & (dataset1['Day_Perc_Change'] <= -3), 'Trend'] = 'Among top losers'
dataset1.loc[(dataset1['Day_Perc_Change'] > 7), 'Trend'] = 'Bull run'
dataset1.loc[(dataset1['Day_Perc_Change'] < -7), 'Trend'] = 'Bear drop'
#creating the pie and bar chart for data vishuvaization
# we are grouping the dataset according to trend using count
x = dataset1.groupby('Trend').size().reset_index(name="count")
labelss = [i for i in dataset1.Trend.unique()]
values = [i for i in x['count']]
# plot the pie chart
fig1, ax1 = plt.subplots(2,2,figsize=(20,19))
ax1[0,0].pie(values, labels=labelss, shadow=True, startangle=90)
ax1[0,0].axis('equal')
ax1[0,1].bar(labelss,values)
ax1[1,0].scatter(dataset1['Date'],dataset1['Close Price'])
ax1[1,0].set_xlabel('Close Price')
fig1.autofmt_xdate()
ax1[1,0].set_ylabel('Date')
plt.style.use('seaborn')
ax1[1,1].stem(dataset1['Date'],dataset1['Day_Perc_Change'],use_line_collection=True)
plt.show()
dataset1['Day_Perc_Change'].hist(bins=500)
plt.xlabel('Daily returns')
plt.ylabel('Frequency')
plt.show()


