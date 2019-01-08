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
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            stockJSON = requests.get("https://api.iextrading.com/1.0/stock/{}/chart/1y".format(ticker)).json() #IEX API

            with open("{}.json".format(ticker), 'w') as outfile:
                json.dump(stockJSON, outfile)
            
            stockDF = pd.read_json("{}.json".format(ticker))
            dir_path = os.path.dirname(os.path.realpath(__file__)) + "\\stock_dfs\\{}.csv".format(ticker)
            stockDF.to_csv(dir_path)
            print(ticker)
        else:
            print("Already have {}".format(ticker))

#getData()