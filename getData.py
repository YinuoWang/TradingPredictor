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

def compile_data():
    with open("sp500tickers.pickle", 'rb') as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()
    
    for count, ticker in enumerate(tickers):
        df = pd.read_csv('stock_csv\\{}.csv'.format(ticker))
        df.rename(columns = {'close' : ticker}, inplace = True)
        df.drop(columns = ['change', 'changeOverTime', 'changePercent', 'date', 'high', 'label', 'low', 'open', 'unadjustedVolume', 'volume', 'vwap', 'Unnamed: 0'], inplace = True)
        
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how = 'outer')

    print(main_df.head())
    main_df.to_csv('sp500_joined_closes.csv')

#compile_data()