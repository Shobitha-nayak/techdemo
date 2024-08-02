# management/commands/fetch_stock_data.py
from django.core.management.base import BaseCommand
from datetime import datetime
from yourapp.utils import fetch_stock_data, save_to_db

class Command(BaseCommand):
    help = 'Fetch stock data and save to database'

    def handle(self, *args, **kwargs):
        tickers = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
            'META', 'NVDA', 'NFLX', 'BABA', 'V',
            'IBM', 'ORCL', 'CSCO', 'AMD', 'INTC',
            'NVDA', 'BA', 'SBUX','UDMY', 'WMT'
        ]
        for ticker in tickers:
            print(f"Processing {ticker}...")
            data = fetch_stock_data(ticker, period="1d", interval="1h")
            save_to_db(ticker, data)
            self.stdout.write(self.style.SUCCESS(f'Successfully processed {ticker}'))

# Run this command using: python manage.py fetch_stock_data
