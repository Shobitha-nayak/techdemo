# backend/backend/scheduler.py

import schedule
import threading
import time
from .data_ingestion import fetch_stock_data, save_to_db

def job():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'BABA', 'V', 'IBM', 'ORCL', 'CSCO', 'AMD', 'INTC', 'BA', 'SBUX','UDMY', 'WMT']
    for ticker in tickers:
        data = fetch_stock_data(ticker)
        save_to_db(ticker, data)

schedule.every().day.at("00:00").do(job)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_schedule).start()
