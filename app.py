import streamlit as st
imporat requests
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

    st.error(f"Reached the maximum number of retries. Unable to fetch Reddit stocks.")
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

# Button to fetch and display Reddit stocks
if st.button('Fetch Reddit Stocks'):
    reddit_stocks = get_reddit_stocks(selected_date)
    if reddit_stocks is not None:
        st.header('Top 50 Stocks Discussed on Wallstreetbets')
        with st.container():
            for stock in reddit_stocks:
                st.text(f"Ticker: {stock.get('ticker', 'N/A')} | Comments: {stock.get('no_of_comments', 'N/A')} | Sentiment: ")
                if stock.get('sentiment') == 'Bullish':
                    st.markdown(f"<font color='green'>{stock['sentiment']} ({stock.get('sentiment_score', 0.0):.2f})</font>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<font color='red'>{stock['sentiment']} ({stock.get('sentiment_score', 0.0):.2f})</font>", unsafe_allow_html=True)
                st.text("")

# Button to fetch and display TTM Squeeze stocks
if st.button('Fetch TTM Squeeze Stocks'):
    ttm_squeeze_stocks = get_ttm_squeeze_stocks(selected_date)
    if ttm_squeeze_stocks is not None:
        st.header('TTM Squeeze Stocks')
        with st.container():
            for stock in ttm_squeeze_stocks:
                st.text(f"Date: {stock.get('date', 'N/A')} | In Squeeze: {stock.get('in_squeeze', 'N/A')} | Days in Squeeze: {stock.get('no_of_days_in_squeeze', 'N/A')} | Days out of Squeeze: {stock.get('no_of_days_out_of_squeeze', 'N/A')}")
                if stock.get('in_squeeze'):
                    st.markdown("<font color='green'>In Squeeze</font>", unsafe_allow_html=True)
                else:
                    st.markdown("<font color='red'>Out of Squeeze</font>", unsafe_allow_html=True)
                st.text("")

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
