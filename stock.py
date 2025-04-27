import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Function to fetch stock data
def fetch_stock_data(ticker, start_date, end_date):
    try:
        stock = yf.download(ticker, start=start_date, end=end_date)
        if stock.empty:
            print("Error: No data found for the given ticker symbol and date range.")
            return None
        stock.fillna(method='ffill', inplace=True)  # Handle missing values
        return stock
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None

# Function to calculate moving averages
def calculate_moving_average(data, window=50):
    data[f'{window}-Day MA'] = data['Close'].rolling(window=window).mean()
    return data

# Function to plot stock trends
def plot_stock_data(stock, ticker):
    plt.figure(figsize=(12, 6))
    plt.plot(stock.index, stock['Close'], label='Closing Price', color='blue', linewidth=2)
    
    if '50-Day MA' in stock.columns:
        plt.plot(stock.index, stock['50-Day MA'], label='50-Day Moving Average', color='red', linestyle='dashed')
    if '200-Day MA' in stock.columns:
        plt.plot(stock.index, stock['200-Day MA'], label='200-Day Moving Average', color='green', linestyle='dashed')
    
    plt.xlabel('Date')
    plt.ylabel('Stock Price')
    plt.title(f'{ticker} Stock Price Analysis')
    plt.legend()
    plt.grid(True)
    plt.show()

# Validate date input
def validate_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please enter in YYYY-MM-DD format.")
        return None

# User Input for stock symbol and dates
ticker = input("Enter stock ticker symbol (e.g., AAPL, TSLA): ").upper()

start_date = None
end_date = None

while start_date is None:
    start_date = validate_date(input("Enter start date (YYYY-MM-DD): "))

while end_date is None:
    end_date = validate_date(input("Enter end date (YYYY-MM-DD): "))

# Fetch and analyze stock data
stock_data = fetch_stock_data(ticker, str(start_date), str(end_date))

if stock_data is not None:
    stock_data = calculate_moving_average(stock_data, 50)
    stock_data = calculate_moving_average(stock_data, 200)
    plot_stock_data(stock_data, ticker)