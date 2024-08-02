# Stock Market Data Ingestion and Monitoring System

## Overview

This project ingests stock data from Yahoo Finance daily, generates reports on key performance indicators (KPIs), and creates alerts based on significant stock value changes. The system is divided into a backend (Python) and a frontend (Next.js) and is containerized using Docker and deployed with Kubernetes.

## Directory Structure

- `/backend`: Contains backend code, models, and scripts.
- `/frontend`: Contains frontend code, components, and pages.
- `/k8s`: Kubernetes configuration files.
- `/docs`: Documentation for the project.
- `/scripts`: Utility scripts.
- `.gitignore`: Git ignore file.

## Setup

1. **Backend Setup**
   - Navigate to the `/backend` directory.
   - Install dependencies: `pip install -r requirements.txt`.
   - Build and run the Docker image: `docker build -t stock-backend .` and `docker run -p 5000:5000 stock-backend`.

2. **Frontend Setup**
   - Navigate to the `/frontend` directory.
   - Install dependencies: `npm install`.
   - Build and run the Docker image: `docker build -t stock-frontend .` and `docker run -p 3000:3000 stock-frontend`.

3. **Kubernetes Deployment**
   - Apply Kubernetes configurations: `kubectl apply -f k8s/`.

## Documentation

- [Architecture](docs/architecture.md)
- [Setup Instructions](docs/setup.md)


# 1. Data Ingestion

Task: Implement a module to fetch data from the Yahoo Finance API daily.

Description:

    Fetching Data: The fetch_stock_data function uses the yfinance library to pull historical stock data. It fetches data for specified tickers, with options for period and interval (e.g., daily data with hourly intervals).

    python

def fetch_stock_data(ticker, period="1d", interval="2h"):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period, interval=interval)
        return hist
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()

Scheduling Data Fetching: The job function, which is scheduled to run every hour, fetches data for a list of tickers and saves it to the database.

python

    def job():
        tickers = [ ... ]  # List of tickers
        for ticker in tickers:
            print(f"Processing {ticker}...")
            data = fetch_stock_data(ticker, period="1d", interval="1h")
            save_to_db(ticker, data)

2. Data Storage

Task: Store the ingested data in a structured format.

Description:

    Database Schema: The StockData class defines the schema for storing stock data in a SQLite database using SQLAlchemy. This includes columns for ticker, date, and various price metrics.
    The SQLite database (stocks.db) is automatically created by SQLAlchemy when you run your Flask application, provided that the Base.metadata.create_all(engine) line is executed.

    python

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

Saving Data: The save_to_db function processes the fetched data and stores it in the database. It avoids duplicating existing records.

python

    def save_to_db(ticker, data):
        if data.empty:
            print(f"No data to save for {ticker}")
            return
        ...
        session.commit()

3. Report Generation

Task: Generate daily, weekly, and monthly reports based on KPIs.

Description:

    Generating KPIs: The generate_kpi_report function calculates various KPIs for a given ticker, such as daily closing price and percentage changes over different periods.

    python

def generate_kpi_report(ticker):
    daily_report = generate_daily_opening_closing_price_report(ticker)
    return {
        "ticker": ticker,
        "daily_closing_price": daily_report[-1]['close'] if daily_report else "No data",
        "24h_change": calculate_percentage_change(ticker, datetime.now() - timedelta(days=1), datetime.now()) or "Not enough data",
        "30d_change": calculate_percentage_change(ticker, datetime.now() - timedelta(days=30), datetime.now()) or "Not enough data",
        "1y_change": calculate_percentage_change(ticker, datetime.now() - timedelta(days=365), datetime.now()) or "Not enough data"
    }

Top Gainers/Losers: The get_top_gainers_losers_last_24h function identifies the top gainers and losers based on percentage change over the last 24 hours.

python

    def get_top_gainers_losers_last_24h():
        end_date = datetime.now()
        start_date = end_date - timedelta(hours=24)
        ...
        return {
            "top_gainers": top_gainers.to_dict(orient='records'),
            "top_losers": top_losers.to_dict(orient='records')
        }

Automation

    Scheduler: The schedule library is used to run the data fetching job every hour, and the scheduler runs in a separate thread.

    python

    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)

    if __name__ == "__main__":
        schedule.every().hour.do(job)
        threading.Thread(target=run_scheduler, daemon=True).start()
        app.run(debug=True, port=5001)

This setup ensures that stock data is ingested, stored, and processed regularly, and reports are generated based on the latest available data.