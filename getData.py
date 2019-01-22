import bs4 as bs
import pickle
import requests
import pandas as pd
import os
import json

def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class' : 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]: # tr = tablerow, from one onwards
        ticker = row.findAll('td')[0].text # td = table data
        tickers.append(ticker)

    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    print(tickers)

    return

#save_sp500_tickers()

def getData():
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)
    
    if not os.path.exists('stock_csv'):
        os.makedirs('stock_csv')

    for ticker in tickers:
        if not os.path.exists('stock_csv/{}.csv'.format(ticker)):
            stockJSON = requests.get("https://api.iextrading.com/1.0/stock/{}/chart/1y".format(ticker)).json() #IEX API

            with open("{}.json".format(ticker), 'w') as outfile:
                json.dump(stockJSON, outfile)
            
            stockDF = pd.read_json("{}.json".format(ticker))
            stockDF.to_csv('stock_csv\\{}.csv'.format(ticker))
            print(ticker)
        else:
            print("Already have {}".format(ticker))

#getData()

def calcResult(df, index):
    pctChange = (df.at[index, 'close'] - df.at[index + 10, 'close']) / df.at[index, 'close'] * 100
    if pctChange >= 2:
        return 1
    elif pctChange <= -2:
        return -1
    else:
        return 0

def calcMA(df, index, periodLength):
    
    simpleMA = 0

    for i in range (1, periodLength + 1):
        simpleMA += df.at[index-i, 'close']

    return simpleMA / periodLength

def compile_data_oneStock(ticker):
    df = pd.read_csv('stock_csv\\{}.csv'.format(ticker))
    df.drop(columns = ['change', 'changeOverTime', 'changePercent', 'date', 'high', 'label', 'low', 'open', 'unadjustedVolume', 'volume', 'vwap', 'Unnamed: 0'], inplace = True)
    
    columnList = ["close", "10D_SMA", "20D_SMA", "30D_SMA", "RESULT"]
    stockDataFrame = pd.DataFrame(columns = columnList)

    for index, row in df.iterrows():
        if index <= 41 or index >= 235:
            continue

        try:
            df.at[index + 10, 'close']
        except KeyError:
            break

        valueList = [row['close'], calcMA(df, index, 10), calcMA(df, index, 20), calcMA(df, index, 30), calcResult(df, index)]
        
        dayDataFrame = pd.DataFrame(columns = columnList)
        dayDataFrame.loc["{}_{}".format(ticker, index)] = valueList
        
        stockDataFrame = stockDataFrame.append(dayDataFrame)
    
    return stockDataFrame

def compile_data():
    with open("sp500tickers.pickle", 'rb') as f:
        tickers = pickle.load(f)

    columnList = ["close", "10D_SMA", "20D_SMA", "30D_SMA", "RESULT"]

    main_df = pd.DataFrame(columns = columnList)
    
    for count, ticker in enumerate(tickers):
        main_df = main_df.append(compile_data_oneStock(ticker))
        print(ticker)

    main_df.to_csv('compiledData.csv')

#compile_data()