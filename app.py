# !pip install streamlit
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf 
from ta.volatility import BollingerBands
from ta.trend import MACD
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator

# for more about ta liabrary --> https://github.com/bukosabino/ta
#https://technical-analysis-library-in-python.readthedocs.io/en/latest/

#defining ticker variables
#Bitcoin = 'BTC-USD'
#Ethereum = 'ETH-USD'
#Ripple = 'XRP-USD'
#BitcoinCash = 'BCH-USD'

##################
# Set up wallet #
##################
import streamlit as st

# Import the functions from ethereum.py
from ethereum import w3, generate_account, get_balance, send_transaction
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# Streamlit application headings
st.markdown("# Crypto Wallet Dashboard!")

# Generate the Ethereum account
account = generate_account(w3)


##################
# Set up sidebar for Crypto selection #
##################

# Add in location to select image.

option = st.sidebar.selectbox('Select one symbol', ( 'BTC-USD', 'ETH-USD','XRP-USD','BCH-USD'))

##################
# Set up sidebar for time period selection #
##################

import datetime

today = datetime.date.today()
before = today - datetime.timedelta(days=700)
start_date = st.sidebar.date_input('Start date', before)
end_date = st.sidebar.date_input('End date', today)

if start_date > end_date:
#    st.sidebar.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
    st.sidebar.error('Error: End date must fall after start date.')
#else:
    
##############################
# Set up sidebar for wallet #
#############################

st.write("         ")
accounts = w3.eth.accounts
address = st.sidebar.selectbox("Account Address", options=accounts)

# show wallet account balance
st.text("\n")
st.sidebar.write("Account Balance in Ethereum:")


# Call the get_balance function and write the account balance to the screen
ether_balance = get_balance(w3, address)
st.sidebar.write(ether_balance)

##############################
# send Ether between accounts #
#############################

st.sidebar.markdown("An Ethereum Transaction")

# Create inputs for the receiver address and ether amount
sender = st.sidebar.text_input("Input the sender address")
receiver = st.sidebar.text_input("Input the receiver address")
ether = st.sidebar.number_input("Input the amount of ether")

# Create a button that calls the `send_transaction` function and returns the transaction hash
if st.sidebar.button("Send Transaction"):

    transaction_hash = send_transaction(w3, account, receiver, ether)

    # Display the Etheremum Transaction Hash
    st.sidebar.text("\n")
    st.sidebar.markdown("Ethereum Transaction Hash:")

    st.sidebar.write(transaction_hash)

##############
# Stock data #
##############

# https://technical-analysis-library-in-python.readthedocs.io/en/latest/ta.html#momentum-indicators

df = yf.download(option,start= start_date,end= end_date, progress=False)

indicator_bb = BollingerBands(df['Close'])

bb = df
bb['bb_h'] = indicator_bb.bollinger_hband()
bb['bb_l'] = indicator_bb.bollinger_lband()
bb = bb[['Close','bb_h','bb_l']]

macd = MACD(df['Close']).macd()

rsi = RSIIndicator(df['Close']).rsi()

ema = EMAIndicator(df['Close'],window=20).ema_indicator().fillna(0)


###################
# Set up main app #
###################

st.write('Stock Bollinger Bands')

st.line_chart(bb)

progress_bar = st.progress(0)

# https://share.streamlit.io/daniellewisdl/streamlit-cheat-sheet/app.py

st.write('Stock Moving Average Convergence Divergence (MACD)')
st.area_chart(macd)

st.write('Stock RSI ')
st.line_chart(rsi)

st.write('Stock EMA 20 ')
st.line_chart(ema)

st.write('Recent data ')
st.dataframe(df.tail(10))


################
# Download csv #
################

import base64
from io import BytesIO

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="download.xlsx">Download excel file</a>' # decode b'abc' => abc

st.markdown(get_table_download_link(df), unsafe_allow_html=True)










