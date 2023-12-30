import streamlit as st
import requests
import time
import pandas as pd

# Function to fetch top 25 stocks discussed on Wallstreetbets
def get_reddit_stocks(date=None, max_retries=3, limit=25):
    url = 'https://tradestie.com/api/v1/apps/reddit'
    if date:
        url += f'?date={date}'
    
    retries = 0
    while retries < max_retries:
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            return data[:limit]  # Limit results to the top 25
        elif response.status_code == 429:
            retry_message = st.empty()
            retry_message.warning(f"Rate limit exceeded. Retrying in 2 minutes. Retry attempt: {retries + 1}/{max_retries}")
            
            # Countdown timer
            for i in range(120, 0, -1):
                time.sleep(1)
                retry_message.warning(f"Retrying in {i} seconds...")
            
            retries += 1
        else:
            st.error(f"Error fetching Reddit stocks. Status code: {response.status_code}")
            return None

    st.error(f"Reached the maximum number of retries. Unable to fetch Reddit stocks.")
    return None

# Function to fetch top 25 TTM Squeeze stocks
def get_ttm_squeeze_stocks(date=None, limit=25):
    if not date:
        st.warning("Please enter a date before fetching TTM Squeeze stocks.")
        return None

    url = f'https://tradestie.com/api/v1/apps/ttm-squeeze-stocks?date={date}'
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()
        return data[:limit]  # Limit results to the top 25
    else:
        st.error(f"Error fetching TTM Squeeze stocks. Status code: {response.status_code}")
        return None

# Streamlit UI
st.title('Wallstreetbets & TTM Squeeze Stocks')

# Get date from user
selected_date = st.text_input('Enter date (yyyy-mm-dd):', '')

# Validate if a date is entered
if not selected_date:
    st.warning("Please enter a date before fetching stocks.")
else:
    # Button to fetch and display Reddit stocks
    if st.button('Fetch Top 25 Reddit Stocks'):
        reddit_stocks = get_reddit_stocks(selected_date)
        if reddit_stocks is not None:
            st.header('Top 25 Stocks Discussed on Wallstreetbets')
            table_data = []
            for stock in reddit_stocks:
                table_data.append({
                    'Ticker': stock.get('ticker', 'N/A'),
                    'Comments': stock.get('no_of_comments', 'N/A'),
                    'Sentiment': f"{stock.get('sentiment', 'N/A')} ({stock.get('sentiment_score', 0.0):.2f})"
                })
            df_reddit = pd.DataFrame(table_data)
            st.dataframe(df_reddit.style.applymap(lambda x: 'color: green' if x == 'N/A' else 'color: red', subset=['Ticker', 'Comments']).applymap(lambda x: f'color: {"yellow" if "N/A" in x else "green" if float(x.split("(")[1].split(")")[0]) > 0 else "red"}', subset=['Sentiment']))

    # Button to fetch and display TTM Squeeze stocks
    if st.button('Fetch Top 25 TTM Squeeze Stocks for Date'):
        ttm_squeeze_stocks = get_ttm_squeeze_stocks(selected_date)
        if ttm_squeeze_stocks is not None:
            st.header('Top 25 TTM Squeeze Stocks')
            table_data = []
            for stock in ttm_squeeze_stocks:
                table_data.append({
                    'Date': stock.get('date', 'N/A'),
                    'In Squeeze': stock.get('in_squeeze', 'N/A'),
                    'Days in Squeeze': stock.get('no_of_days_in_squeeze', 'N/A'),
                    'Days out of Squeeze': stock.get('no_of_days_out_of_squeeze', 'N/A'),
                    'Status': 'In Squeeze' if stock.get('in_squeeze') else 'Out of Squeeze'
                })
            df_ttm_squeeze = pd.DataFrame(table_data)
            st.dataframe(df_ttm_squeeze.style.applymap(lambda x: 'color: green' if x == 'N/A' else 'color: red', subset=['Date', 'In Squeeze', 'Days in Squeeze', 'Days out of Squeeze']).applymap(lambda x: 'color: yellow' if x == 'N/A' else 'color: green' if x else 'color: red', subset=['Status']))

# Apply dark background without scrollbars
st.markdown(
    """
    <style>
        body {
            background-color: #121212;
            color: #FFFFFF;
            overflow-y: hidden;
        }
        .stContainer {
            background-color: #333333;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)
