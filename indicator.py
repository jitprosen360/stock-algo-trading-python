import yfinance as yf
import talib
import pandas as pd
import copy
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

def backtestsymbol(symbol):

    df = yf.Ticker(f"{symbol}.NS").history(period = "5y" , interval = "1d")


    df["MA_10"] = talib.MA(df["Close"], timeperiod = 10)
    df["MA_50"] = talib.MA(df["Close"], timeperiod = 50)
    df["RSI_14"] = talib.RSI(df["Close"], timeperiod = 14)
    # df["ATR_14"] = talib.ATR(df["Close"], df["High"] , df["Low"], timeperiod = 14)
    # df["Upper_band"] , df["Middle_band"], df["Lower_band"] = talib.BBANDS(df["Close"], timeperiod = 20 , nbdevup = 2 , nbdevdn=2)

    # print(df)
    mytradelist = []
    trade = { "Symbol" : None , "Buy/Sell" : None ,"Entry": None, "Entry Date" : None, "Exit" : None , "Exit date" : None }
    position = None
    for i in df.index[49:]:
        if df["MA_10"][i] > df["MA_50"][i] and df["RSI_14"][i] > 70 and position != "Buy":
            if trade["Symbol"] is not None:
                trade["Exit"] = df["Close"][i]
                trade["Exit date"] = i
                mytradelist.append(copy.deepcopy(trade))
            if position is not None:
                trade["Symbol"] = symbol
                trade["Buy/Sell"] = "Buy"
                trade["Entry"] = df["Close"][i]
                trade["Entry Date"] = i
            position = "Buy"
        
        if df["MA_10"][i] < df["MA_50"][i] and df["RSI_14"][i] < 30 and position != "Sell":
            if trade["Symbol"] is not None:
                trade["Exit"] = df["Close"][i]
                trade["Exit date"] = i
                mytradelist.append(copy.deepcopy(trade))
            if position is not None:
                trade["Symbol"] = symbol
                trade["Buy/Sell"] = "Sell"
                trade["Entry"] = df["Close"][i]
                trade["Entry Date"] = i
        
            position = "Sell"
    return mytradelist

symbollist = backtestsymbol("TATAMOTORS")
print(pd.DataFrame(symbollist))
# symbollist = ["TATAMOTORS", "Reliance", "Upl"]

# alltrades = []
# for symbol in symbollist:
#     for i in backtestsymbol(symbol):
#         alltrades.append(i)
# print(pd.DataFrame(alltrades))
        
