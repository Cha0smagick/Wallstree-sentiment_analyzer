import streamlit as st
import requests
import time

# Function to fetch top 50 stocks discussed on Wallstreetbets
def get_reddit_stocks(date=None, max_retries=3):
    url = 'https://tradestie.com/api/v1/apps/reddit'
    if date:
        url += f'?date={date}'
    
    retries = 0
    while retries < max_retries:
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            return data
        elif response.status_code == 429:
            st.warning(f"Rate limit exceeded. Retrying in 5 seconds. Retry attempt: {retries + 1}/{max_retries}")
            time.sleep(5)
            retries += 1
        else:
            st.error(f"Error fetching Reddit stocks. Status code: {response.status_code}")
            return None

    st.error(f"Reached maximum number of retries. Unable to fetch Reddit stocks.")
    return None

# Function to fetch TTM Squeeze stocks
def get_ttm_squeeze_stocks(date=None):
    url = f'https://tradestie.com/api/v1/apps/ttm-squeeze-stocks?date={date}'
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error(f"Error fetching TTM Squeeze stocks. Status code: {response.status_code}")
        return None

# Streamlit UI
st.title('Wallstreetbets & TTM Squeeze Stocks')

# Get date from user
selected_date = st.text_input('Enter date (yyyy-mm-dd):', '')

# Fetch and display Reddit stocks
reddit_stocks = get_reddit_stocks(selected_date)
if reddit_stocks is not None:
    st.header('Top 50 Stocks Discussed on Wallstreetbets')
    st.table(reddit_stocks)

# Fetch and display TTM Squeeze stocks
ttm_squeeze_stocks = get_ttm_squeeze_stocks(selected_date)
if ttm_squeeze_stocks is not None:
    st.header('TTM Squeeze Stocks')
    st.table(ttm_squeeze_stocks)
