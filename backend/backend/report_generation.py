# backend/backend/report_generation.py

import pandas as pd
from datetime import datetime, timedelta
from .models import StockData
from django.db.models import F, FloatField, ExpressionWrapper

def calculate_percentage_change(ticker, start_date, end_date):
    recent_data = StockData.objects.filter(
        ticker=ticker,
        date__gte=start_date,
        date__lte=end_date
    ).order_by('date')

    if len(recent_data) < 2:
        return None

    old_price = recent_data.first().close
    new_price = recent_data.last().close
    percentage_change = ((new_price - old_price) / old_price) * 100

    return round(percentage_change, 2) if percentage_change is not None else 0

def generate_kpi_report(ticker):
    daily_report = generate_daily_opening_closing_price_report(ticker)
    return {
        "ticker": ticker,
        "daily_closing_price": daily_report[-1]['close'] if daily_report else "No data",
        "24h_change": calculate_percentage_change(ticker, datetime.now() - timedelta(days=1), datetime.now()) or "Not enough data",
        "30d_change": calculate_percentage_change(ticker, datetime.now() - timedelta(days=30), datetime.now()) or "Not enough data",
        "1y_change": calculate_percentage_change(ticker, datetime.now() - timedelta(days=365), datetime.now()) or "Not enough data"
    }

def generate_daily_opening_closing_price_report(ticker):
    results = StockData.objects.filter(ticker=ticker).order_by('-date')
    data = [{
        'date': entry.date,
        'open': entry.open,
        'close': entry.close,
        'ticker': entry.ticker
    } for entry in results]
    return data

def get_top_gainers_losers_last_24h():
    now = datetime.now()
    start_time = now - timedelta(days=1)
    
    # Get all stock data for the last 24 hours
    data_last_24h = StockData.objects.filter(date__gte=start_time)
    
    if not data_last_24h.exists():
        return {'top_gainers': [], 'top_losers': []}
    
    # Calculate the percentage change
    data_last_24h = data_last_24h.annotate(
        percentage_change=ExpressionWrapper(
            (F('close') - F('open')) * 100 / F('open'),
            output_field=FloatField()
        )
    ).order_by('-percentage_change')
    
    # Find top gainers and losers
    top_gainers = list(data_last_24h[:5].values('ticker', 'percentage_change'))
    top_losers = list(data_last_24h.reverse()[:5].values('ticker', 'percentage_change'))
    
    return {'top_gainers': top_gainers, 'top_losers': top_losers}
