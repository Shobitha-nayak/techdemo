from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from django.conf import settings
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from .models import StockData
from prometheus_client import Gauge

# Define metrics for Prometheus
gauge = Gauge('stock_price_change_percentage', 'Stock price change percentage', ['ticker'])

# Fetch stock data from Yahoo Finance
def fetch_stock_data(ticker, period="1d", interval="24h"):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period, interval=interval)
        return hist
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()

# Save data to the database
def save_to_db(ticker, data):
    if data.empty:
        print(f"No data to save for {ticker}")
        return

    existing_dates = StockData.objects.filter(ticker=ticker).values_list('date', flat=True)
    existing_dates = set(existing_dates)

    new_entries = []
    for date, row in data.iterrows():
        date_value = timezone.make_aware(date)  # Ensure datetime is timezone-aware
        if date_value not in existing_dates:
            stock_entry = StockData(
                ticker=ticker,
                date=date_value,
                open=row['Open'],
                high=row['High'],
                low=row['Low'],
                close=row['Close'],
                volume=row['Volume']
            )
            new_entries.append(stock_entry)

    StockData.objects.bulk_create(new_entries)

# Calculate percentage change
def calculate_percentage_change(ticker, start_date, end_date):
    if start_date.tzinfo is None:
        start_date = timezone.make_aware(start_date)
    if end_date.tzinfo is None:
        end_date = timezone.make_aware(end_date)

    recent_data = StockData.objects.filter(
        ticker=ticker,
        date__range=(start_date, end_date)
    ).order_by('date')

    if recent_data.count() < 2:
        return None

    old_price = recent_data.first().close
    new_price = recent_data.last().close
    percentage_change = ((new_price - old_price) / old_price) * 100

    return round(percentage_change, 2) if percentage_change is not None else 0

# Generate KPI report
def generate_kpi_report(ticker):
    daily_report = generate_daily_opening_closing_price_report(ticker)
    return {
        "ticker": ticker,
        "daily_closing_price": daily_report[-1]['close'] if daily_report else "No data",
        "24h_change": calculate_percentage_change(ticker, timezone.now() - timedelta(days=1), timezone.now()) or "Not enough data",
        "30d_change": calculate_percentage_change(ticker, timezone.now() - timedelta(days=30), timezone.now()) or "Not enough data",
        "1y_change": calculate_percentage_change(ticker, timezone.now() - timedelta(days=365), timezone.now()) or "Not enough data"
    }

# Generate daily opening and closing price report
def generate_daily_opening_closing_price_report(ticker):
    results = StockData.objects.filter(ticker=ticker).order_by('-date')
    data = []
    for entry in results:
        data.append({
            'date': entry.date,
            'open': entry.open,
            'close': entry.close,
            'ticker': entry.ticker
        })
    return pd.DataFrame(data).to_dict(orient='records')

# Get top gainers and losers in the last 24 hours
def get_top_gainers_losers_last_24h():
    end_date = timezone.now()
    start_date = end_date - timedelta(hours=24)

    if start_date.tzinfo is None:
        start_date = timezone.make_aware(start_date)
    if end_date.tzinfo is None:
        end_date = timezone.make_aware(end_date)

    recent_data = StockData.objects.filter(date__range=(start_date, end_date))

    if not recent_data:
        return {"top_gainers": [], "top_losers": []}

    data = []
    for record in recent_data:
        data.append({
            'ticker': record.ticker,
            'date': record.date,
            'open': record.open,
            'close': record.close
        })

    df = pd.DataFrame(data)
    df['change_percentage'] = ((df['close'] - df['open']) / df['open']) * 100

    df_latest = df.groupby('ticker').apply(lambda x: x.sort_values('date').iloc[-1]).reset_index(drop=True)

    top_gainers = df_latest.nlargest(5, 'change_percentage')
    top_losers = df_latest.nsmallest(5, 'change_percentage')

    return {
        "top_gainers": top_gainers.to_dict(orient='records'),
        "top_losers": top_losers.to_dict(orient='records')
    }

# Check for stock alerts
def check_alerts():
    tickers = StockData.objects.values_list('ticker', flat=True).distinct()
    alerts = []
    for ticker in tickers:
        change_24h = calculate_percentage_change(ticker, timezone.now() - timedelta(days=1), timezone.now())
        if change_24h is not None and abs(change_24h) >= settings.ALERT_THRESHOLD:
            alerts.append({
                'ticker': ticker,
                '24h_change': change_24h,
                'alert_message': f"{ticker} has changed by {change_24h}% in the last 24 hours!"
            })
    return alerts

# Send alerts (e.g., via email or other means)
def send_alerts():
    alerts = check_alerts()
    for alert in alerts:
        send_mail(
            subject=f"Stock Alert: {alert['ticker']}",
            message=alert['alert_message'],
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ALERT_RECIPIENT_EMAIL],
        )

# Expose metrics for Prometheus
def expose_metrics(request):
    for ticker in StockData.objects.values_list('ticker', flat=True).distinct():
        change_24h = calculate_percentage_change(ticker, timezone.now() - timedelta(days=1), timezone.now())
        gauge.labels(ticker=ticker).set(change_24h)
    return HttpResponse("Metrics exposed")

# Django view functions
def index(request):
    tickers = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
        'META', 'NVDA', 'NFLX', 'BABA', 'V',
        'IBM', 'ORCL', 'CSCO', 'AMD', 'INTC',
        'NVDA', 'BA', 'SBUX', 'UDMY', 'WMT'
    ]
    reports = []
    for ticker in tickers:
        reports.append(generate_kpi_report(ticker))
    top_gainers_losers_24h = get_top_gainers_losers_last_24h()
    return render(request, 'index.html', {'reports': reports, 'top_gainers_losers_24h': top_gainers_losers_24h})

def api_kpi(request, ticker):
    report = generate_kpi_report(ticker)
    return JsonResponse(report)

def api_top_gainers_losers(request):
    top_gainers_losers_24h = get_top_gainers_losers_last_24h()
    return JsonResponse(top_gainers_losers_24h)

def api_alerts(request):
    alerts = check_alerts()
    return JsonResponse({'alerts': alerts})
