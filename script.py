# -*- coding: utf-8 -*-





import pandas as pd
import numpy as np
import matplotlib.pyplot as plt







path = 'C:/Users/clain/Documents/Jupyter notes/Trading project/stocks.csv'


def create_df(start,end,symbols):
    #Define date range
    dates = pd.date_range(start,end)
    
    #create empty DataFrame with dates as index
    df_empty = pd.DataFrame(index=dates)
    
    #Read the csv into dataframe
    path = 'C:/Users/clain/Documents/Jupyter notes/Trading project/stocks.csv'
    
    df = pd.read_csv(path,index_col='date', usecols=['date','close','Name'], parse_dates=True, na_values=['nan'])
    
    
    #merge the dataframes and fill in the missing data
    df = df.join(df_empty,how='inner')
    df = df.fillna(method='pad')
    df = df.fillna(method='bfill')
    
    #convert DataFrame to wide format
    df = df.pivot(columns='Name', values='close')
    
    df = df[symbols]
    
    return df
    
symbols = ['AAPL','GOOGL','AMZN','FB']
    
df = create_df('2017-01-01','2018-12-31',symbols=symbols)


def plot_data():
    title = 'Stock Prices'
    xlabel = 'Date'
    ylabel = 'Price' 
    
    ax= df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()
    
    
def compute_daily_returns():
    daily_returns = df.copy()
    daily_returns.iloc[1:] = (daily_returns.iloc[1:] / daily_returns.shift(1)) -1
    daily_returns.iloc[0] = 0 #set daily returns for row 0 to 0
    for symbol in daily_returns:
        mean = daily_returns[symbol].mean()
        std = daily_returns[symbol].std()
        print(symbol,'kurtosis:', daily_returns[symbol].kurtosis())
        daily_returns[symbol].plot(kind='hist',bins=15),\
        plt.axvline(mean,c='w',linestyle='dashed',linewidth=2),\
        plt.axvline(std,c='y',linestyle='dashed',linewidth=2),\
        plt.axvline(-std,c='y',linestyle='dashed',linewidth=2),\
        plt.legend()
        
        plt.show()


def plot_rolling_stats():
    #calculate the rolling mean and std
    for i in df.columns:
        rm = df[i].rolling(window= 20).mean()
        rstd = df[i].rolling(window=20).std()
        u_bound = rm + rstd * 2
        l_bound = rm - rstd * 2
    
    
        ax= df[i].plot(title= i,x='Date',y='Price',legend=None)
        rm.plot(ax=ax)
        u_bound.plot(ax=ax)
        l_bound.plot(ax=ax)
        plt.legend(['Price','Mean','U-bound','L-bound'],loc='upper left')
        plt.show()
    
    
def daily_port_returns():
    alloc= [0.4,0.4,0.1,0.1]
    start_val = [2000,2000,500,500]
    
    df_normed = (df.iloc[:] / df.iloc[0])
    df_alloced = df_normed * alloc
    df_postval = df_alloced * start_val
    df_portval = df_postval.sum(axis=1)
    
    
    daily_returns = df_portval.copy()
    daily_returns.iloc[1:] = (daily_returns.iloc[1:] / daily_returns.shift(1)) -1
    daily_returns.iloc[0] = 0
    
    daily_returns = daily_returns[1:]
    
    print(daily_returns.head())
    
    return daily_returns
    

daily_port_returns()