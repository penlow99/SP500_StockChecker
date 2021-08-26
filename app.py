import yfinance as yf
import pandas as pd
import streamlit as st 
import os

# get the path of the csv that contains stock symbols and company names
dir_path = os.path.dirname(os.path.realpath(__file__))

# load csv into pandas dataframe
df_stocks = pd.read_csv(dir_path + "/data/sp500list.csv")

# use pandas series to create list of stock symbols
symbolList = df_stocks['Symbol'].tolist()

# create a form over in the sidebar to select stocks and dates
with st.sidebar.form('stockForm'):
    st.write("# S&P 500 Stock Checker")
    # create the select box using the list of symbols as the values, and the displayed option with the name of the company (using the format_func argument)
    stockSymbol = st.selectbox('Pick a stock from the S&P 500', symbolList, format_func=lambda x: df_stocks[df_stocks['Symbol']==x]['Security'].values[0])
    # create start and end date pickers
    startDate = st.date_input('Start Date')
    endDate = st.date_input('End Date')
    submitted = st.form_submit_button('Check Stock')

if submitted:
    # get ticker data
    tickerData = yf.Ticker(stockSymbol)
    # get info for given date 
    tickerDf = tickerData.history(period='1d' ,start=startDate,end=endDate)
    # display logo, name, and symbol of company
    st.image(tickerData.info["logo_url"], width=150)
    st.write("  " + "## " + tickerData.info["longName"] + " (**" + stockSymbol + "**)")
    # display charts of closing price and trading volume
    st.write("### Closing Price")
    st.line_chart(tickerDf.Close)
    st.write("### Volume")
    st.line_chart(tickerDf.Volume)
    # display stock info dataframe
    st.table(tickerDf)
else:
    st.write("## Pick a stock and date range to see information about that security.")
