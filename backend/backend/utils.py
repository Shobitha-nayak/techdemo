# backend/utils.py

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from .models import StockData

def fetch_stock_data(ticker, period="1d", interval="1h"):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period, interval=interval)
        print(f"Fetched data for {ticker}:")
        print(hist)
        return hist
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()

def save_to_db(ticker, data):
    if data.empty:
        print(f"No data to save for {ticker}")
        return

    existing_dates = set(StockData.objects.filter(ticker=ticker).values_list('date', flat=True))
    print(f"Existing dates for {ticker}: {existing_dates}")

    for date, row in data.iterrows():
        date_value = date.date()  # Ensure date is in the correct format
        if date_value not in existing_dates:
            print(f"Saving data for {ticker} on {date_value}")
            StockData.objects.create(
                ticker=ticker,
                date=date_value,
                open=row['Open'],
                high=row['High'],
                low=row['Low'],
                close=row['Close'],
                volume=row['Volume']
            )
            existing_dates.add(date_value)
        else:
            print(f"Data for {ticker} on {date_value} already exists")

def calculate_percentage_change(ticker, start_date, end_date):
    recent_data = StockData.objects.filter(
        ticker=ticker,
        date__gte=start_date,
        date__lte=end_date
    ).order_by('date')

    if not recent_data.exists():
        return None

    old_price = recent_data.first().close
    new_price = recent_data.last().close
    percentage_change = ((new_price - old_price) / old_price) * 100

    return round(percentage_change, 2) if percentage_change is not None else 0

def generate_daily_opening_closing_price_report(ticker):
    results = StockData.objects.filter(ticker=ticker).order_by('-date')
    data = [
        {
            'date': entry.date,
            'open': entry.open,
            'close': entry.close,
            'ticker': entry.ticker
        }
        for entry in results
    ]
    return data

def generate_kpi_report(ticker):
    daily_report = StockData.objects.filter(ticker=ticker).order_by('-date')
    daily_closing_price = daily_report.first().close if daily_report.exists() else "No data"
    
    return {
        "ticker": ticker,
        "daily_closing_price": daily_closing_price,
        "24h_change": calculate_percentage_change(ticker, datetime.now() - timedelta(days=1), datetime.now()) or "Not enough data",
        "30d_change": calculate_percentage_change(ticker, datetime.now() - timedelta(days=30), datetime.now()) or "Not enough data",
        "1y_change": calculate_percentage_change(ticker, datetime.now() - timedelta(days=365), datetime.now()) or "Not enough data"
    }

def get_top_gainers_losers_last_24h():
    end_date = datetime.now()
    start_date = end_date - timedelta(hours=24)

    recent_data = StockData.objects.filter(
        date__gte=start_date,
        date__lte=end_date
    )

    if not recent_data.exists():
        return {"top_gainers": [], "top_losers": []}

    data = [
        {
            'ticker': record.ticker,
            'date': record.date,
            'open': record.open,
            'close': record.close
        }
        for record in recent_data
    ]

    df = pd.DataFrame(data)
    df['change_percentage'] = ((df['close'] - df['open']) / df['open']) * 100

    df_latest = df.groupby('ticker').apply(lambda x: x.sort_values('date').iloc[-1]).reset_index(drop=True)

    top_gainers = df_latest.nlargest(5, 'change_percentage')
    top_losers = df_latest.nsmallest(5, 'change_percentage')

    return {
        "top_gainers": top_gainers.to_dict(orient='records'),
        "top_losers": top_losers.to_dict(orient='records')
    }
