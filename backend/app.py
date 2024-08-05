# # from flask import Flask, jsonify, render_template
# # import yfinance as yf
# # import pandas as pd
# # from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
# # from sqlalchemy.orm import declarative_base, sessionmaker
# # from datetime import datetime, timedelta
# # import schedule
# # import time
# # import threading
# # from flask_cors import CORS

# # # Define database schema
# # Base = declarative_base()

# # class StockData(Base):
# #     __tablename__ = 'stock_data'
# #     id = Column(Integer, primary_key=True)
# #     ticker = Column(String)
# #     date = Column(DateTime)
# #     open = Column(Float)
# #     high = Column(Float)
# #     low = Column(Float)
# #     close = Column(Float)
# #     volume = Column(Integer)

# # # Create SQLite engine and session
# # engine = create_engine('sqlite:///stocks.db')
# # Base.metadata.create_all(engine)
# # Session = sessionmaker(bind=engine)
# # session = Session()

# # app = Flask(__name__)
# # CORS(app, resource={"/api/*": {"origin": "*"}})

# # def fetch_stock_data(ticker, period="1d", interval="1h"):
# #     try:
# #         stock = yf.Ticker(ticker)
# #         hist = stock.history(period=period, interval=interval)
# #         return hist
# #     except Exception as e:
# #         print(f"Error fetching data for {ticker}: {e}")
# #         return pd.DataFrame()

# # def save_to_db(ticker, data):
# #     if data.empty:
# #         print(f"No data to save for {ticker}")
# #         return

# #     existing_dates = session.query(StockData.date).filter(StockData.ticker == ticker).all()
# #     existing_dates = {d[0] for d in existing_dates}

# #     for date, row in data.iterrows():
# #         date_value = date
# #         if date_value not in existing_dates:
# #             stock_entry = StockData(
# #                 ticker=ticker,
# #                 date=date_value,
# #                 open=row['Open'],
# #                 high=row['High'],
# #                 low=row['Low'],
# #                 close=row['Close'],
# #                 volume=row['Volume']
# #             )
# #             session.add(stock_entry)
# #             existing_dates.add(date_value)

# #     session.commit()

# # def calculate_percentage_change(ticker, start_date, end_date):
# #     recent_data = session.query(StockData).filter(
# #         StockData.ticker == ticker,
# #         StockData.date >= start_date,
# #         StockData.date <= end_date
# #     ).order_by(StockData.date).all()

# #     if len(recent_data) < 2:
# #         return None

# #     old_price = recent_data[0].close
# #     new_price = recent_data[-1].close
# #     percentage_change = ((new_price - old_price) / old_price) * 100

# #     return round(percentage_change, 2) if percentage_change is not None else 0


# # def generate_kpi_report(ticker):
# #     daily_report = generate_daily_opening_closing_price_report(ticker)
# #     return {
# #         "ticker": ticker,
# #         "daily_closing_price": daily_report[-1]['close'] if daily_report else "No data",
# #         "24h_change": calculate_percentage_change(ticker, datetime.now() - timedelta(days=1), datetime.now()) or "Not enough data",
# #         "30d_change": calculate_percentage_change(ticker, datetime.now() - timedelta(days=30), datetime.now()) or "Not enough data",
# #         "1y_change": calculate_percentage_change(ticker, datetime.now() - timedelta(days=365), datetime.now()) or "Not enough data"
# #     }

# # def generate_daily_opening_closing_price_report(ticker):
# #     results = session.query(StockData).filter_by(ticker=ticker).order_by(StockData.date.desc()).all()
# #     data = []
# #     for entry in results:
# #         data.append({
# #             'date': entry.date,
# #             'open': entry.open,
# #             'close': entry.close,
# #             'ticker': entry.ticker
# #         })
# #     return pd.DataFrame(data).to_dict(orient='records')

# # def get_top_gainers_losers_last_24h():
# #     end_date = datetime.now()
# #     start_date = end_date - timedelta(hours=24)

# #     recent_data = session.query(StockData).filter(
# #         StockData.date >= start_date,
# #         StockData.date <= end_date
# #     ).all()

# #     if not recent_data:
# #         return {"top_gainers": [], "top_losers": []}

# #     data = []
# #     for record in recent_data:
# #         data.append({
# #             'ticker': record.ticker,
# #             'date': record.date,
# #             'open': record.open,
# #             'close': record.close
# #         })

# #     df = pd.DataFrame(data)
# #     df['change_percentage'] = ((df['close'] - df['open']) / df['open']) * 100

# #     # Group by ticker and get the latest entry for each ticker
# #     df_latest = df.groupby('ticker').apply(lambda x: x.sort_values('date').iloc[-1]).reset_index(drop=True)

# #     top_gainers = df_latest.nlargest(5, 'change_percentage')
# #     top_losers = df_latest.nsmallest(5, 'change_percentage')

# #     return {
# #         "top_gainers": top_gainers.to_dict(orient='records'),
# #         "top_losers": top_losers.to_dict(orient='records')
# #     }

# # def generate_reports():
# #     tickers = [
# #         'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
# #         'META', 'NVDA', 'NFLX', 'BABA', 'V',
# #         'IBM', 'ORCL', 'CSCO', 'AMD', 'INTC',
# #         'NVDA', 'BA', 'UDMY', 'SBUX', 'WMT'
# #     ]
    
# #     reports = {}
# #     for ticker in tickers:
# #         reports[ticker] = generate_kpi_report(ticker)

# #     return reports

# # def job():
# #     tickers = [
# #         'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
# #         'META', 'NVDA', 'NFLX', 'BABA', 'V',
# #         'IBM', 'ORCL', 'CSCO', 'AMD', 'INTC',
# #         'NVDA', 'BA', 'UDMY', 'SBUX', 'WMT'
# #     ]
# #     for ticker in tickers:
# #         print(f"Processing {ticker}...")
# #         data = fetch_stock_data(ticker, period="1d", interval="1h")
# #         save_to_db(ticker, data)

# # @app.route('/')
# # def index():
# #     tickers = [
# #         'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
# #         'META', 'NVDA', 'NFLX', 'BABA', 'V',
# #         'IBM', 'ORCL', 'CSCO', 'AMD', 'INTC',
# #         'NVDA', 'BA', 'UDMY', 'SBUX', 'WMT'
# #     ]
    
# #     reports = generate_reports()
# #     top_gainers_losers_24h = get_top_gainers_losers_last_24h()

# #     # Get current date
# #     now = datetime.now()
    
# #     # Prepare data for daily, weekly, and monthly reports
# #     daily_report_data = {ticker: generate_kpi_report(ticker) for ticker in tickers}
# #     weekly_report_data = {ticker: generate_kpi_report(ticker) for ticker in tickers}  # Update with actual weekly data if necessary
# #     monthly_report_data = {ticker: generate_kpi_report(ticker) for ticker in tickers}  # Update with actual monthly data if necessary

# #     return render_template('index.html', reports=reports, 
# #                            top_gainers_losers_24h=top_gainers_losers_24h, 
# #                            now=now, 
# #                            daily_report=daily_report_data,
# #                            weekly_report=weekly_report_data,
# #                            monthly_report=monthly_report_data)

# # @app.route('/api/kpi/<ticker>')
# # def api_kpi(ticker):
# #     report = generate_kpi_report(ticker)
# #     return jsonify(report)

# # @app.route('/api/top-gainers-losers')
# # def api_top_gainers_losers():
# #     top_gainers_losers_24h = get_top_gainers_losers_last_24h()
# #     return jsonify(top_gainers_losers_24h)

# # def run_scheduler():
# #     while True:
# #         schedule.run_pending()
# #         time.sleep(1)

# # if __name__ == "__main__":
# #     # Schedule the job to run every hour
# #     schedule.every().hour.do(job)

# #     # Run the job once immediately for testing
# #     job()

# #     # Run scheduler in a separate thread
# #     threading.Thread(target=run_scheduler, daemon=True).start()

# #     # Run the Flask app
# #     app.run(debug=True, port=5006)


# from flask import Flask, jsonify, render_template, Response
# import yfinance as yf
# import pandas as pd
# from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
# from sqlalchemy.orm import declarative_base, sessionmaker
# from datetime import datetime, timedelta
# import schedule
# import time
# import threading
# from flask_cors import CORS
# from prometheus_client import generate_latest, Gauge, Counter, Summary

# # Define database schema
# Base = declarative_base()

# class StockData(Base):
#     __tablename__ = 'stock_data'
#     id = Column(Integer, primary_key=True)
#     ticker = Column(String)
#     date = Column(DateTime)
#     open = Column(Float)
#     high = Column(Float)
#     low = Column(Float)
#     close = Column(Float)
#     volume = Column(Integer)

# # Create SQLite engine and session
# engine = create_engine('sqlite:///stocks.db')
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()

# app = Flask(__name__)
# CORS(app, resource={"/api/*": {"origin": "*"}})

# # Prometheus metrics
# REQUEST_COUNT = Counter('request_count', 'Total number of requests')
# FETCH_STOCK_DATA_TIME = Summary('fetch_stock_data_time', 'Time spent fetching stock data')
# STOCK_PRICE_CHANGE = Gauge('stock_price_change', 'Percentage change of the stock price')

# def fetch_stock_data(ticker, period="1d", interval="1h"):
#     try:
#         stock = yf.Ticker(ticker)
#         hist = stock.history(period=period, interval=interval)
#         return hist
#     except Exception as e:
#         print(f"Error fetching data for {ticker}: {e}")
#         return pd.DataFrame()

# def save_to_db(ticker, data):
#     if data.empty:
#         print(f"No data to save for {ticker}")
#         return

#     existing_dates = session.query(StockData.date).filter(StockData.ticker == ticker).all()
#     existing_dates = {d[0] for d in existing_dates}

#     for date, row in data.iterrows():
#         date_value = date
#         if date_value not in existing_dates:
#             stock_entry = StockData(
#                 ticker=ticker,
#                 date=date_value,
#                 open=row['Open'],
#                 high=row['High'],
#                 low=row['Low'],
#                 close=row['Close'],
#                 volume=row['Volume']
#             )
#             session.add(stock_entry)
#             existing_dates.add(date_value)

#     session.commit()

# def calculate_percentage_change(ticker, start_date, end_date):
#     recent_data = session.query(StockData).filter(
#         StockData.ticker == ticker,
#         StockData.date >= start_date,
#         StockData.date <= end_date
#     ).order_by(StockData.date).all()

#     if len(recent_data) < 2:
#         return None

#     old_price = recent_data[0].close
#     new_price = recent_data[-1].close
#     percentage_change = ((new_price - old_price) / old_price) * 100

#     return round(percentage_change, 2) if percentage_change is not None else 0

# def generate_kpi_report(ticker):
#     daily_report = generate_daily_opening_closing_price_report(ticker)
#     percentage_change_24h = calculate_percentage_change(ticker, datetime.now() - timedelta(days=1), datetime.now())
#     percentage_change_30d = calculate_percentage_change(ticker, datetime.now() - timedelta(days=30), datetime.now())
#     percentage_change_1y = calculate_percentage_change(ticker, datetime.now() - timedelta(days=365), datetime.now())
    
#     # Update the Prometheus gauge
#     if percentage_change_24h is not None:
#         STOCK_PRICE_CHANGE.labels(ticker=ticker).set(percentage_change_24h)

#     return {
#         "ticker": ticker,
#         "daily_closing_price": daily_report[-1]['close'] if daily_report else "No data",
#         "24h_change": percentage_change_24h or "Not enough data",
#         "30d_change": percentage_change_30d or "Not enough data",
#         "1y_change": percentage_change_1y or "Not enough data"
#     }

# def generate_daily_opening_closing_price_report(ticker):
#     results = session.query(StockData).filter_by(ticker=ticker).order_by(StockData.date.desc()).all()
#     data = []
#     for entry in results:
#         data.append({
#             'date': entry.date,
#             'open': entry.open,
#             'close': entry.close,
#             'ticker': entry.ticker
#         })
#     return pd.DataFrame(data).to_dict(orient='records')

# def get_top_gainers_losers_last_24h():
#     end_date = datetime.now()
#     start_date = end_date - timedelta(hours=24)

#     recent_data = session.query(StockData).filter(
#         StockData.date >= start_date,
#         StockData.date <= end_date
#     ).all()

#     if not recent_data:
#         return {"top_gainers": [], "top_losers": []}

#     data = []
#     for record in recent_data:
#         data.append({
#             'ticker': record.ticker,
#             'date': record.date,
#             'open': record.open,
#             'close': record.close
#         })

#     df = pd.DataFrame(data)
#     df['change_percentage'] = ((df['close'] - df['open']) / df['open']) * 100

#     # Group by ticker and get the latest entry for each ticker
#     df_latest = df.groupby('ticker').apply(lambda x: x.sort_values('date').iloc[-1]).reset_index(drop=True)

#     top_gainers = df_latest.nlargest(5, 'change_percentage')
#     top_losers = df_latest.nsmallest(5, 'change_percentage')

#     return {
#         "top_gainers": top_gainers.to_dict(orient='records'),
#         "top_losers": top_losers.to_dict(orient='records')
#     }

# def generate_reports():
#     tickers = [
#         'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
#         'META', 'NVDA', 'NFLX', 'BABA', 'V',
#         'IBM', 'ORCL', 'CSCO', 'AMD', 'INTC',
#         'NVDA', 'BA', 'UDMY', 'SBUX', 'WMT'
#     ]
    
#     reports = {}
#     for ticker in tickers:
#         reports[ticker] = generate_kpi_report(ticker)

#     return reports

# def job():
#     tickers = [
#         'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
#         'META', 'NVDA', 'NFLX', 'BABA', 'V',
#         'IBM', 'ORCL', 'CSCO', 'AMD', 'INTC',
#         'NVDA', 'BA', 'UDMY', 'SBUX', 'WMT'
#     ]
#     for ticker in tickers:
#         print(f"Processing {ticker}...")
#         with FETCH_STOCK_DATA_TIME.time():
#             data = fetch_stock_data(ticker, period="1d", interval="1h")
#         save_to_db(ticker, data)

# @app.route('/')
# def index():
#     tickers = [
#         'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
#         'META', 'NVDA', 'NFLX', 'BABA', 'V',
#         'IBM', 'ORCL', 'CSCO', 'AMD', 'INTC',
#         'NVDA', 'BA', 'UDMY', 'SBUX', 'WMT'
#     ]
    
#     reports = generate_reports()
#     top_gainers_losers_24h = get_top_gainers_losers_last_24h()

#     # Get current date
#     now = datetime.now()
    
#     # Prepare data for daily, weekly, and monthly reports
#     daily_report_data = {ticker: generate_kpi_report(ticker) for ticker in tickers}
#     weekly_report_data = {ticker: generate_kpi_report(ticker) for ticker in tickers}  # Update with actual weekly data if necessary
#     monthly_report_data = {ticker: generate_kpi_report(ticker) for ticker in tickers}  # Update with actual monthly data if necessary

#     return render_template('index.html', reports=reports, 
#                            top_gainers_losers_24h=top_gainers_losers_24h, 
#                            now=now, 
#                            daily_report=daily_report_data,
#                            weekly_report=weekly_report_data,
#                            monthly_report=monthly_report_data)

# @app.route('/api/kpi/<ticker>')
# @REQUEST_COUNT.count_exceptions()
# def api_kpi(ticker):
#     report = generate_kpi_report(ticker)
#     return jsonify(report)

# @app.route('/api/top-gainers-losers')
# def api_top_gainers_losers():
#     top_gainers_losers_24h = get_top_gainers_losers_last_24h()
#     return jsonify(top_gainers_losers_24h)

# @app.route('/metrics')
# def metrics():
#     return Response(generate_latest(), mimetype='text/plain')

# def run_scheduler():
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# if __name__ == "__main__":
#     # Schedule the job to run every hour
#     schedule.every().hour.do(job)

#     # Run the job once immediately for testing
#     job()

#     # Run scheduler in a separate thread
#     threading.Thread(target=run_scheduler, daemon=True).start()

#     app.run(debug=True, port=5006)



# from flask import Flask, jsonify, render_template
# import yfinance as yf
# import pandas as pd
# from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
# from sqlalchemy.orm import declarative_base, sessionmaker
# from datetime import datetime, timedelta
# import schedule
# import time
# import threading
# from flask_cors import CORS
# from prometheus_client import start_http_server, Summary, Gauge, Counter, generate_latest

# # Define database schema
# Base = declarative_base()

# class StockData(Base):
#     __tablename__ = 'stock_data'
#     id = Column(Integer, primary_key=True)
#     ticker = Column(String)
#     date = Column(DateTime)
#     open = Column(Float)
#     high = Column(Float)
#     low = Column(Float)
#     close = Column(Float)
#     volume = Column(Integer)

# # Create SQLite engine and session
# engine = create_engine('sqlite:///stocks.db')
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()

# app = Flask(__name__)
# CORS(app, resource={"/api/*": {"origin": "*"}})

# # Prometheus metrics
# REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
# STOCK_PRICE_CHANGE_PERCENTAGE = Gauge('stock_price_change_percentage', 'Stock price change percentage', ['ticker'])

# def fetch_stock_data(ticker, period="1d", interval="1h"):
#     try:
#         stock = yf.Ticker(ticker)
#         hist = stock.history(period=period, interval=interval)
#         return hist
#     except Exception as e:
#         print(f"Error fetching data for {ticker}: {e}")
#         return pd.DataFrame()

# def save_to_db(ticker, data):
#     if data.empty:
#         print(f"No data to save for {ticker}")
#         return

#     existing_dates = session.query(StockData.date).filter(StockData.ticker == ticker).all()
#     existing_dates = {d[0] for d in existing_dates}

#     for date, row in data.iterrows():
#         date_value = date
#         if date_value not in existing_dates:
#             stock_entry = StockData(
#                 ticker=ticker,
#                 date=date_value,
#                 open=row['Open'],
#                 high=row['High'],
#                 low=row['Low'],
#                 close=row['Close'],
#                 volume=row['Volume']
#             )
#             session.add(stock_entry)
#             existing_dates.add(date_value)

#     session.commit()

# @REQUEST_TIME.time()
# def calculate_percentage_change(ticker, start_date, end_date):
#     recent_data = session.query(StockData).filter(
#         StockData.ticker == ticker,
#         StockData.date >= start_date,
#         StockData.date <= end_date
#     ).order_by(StockData.date).all()

#     if len(recent_data) < 2:
#         return None

#     old_price = recent_data[0].close
#     new_price = recent_data[-1].close
#     percentage_change = ((new_price - old_price) / old_price) * 100
#     STOCK_PRICE_CHANGE_PERCENTAGE.labels(ticker=ticker).set(percentage_change)

#     return round(percentage_change, 2) if percentage_change is not None else 0

# def generate_kpi_report(ticker):
#     daily_report = generate_daily_opening_closing_price_report(ticker)
#     return {
#         "ticker": ticker,
#         "daily_closing_price": daily_report[-1]['close'] if daily_report else "No data",
#         "24h_change": calculate_percentage_change(ticker, datetime.now() - timedelta(days=1), datetime.now()) or "Not enough data",
#         "30d_change": calculate_percentage_change(ticker, datetime.now() - timedelta(days=30), datetime.now()) or "Not enough data",
#         "1y_change": calculate_percentage_change(ticker, datetime.now() - timedelta(days=365), datetime.now()) or "Not enough data"
#     }

# def generate_daily_opening_closing_price_report(ticker):
#     results = session.query(StockData).filter_by(ticker=ticker).order_by(StockData.date.desc()).all()
#     data = []
#     for entry in results:
#         data.append({
#             'date': entry.date,
#             'open': entry.open,
#             'close': entry.close,
#             'ticker': entry.ticker
#         })
#     return pd.DataFrame(data).to_dict(orient='records')

# def get_top_gainers_losers_last_24h():
#     end_date = datetime.now()
#     start_date = end_date - timedelta(hours=24)

#     recent_data = session.query(StockData).filter(
#         StockData.date >= start_date,
#         StockData.date <= end_date
#     ).all()

#     if not recent_data:
#         return {"top_gainers": [], "top_losers": []}

#     data = []
#     for record in recent_data:
#         data.append({
#             'ticker': record.ticker,
#             'date': record.date,
#             'open': record.open,
#             'close': record.close
#         })

#     df = pd.DataFrame(data)
#     df['change_percentage'] = ((df['close'] - df['open']) / df['open']) * 100

#     # Group by ticker and get the latest entry for each ticker
#     df_latest = df.groupby('ticker').apply(lambda x: x.sort_values('date').iloc[-1]).reset_index(drop=True)

#     top_gainers = df_latest.nlargest(5, 'change_percentage')
#     top_losers = df_latest.nsmallest(5, 'change_percentage')

#     return {
#         "top_gainers": top_gainers.to_dict(orient='records'),
#         "top_losers": top_losers.to_dict(orient='records')
#     }

# def generate_reports():
#     tickers = [
#         'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
#         'META', 'NVDA', 'NFLX', 'BABA', 'V',
#         'IBM', 'ORCL', 'CSCO', 'AMD', 'INTC',
#         'NVDA', 'BA', 'UDMY', 'SBUX', 'WMT'
#     ]
    
#     reports = {}
#     for ticker in tickers:
#         reports[ticker] = generate_kpi_report(ticker)

#     return reports

# def job():
#     tickers = [
#         'AAPL', 'MSFT', 'GOOGL', 'AMZN','TSLA', 
#         'META', 'NVDA', 'NFLX', 'BABA', 'V',
#         'IBM', 'ORCL', 'CSCO', 'AMD', 'INTC',
#         'NVDA', 'BA', 'UDMY', 'SBUX', 'WMT'
#     ]

#     for ticker in tickers:
#         data = fetch_stock_data(ticker)
#         save_to_db(ticker, data)

# schedule.every().day.at("22:00").do(job)

# @app.route('/api/price_change/<ticker>', methods=['GET'])
# def price_change(ticker):
#     percentage_change = calculate_percentage_change(ticker, datetime.now() - timedelta(days=1), datetime.now())
#     if percentage_change is None:
#         return jsonify({'message': 'Not enough data to calculate percentage change'}), 404
#     return jsonify({'ticker': ticker, '24h_change_percentage': percentage_change})

# @app.route('/api/top_gainers_losers', methods=['GET'])
# def top_gainers_losers():
#     result = get_top_gainers_losers_last_24h()
#     return jsonify(result)

# @app.route('/api/kpi_report/<ticker>', methods=['GET'])
# def kpi_report(ticker):
#     report = generate_kpi_report(ticker)
#     return jsonify(report)

# @app.route('/api/reports', methods=['GET'])
# def reports():
#     all_reports = generate_reports()
#     return jsonify(all_reports)

# @app.route('/metrics', methods=['GET'])
# def metrics():
#     return generate_latest()

# def run_scheduler():
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# if __name__ == '__main__':
#        schedule.every().hour.do(job)
#        job()
#        threading.Thread(target=run_scheduler, daemon=True).start()
#        app.run(debug=True, port=5006)

from flask import Flask, jsonify, render_template, Response
import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timedelta
import schedule
import time
import threading
from flask_cors import CORS
from prometheus_client import generate_latest, Gauge, Counter, Summary
from sqlalchemy.exc import OperationalError, PendingRollbackError
import sqlite3

# Define database schema
Base = declarative_base()

class StockData(Base):
    __tablename__ = 'stock_data'
    id = Column(Integer, primary_key=True)
    ticker = Column(String)
    date = Column(DateTime)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)

# Create SQLite engine and session
engine = create_engine('sqlite:///stocks.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)
CORS(app, resource={"/api/*": {"origin": "*"}})

# Prometheus metrics
REQUEST_COUNT = Counter('request_count', 'Total number of requests')
FETCH_STOCK_DATA_TIME = Summary('fetch_stock_data_time', 'Time spent fetching stock data')
STOCK_PRICE_CHANGE = Gauge('stock_price_change', 'Daily percentage change of the stock price', ['ticker'])


def fetch_stock_data(ticker, period="1d", interval="1h"):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period, interval=interval)
        return hist
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()

def save_to_db(ticker, data, retries=5, delay=1):
    if data.empty:
        print(f"No data to save for {ticker}")
        return

    session = Session()
    existing_dates = session.query(StockData.date).filter(StockData.ticker == ticker).all()
    existing_dates = {d[0] for d in existing_dates}

    for _ in range(retries):
        try:
            for date, row in data.iterrows():
                date_value = date
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
                    session.add(stock_entry)
                    existing_dates.add(date_value)

            session.commit()
            print(f"Data for {ticker} saved successfully.")
            return  # Exit if successful
        except OperationalError as e:
            print(f"Database is locked, retrying... ({_ + 1}/{retries})")
            session.rollback()
            time.sleep(delay)
            delay *= 2  # Exponential backoff
        except PendingRollbackError as e:
            print(f"Pending rollback error, retrying... ({_ + 1}/{retries})")
            session.rollback()
            time.sleep(delay)
            delay *= 2  # Exponential backoff
        finally:
            session.close()

    print(f"Failed to save data for {ticker} after {retries} retries.")

def calculate_percentage_change(ticker, start_date, end_date):
    recent_data = session.query(StockData).filter(
        StockData.ticker == ticker,
        StockData.date >= start_date,
        StockData.date <= end_date
    ).order_by(StockData.date).all()

    if len(recent_data) < 2:
        return None

    old_price = recent_data[0].close
    new_price = recent_data[-1].close
    percentage_change = ((new_price - old_price) / old_price) * 100

    return round(percentage_change, 2) if percentage_change is not None else 0

def generate_kpi_report(ticker):
    daily_report = generate_daily_opening_closing_price_report(ticker)
    percentage_change_24h = calculate_percentage_change(ticker, datetime.now() - timedelta(days=1), datetime.now())
    percentage_change_30d = calculate_percentage_change(ticker, datetime.now() - timedelta(days=30), datetime.now())
    percentage_change_1y = calculate_percentage_change(ticker, datetime.now() - timedelta(days=365), datetime.now())
    if percentage_change_24h is not None:
        STOCK_PRICE_CHANGE.labels(ticker=ticker).set(percentage_change_24h)

    return {
        "ticker": ticker,
        "daily_closing_price": daily_report[-1]['close'] if daily_report else "No data",
        "24h_change": percentage_change_24h or "Not enough data",
        "30d_change": percentage_change_30d or "Not enough data",
        "1y_change": percentage_change_1y or "Not enough data"
    }

def generate_daily_opening_closing_price_report(ticker):
    results = session.query(StockData).filter_by(ticker=ticker).order_by(StockData.date.desc()).all()
    data = []
    for entry in results:
        data.append({
            'date': entry.date,
            'open': entry.open,
            'close': entry.close,
            'ticker': entry.ticker
        })
    return pd.DataFrame(data).to_dict(orient='records')

def get_top_gainers_losers_last_24h():
    end_date = datetime.now()
    start_date = end_date - timedelta(hours=24)

    recent_data = session.query(StockData).filter(
        StockData.date >= start_date,
        StockData.date <= end_date
    ).all()

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

    # Group by ticker and get the latest entry for each ticker
    df_latest = df.groupby('ticker').apply(lambda x: x.sort_values('date').iloc[-1]).reset_index(drop=True)

    top_gainers = df_latest.nlargest(5, 'change_percentage')
    top_losers = df_latest.nsmallest(5, 'change_percentage')

    return {
        "top_gainers": top_gainers.to_dict(orient='records'),
        "top_losers": top_losers.to_dict(orient='records')
    }

def generate_reports():
    tickers = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
        'META', 'NVDA', 'NFLX', 'BABA', 'V',
        'IBM', 'ORCL', 'CSCO', 'AMD', 'INTC',
        'NVDA', 'BA', 'UDMY', 'SBUX', 'WMT'
    ]
    
    reports = {}
    for ticker in tickers:
        reports[ticker] = generate_kpi_report(ticker)

    return reports

def job():
    tickers = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
        'META', 'NVDA', 'NFLX', 'BABA', 'V',
        'IBM', 'ORCL', 'CSCO', 'AMD', 'INTC',
        'NVDA', 'BA', 'UDMY', 'SBUX', 'WMT'
    ]
    for ticker in tickers:
        print(f"Processing {ticker}...")
        with FETCH_STOCK_DATA_TIME.time():
            data = fetch_stock_data(ticker, period="1d", interval="1h")
        save_to_db(ticker, data)

@app.route('/')
def index():
    tickers = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
        'META', 'NVDA', 'NFLX', 'BABA', 'V',
        'IBM', 'ORCL', 'CSCO', 'AMD', 'INTC',
        'NVDA', 'BA', 'UDMY', 'SBUX', 'WMT'
    ]
    
    reports = generate_reports()
    top_gainers_losers_24h = get_top_gainers_losers_last_24h()

    # Get current date
    now = datetime.now()
    
    # Prepare data for daily, weekly, and monthly reports
    daily_report_data = {ticker: generate_kpi_report(ticker) for ticker in tickers}
    weekly_report_data = {ticker: generate_kpi_report(ticker) for ticker in tickers}  # Update with actual weekly data if necessary
    monthly_report_data = {ticker: generate_kpi_report(ticker) for ticker in tickers}  # Update with actual monthly data if necessary

    return render_template('index.html', reports=reports, 
                           top_gainers_losers_24h=top_gainers_losers_24h, 
                           now=now, 
                           daily_report=daily_report_data,
                           weekly_report=weekly_report_data,
                           monthly_report=monthly_report_data)

@app.route('/api/kpi/<ticker>')
@REQUEST_COUNT.count_exceptions()
def api_kpi(ticker):
    report = generate_kpi_report(ticker)
    return jsonify(report)

@app.route('/api/top-gainers-losers')
def api_top_gainers_losers():
    top_gainers_losers_24h = get_top_gainers_losers_last_24h()
    return jsonify(top_gainers_losers_24h)

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Schedule the job to run every hour
    schedule.every().hour.do(job)

    # Run the job once immediately for testing
    job()

    # Run scheduler in a separate thread
    threading.Thread(target=run_scheduler, daemon=True).start()

    app.run(debug=True, port=5006)






# from flask import Flask, jsonify, render_template
# import yfinance as yf
# import pandas as pd
# from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
# from sqlalchemy.orm import declarative_base, sessionmaker
# from datetime import datetime, timedelta
# import schedule
# import time
# import threading
# from flask_cors import CORS


# # Define database schema
# Base = declarative_base()

# class StockData(Base):
#     __tablename__ = 'stock_data'
#     id = Column(Integer, primary_key=True)
#     ticker = Column(String)
#     date = Column(DateTime)
#     open = Column(Float)
#     high = Column(Float)
#     low = Column(Float)
#     close = Column(Float)
#     volume = Column(Integer)

# # Create SQLite engine and session
# engine = create_engine('sqlite:///stocks.db')
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()

# app = Flask(__name__)
# CORS(app)

# def fetch_stock_data(ticker, period="1d", interval="1h"):
#     try:
#         stock = yf.Ticker(ticker)
#         hist = stock.history(period=period, interval=interval)
#         return hist
#     except Exception as e:
#         print(f"Error fetching data for {ticker}: {e}")
#         return pd.DataFrame()

# def save_to_db(ticker, data):
#     if data.empty:
#         print(f"No data to save for {ticker}")
#         return

#     existing_dates = session.query(StockData.date).filter(StockData.ticker == ticker).all()
#     existing_dates = {d[0] for d in existing_dates}

#     for date, row in data.iterrows():
#         date_value = date
#         if date_value not in existing_dates:
#             stock_entry = StockData(
#                 ticker=ticker,
#                 date=date_value,
#                 open=row['Open'],
#                 high=row['High'],
#                 low=row['Low'],
#                 close=row['Close'],
#                 volume=row['Volume']
#             )
#             session.add(stock_entry)
#             existing_dates.add(date_value)

#     session.commit()

# def calculate_percentage_change(ticker, start_date, end_date):
#     recent_data = session.query(StockData).filter(
#         StockData.ticker == ticker,
#         StockData.date >= start_date,
#         StockData.date <= end_date
#     ).order_by(StockData.date).all()

#     if len(recent_data) < 2:
#         return None

#     old_price = recent_data[0].close
#     new_price = recent_data[-1].close
#     percentage_change = ((new_price - old_price) / old_price) * 100

#     return round(percentage_change, 2) if percentage_change is not None else 0

# def generate_kpi_report(ticker):
#     daily_report = generate_daily_opening_closing_price_report(ticker)
#     return {
#         "ticker": ticker,
#         "daily_closing_price": daily_report[-1]['close'] if daily_report else "No data",
#         "24h_change": calculate_percentage_change(ticker, datetime.now() - timedelta(days=1), datetime.now()) or "Not enough data",
#         "30d_change": calculate_percentage_change(ticker, datetime.now() - timedelta(days=30), datetime.now()) or "Not enough data",
#         "1y_change": calculate_percentage_change(ticker, datetime.now() - timedelta(days=365), datetime.now()) or "Not enough data"
#     }

# def generate_daily_opening_closing_price_report(ticker):
#     results = session.query(StockData).filter_by(ticker=ticker).order_by(StockData.date.desc()).all()
#     data = []
#     for entry in results:
#         data.append({
#             'date': entry.date,
#             'open': entry.open,
#             'close': entry.close,
#             'ticker': entry.ticker
#         })
#     return pd.DataFrame(data).to_dict(orient='records')

# def get_top_gainers_losers_last_24h():
#     end_date = datetime.now()
#     start_date = end_date - timedelta(hours=24)

#     recent_data = session.query(StockData).filter(
#         StockData.date >= start_date,
#         StockData.date <= end_date
#     ).all()

#     if not recent_data:
#         return {"top_gainers": [], "top_losers": []}

#     data = []
#     for record in recent_data:
#         data.append({
#             'ticker': record.ticker,
#             'date': record.date,
#             'open': record.open,
#             'close': record.close
#         })

#     df = pd.DataFrame(data)
#     df['change_percentage'] = ((df['close'] - df['open']) / df['open']) * 100

#     df_latest = df.groupby('ticker').apply(lambda x: x.sort_values('date').iloc[-1]).reset_index(drop=True)

#     top_gainers = df_latest.nlargest(5, 'change_percentage')
#     top_losers = df_latest.nsmallest(5, 'change_percentage')

#     return {
#         "top_gainers": top_gainers.to_dict(orient='records'),
#         "top_losers": top_losers.to_dict(orient='records')
#     }

# def generate_reports():
#     tickers = [
#         'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
#         'META', 'NVDA', 'NFLX', 'BABA', 'V',
#         'IBM', 'ORCL', 'CSCO', 'AMD', 'INTC',
#         'NVDA', 'BA', 'SNE', 'SBUX', 'WMT'
#     ]
    
#     reports = {}
#     for ticker in tickers:
#         reports[ticker] = generate_kpi_report(ticker)
    
#     # Save daily, weekly, and monthly reports
#     now = datetime.now()
#     daily_report_file = f"reports/daily_report_{now.strftime('%Y%m%d')}.csv"
#     weekly_report_file = f"reports/weekly_report_{now.strftime('%Y%W')}.csv"
#     monthly_report_file = f"reports/monthly_report_{now.strftime('%Y%m')}.csv"

#     # Generate and save reports
#     pd.DataFrame(reports.values()).to_csv(daily_report_file, index=False)
    
#     # Weekly and monthly reports
#     weekly_reports = {ticker: generate_kpi_report(ticker) for ticker in tickers}
#     pd.DataFrame(weekly_reports.values()).to_csv(weekly_report_file, index=False)
    
#     monthly_reports = {ticker: generate_kpi_report(ticker) for ticker in tickers}
#     pd.DataFrame(monthly_reports.values()).to_csv(monthly_report_file, index=False)

# def job():
#     tickers = [
#         'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
#         'META', 'NVDA', 'NFLX', 'BABA', 'V',
#         'IBM', 'ORCL', 'CSCO', 'AMD', 'INTC',
#         'NVDA', 'BA', 'SNE', 'SBUX', 'WMT'
#     ]
#     for ticker in tickers:
#         print(f"Processing {ticker}...")
#         data = fetch_stock_data(ticker, period="1d", interval="1h")
#         save_to_db(ticker, data)

# def report_job():
#     generate_reports()

# @app.route('/')
# def index():
#     tickers = [
#         'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
#         'META', 'NVDA', 'NFLX', 'BABA', 'V',
#         'IBM', 'ORCL', 'CSCO', 'AMD', 'INTC',
#         'NVDA', 'BA', 'SNE', 'SBUX', 'WMT'
#     ]
#     reports = {}
#     for ticker in tickers:
#         reports[ticker] = generate_kpi_report(ticker)
#     top_gainers_losers_24h = get_top_gainers_losers_last_24h()
    
#     # Get current date
#     now = datetime.now()

#     return render_template('index.html', reports=reports, top_gainers_losers_24h=top_gainers_losers_24h, now=now)

# @app.route('/api/kpi/<ticker>')
# def api_kpi(ticker):
#     report = generate_kpi_report(ticker)
#     return jsonify(report)

# @app.route('/api/top-gainers-losers')
# def api_top_gainers_losers():
#     top_gainers_losers_24h = get_top_gainers_losers_last_24h()
#     return jsonify(top_gainers_losers_24h)

# def run_scheduler():
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# if __name__ == "__main__":
#     # Schedule the job to run every hour
#     schedule.every().hour.do(job)

#     # Schedule the report generation job to run daily
#     schedule.every().day.at("00:00").do(report_job)

#     # Run the job once immediately for testing
#     job()

#     # Run scheduler in a separate thread
#     threading.Thread(target=run_scheduler, daemon=True).start()

#     # Run the Flask app
#     app.run(debug=True, port=5004)
