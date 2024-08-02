from prometheus_client import start_http_server, Gauge
import sqlite3
import time

# Define the metrics
open_gauge = Gauge('stock_open_price', 'The opening price of the stock', ['ticker'])
high_gauge = Gauge('stock_high_price', 'The highest price of the stock', ['ticker'])
low_gauge = Gauge('stock_low_price', 'The lowest price of the stock', ['ticker'])
close_gauge = Gauge('stock_close_price', 'The closing price of the stock', ['ticker'])
week_high_gauge = Gauge('stock_week_high_price', 'The weekly high price of the stock', ['ticker'])
week_low_gauge = Gauge('stock_week_low_price', 'The weekly low price of the stock', ['ticker'])
month_high_gauge = Gauge('stock_month_high_price', 'The monthly high price of the stock', ['ticker'])
month_low_gauge = Gauge('stock_month_low_price', 'The monthly low price of the stock', ['ticker'])
market_cap_gauge = Gauge('stock_market_cap', 'The market capitalization of the stock', ['ticker'])
percentage_change_gauge = Gauge('stock_percentage_change', 'The percentage change value of the stock', ['ticker'])

def collect_metrics():
    # Connect to SQLite
    conn = sqlite3.connect('stocks.db')
    cur = conn.cursor()
    
    # Query to get the stock data
    cur.execute('''
        SELECT ticker, date, open, high, low, close, volume
        FROM stock_data;
    ''')
    rows = cur.fetchall()
    
    # Process each row to update metrics
    for row in rows:
        ticker = row[0]
        open_price = row[2]
        high_price = row[3]
        low_price = row[4]
        close_price = row[5]
        
        # For simplicity, we'll set the weekly and monthly high/low to the same values as daily for this example.
        # You can modify this according to how you track these values.
        week_high = high_price
        week_low = low_price
        month_high = high_price
        month_low = low_price
        
        # Set the metrics with the column data
        open_gauge.labels(ticker=ticker).set(open_price)
        high_gauge.labels(ticker=ticker).set(high_price)
        low_gauge.labels(ticker=ticker).set(low_price)
        close_gauge.labels(ticker=ticker).set(close_price)
        week_high_gauge.labels(ticker=ticker).set(week_high)
        week_low_gauge.labels(ticker=ticker).set(week_low)
        month_high_gauge.labels(ticker=ticker).set(month_high)
        month_low_gauge.labels(ticker=ticker).set(month_low)
        
        # Market cap and percentage change need additional calculations or data
        # For now, we'll set them to zero
        market_cap_gauge.labels(ticker=ticker).set(0)
        percentage_change_gauge.labels(ticker=ticker).set(0)

    cur.close()
    conn.close()

if __name__ == '__main__':
    start_http_server(7878)
    while True:
        collect_metrics()
        time.sleep(60)  # Update metrics every 60 seconds
