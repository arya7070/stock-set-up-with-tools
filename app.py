

from datetime import datetime, timedelta
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from apiKeys import *
import webbrowser

import re
def openRRG(stock_list, 
                                   base_url="https://stockcharts.com/freecharts/rrg/?period=daily&range=threemonths&group=custom&symbols=", 
                                   chrome_path="C:/Program Files/Google/Chrome/Application/chrome.exe"):
    """
    Constructs and opens a StockCharts RRG URL with all the stocks in the list using Google Chrome.

    Parameters:
        stock_list (list): A list of strings with stock symbols and values (e.g., ['ADI 1', 'AMAT 1']).
        base_url (str): The base URL for StockCharts RRG (default provided).
        chrome_path (str): Full path to the Chrome executable.
    """
    try:
        # Register Google Chrome with its full path
        webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(chrome_path))
        chrome = webbrowser.get("chrome")
    except webbrowser.Error:
        print(f"Error: Could not locate Chrome at {chrome_path}. Please check the path and try again.")
        return

    # Extract only the stock symbols
    stock_symbols = [stock.split()[0] for stock in stock_list]
    
    # Join the symbols with commas to form the query string
    symbol_query = "%2C".join(stock_symbols)  # URL encode for commas
    
    # Construct the full URL
    full_url = f"{base_url}{symbol_query}&isArrowMode=true&tailLength=15"
    
    # Open the URL in Google Chrome
    chrome.open(full_url)

def openTabs(stock_list, 
                                    base_url="https://www.tradingview.com/chart/uy1QCKEy/?symbol=",
                                    chrome_path="C:/Program Files/Google/Chrome/Application/chrome.exe"):
    """
    Opens TradingView tabs for the given stock list in Google Chrome.

    Parameters:
        stock_list (list): A list of strings with stock symbols and values (e.g., ['ADI 1', 'AMAT 1']).
        base_url (str): The base URL for TradingView charts (default provided).
        chrome_path (str): Full path to the Chrome executable.
    """
    try:
        # Register Google Chrome with its full path
        webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(chrome_path))
        chrome = webbrowser.get("chrome")
    except webbrowser.Error:
        print(f"Error: Could not locate Chrome at {chrome_path}. Please check the path and try again.")
        return

    for stock in stock_list:
        # Extract the stock symbol
        stock_symbol = stock.split()[0]
        
        # Construct the full TradingView URL
        url = f"{base_url}{stock_symbol}"
        
        # Open the URL in a new browser tab
        chrome.open(url)
def cleandata(input_list):
    # Remove trailing numbers, spaces, and periods using regex
    cleaned_list = [re.sub(r'\s*\d+\s*\.?', '', item) for item in input_list]
    return ','.join(cleaned_list)
def convert_to_comma_separated(input_list):
    return ','.join(input_list)
def get_historical_prices(symbol,interval, start_date, end_date):#gets the data
    base_url = 'https://api.tradier.com/v1/markets/history'
    headers = {
        'Authorization': tradier,
        'Accept': 'application/json'
    }
    params = {
        'symbol': symbol,
        'start': start_date,
        'end': end_date,
        'interval':interval
    }
    response = requests.get(base_url, headers=headers, params=params)
    data = response.json()
    return data['history']['day']
def score (candelsF):#scores the candels
    points=0;
    if candelsF[1]["IB"]: #if the first candel is a ib
        points= points +1
    if candelsF[3]["IB"]:#if last candel is ib
        points= points +1
    if candelsF[0]["low"]>candelsF[1]["low"]:
        points= points +1
    if candelsF[1]["UpWick"]:
        points= points +.4
    if candelsF[2]["UpWick"]:
        points= points +.4   
    if candelsF[3]["UpWick"]:
        points= points +.4
    return points
def greenday(daybefor, dayafter,atr): #addes some context to the candels, needs stuf for downweek
    dayafter["green"] = False 
    dayafter["NoWick"] = False
    dayafter["UpWick"] = False
    dayafter["GapDown"]=False
    dayafter["IB"]=False 
    if dayafter["open"] < dayafter["close"]:
        dayafter["green"] = True
    if dayafter["green"] == True :
        if (atr * .27 >dayafter["high"]- dayafter["close"] or .3 * atr >dayafter["high"]- dayafter["low"]or (2.5* (dayafter["high"]- dayafter["close"])<dayafter["close"]- dayafter["open"] and atr * .4 >dayafter["high"]- dayafter["close"] )):
            dayafter["NoWick"] = True
    if dayafter["green"] == True:
        if (atr * .33 <dayafter["open"]- dayafter["low"] and .3 * atr <dayafter["high"]- dayafter["low"]): #seconedcalcualtion i think is useless
            dayafter["UpWick"] = True        
    if (dayafter["open"]-daybefor["close"]>0 or .16 * atr<daybefor["close"]-dayafter["open"]):
        dayafter["GapDown"]=True
    if(daybefor["low"]<dayafter["low"] and daybefor["high"]>dayafter["high"] ):
        dayafter["IB"]=True
    return dayafter
def atr(data):
    true_ranges = []
    for i in range(1, len(data)):
            high = data[i]["high"]
            low = data[i]["low"]
            prev_close = data[i - 1]["close"]
            true_range = max(high - low, abs(high - prev_close), abs(low - prev_close))
            true_ranges.append(true_range)
    return sum(true_ranges) / len(true_ranges)
    
names= [
    "AAPL", "ABBV", "ABNB", "ABT", "ADBE", "ADI", "AFRM", "AMAT", "AMC", "AMD","ARM",
    "AMGN", "AMZN", "AVGO", "AXP", "BA", "BABA", "BAC", "BIDU", "BLK", "BMY", "C",
    "CAT","CAVA","CART", "CCJ", "CCL", "CHWY", "CL", "COIN", "COST", "CRM","CMG", "CROX", "CI", "CRWD", "CSCO", "CVS",
    "CVX", "CZR", "DD", "DASH", "DDOG", "DE", "DPZ", "DIS", "DKNG", "DLTR", "DOCU", "EAT", "EBAY", "ENPH",
    "EWZ", "EXPE", "F", "FANG", "FCX", "FDX", "FL","FUTU", "FSLR", "GDX", "GE", "GLD", "GM", "GME",
    "GOOG", "GOOGL", "GS", "H", "HD", "HON", "HOOD", "HPQ", "HYG", "IBM", "IBKR","INTC", "IWM", "JD", "JNJ", "JPM",
    "KO", "LLY", "LMT", "LQD", "LULU", "LUV", "M", "MA", "MCD", "MDT", "META", "MGM", "MMM", "MO",
    "MRK", "MRVL", "MRNA", "MS", "MSFT", "MSTR", "MU", "NCLH", "NET", "NFLX", "NKE", "NUE", "NVDA", "OIH",
    "ORCL", "PANW", "PARA", "PEP", "PFE", "PG", "PINS", "PLTR", "PLUG", "PM", "PYPL", "QCOM", "QQQ",
    "RBLX","ROKU", "ROST", "RUN", "SBUX", "SCHW","SE", "SHOP", "SLV", "SMH", "SNAP", "SNOW", "SPOT", "SOXL", "SOFI",
    "SPY", "xyz", "T", "TDOC", "TER", "TLT","TTWO", "TSLA", "TSM", "TTD", "TWLO", "UAL", "USO", "U", "UBER", "UNH",
    "UNP", "UPS", "UPST", "V", "VALE", "VZ", "WBA", "WDC", "WFC", "WMT", "WYNN", "X", "XBI", "XLB", "XLF",
    "XLI", "XLK", "XLRE", "XLU", "XLV", "XLY","hims", "XOM", "ZM", "ZS", "QQQ", "SPY", "TAN"
]

smallNames=["AAPL","upst","MSFT","ABNB","TTD","ADBE","ADI","AFRM",'GE',
            'NVDA','SNOW','MSTR','BABA','JD','TLT','HYG','V','CRWD','COIN',
            'QCOM','RIVN','MRNA','ZS','HOOD','SHOP','BA','CCJ','TWLO','GOOG','GE',
            'DOCU','PANW','LQD','DKNG','ROKU','WFC','SQ','C','GS','JPM','ZM','U',
            'TSLA','TDOC','NVDA','RBLX','CZR','MGM','FSLR','SOXL','DDOG','F','NET',
            'NCLH','GLD','SLV',"hd","INTC","smh","nke","amd"]
arkk= ['TSLA', 'COIN', 'ROKU', 'ZM', 'SQ', 'TWLO', 'SHOP', 'TDOC', 'DNA', 'CRSP', 'NTLA',
       'RBLX', 'BEAM', 'TXG', 'TER', 'NVDA', 'SDGR', 'TRMB', 'META' ,'ACCD' ,'ADPT' ,'VERV'
       ,'CDNA' ,'ARCT' ,'MELI' ,'DE' ,'VEEV' ,'GLBE' ,'ADYEN' ,'VRTX' ,'DSY' ,'INTU' ,'QSI'
       ,'GENI' ,'INCY' ,'BILL' ,'GOOG' ,'AMD' ,'MASS' ,'STNE' ,'NET' ,'MRNA' ,'TOST' 
        ,'CRWD' ,'NVTA' ,'NRIX' ,'CMPS' ,'REGN' ,'BFLY' ,'JOBY' ,'ESLT' ,'RKLB' ,'SNPS' 
       ,'CAT' , 'TSM', 'MKFG', 'GH', 'MGA', 'ANSS', 'TDY', 'PFE', 'KSPI', 'TTD', 'LMT'
       , 'LHX', 'MSFT', 'SPOT', 'ISRG', 'MTLS', 'SOFI', 'HON']
#onename=["aapl","ADBE","ADI","AFRM",'GE','NVDA','SNOW','MSTR',"aapl"]
onename=['NVDA','SNOW','MSTR',"cost","jd"]
passnames=[]
passnames_no_squeez=[]
errorlist=[]
IB_list=[]
errorlistW=[]
IB_list_W=[]
IB_list_Double=[]
for i in names:
    #set delta
    delta=30
    #set lookback 
    lookback=0
    # Get the current date
    current_date = datetime.now()-timedelta(days=lookback)
    # Calculate the date of the day right before today
    previous_date = current_date - timedelta(days=delta)

    # Format the previous date in the desired format 
    '2023-05-04'
    formatted_previous_date = previous_date.strftime('%Y-%m-%d')
    formatted_current_date = current_date.strftime('%Y-%m-%d')
    #########################################################################
    
    
    print("im scaning ",i)
    try:    
        b=get_historical_prices(i,'daily',formatted_previous_date ,formatted_current_date)
    except Exception:
            errorlist.append(i)
            print("errorrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrs", i)
            pass
    atr_now=atr(b)
    lastdate=greenday(b[-2],b[-1],atr_now)
    midday=greenday(b[-3],b[-2],atr_now)
    firstday=greenday(b[-4],b[-3],atr_now)#3 candels ago greenday(b[-3],b[-2],atr)
    zerodays=greenday(b[-5],b[-4],atr_now)
    candels=[zerodays,firstday,midday,lastdate]
    if lastdate["green"] and midday["green"] and firstday["green"] or lastdate["green"] and midday["green"] and firstday["IB"]:
        print("bingo" +" " + i) 
        if lastdate["NoWick"] and midday["NoWick"]:
            print("nowick")
            passnames_no_squeez.append(i+" " + str(score(candels)))
            if lastdate['close']-lastdate['open']<1.2 * (midday['high']-midday['low']):
               passnames.append(i+" " + str(score(candels)))
               #print("squeez")
              # print(score(candels))
    if lastdate["IB"]:
        IB_list.append(i)
    try:    
        c=get_historical_prices(i,'weekly',formatted_previous_date ,formatted_current_date)
    except Exception:
            errorlistW.append(i)
            print("errorrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrs", i)
            pass    
    atr_weelky=atr(c) #at does not work
    lastdateW=greenday(c[-2],c[-1],atr_now)
    middayW=greenday(c[-3],c[-2],atr_now)
    if lastdateW["IB"]:
        IB_list_W.append(i) 
    if lastdate["IB"] and midday["IB"]:
        IB_list_Double.append(i)
c=get_historical_prices("aapl",'weekly',formatted_previous_date ,formatted_current_date)
print("this is bull set up") 
print(passnames)
print("this is |||| no squeez below")    
print(passnames_no_squeez)        
print("this is |||| erors below")  
print(errorlist) 
print("this is |||| IB s")
print(IB_list)
print("this is |||| IB s W")
print(IB_list_W)
print("this is |||| double ib")
print(IB_list_Double)
