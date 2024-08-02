import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import schedule
import time

Base = declarative_base()

class StockData(Base):
    __tablename__ = 'stock_data'
    id = Column(Integer, primary_key=True)
    ticker = Column(String)
    date = Column(Date)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)

engine = create_engine('sqlite:///stocks.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1d")
    return hist

def save_to_db(ticker, data):
    for date, row in data.iterrows():
        stock_entry = StockData(
            ticker=ticker,
            date=date,
            open=row['Open'],
            high=row['High'],
            low=row['Low'],
            close=row['Close'],
            volume=row['Volume']
        )
        session.add(stock_entry)
    session.commit()

def fetch_and_save_all_stocks():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'BABA', 'V',
               'IBM', 'ORCL', 'CSCO', 'AMD', 'INTC', 'BA', 'SBUX','UDMY', 'WMT']
    
    for ticker in tickers:
        data = fetch_stock_data(ticker)
        save_to_db(ticker, data)
        print(f"Data for {ticker} saved to database.")

def job():
    fetch_and_save_all_stocks()

# Schedule the job to run daily
schedule.every().day.at("18:00").do(job)

# Run the job once immediately for testing
job()

while True:
    schedule.run_pending()
    time.sleep(1)
