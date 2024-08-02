# backend/backend/admin.py

from django.contrib import admin
from .models import StockData

class StockDataAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'date', 'open', 'close', 'high', 'low')
    # Ensure 'volume' is not included if it doesn't exist on StockData

admin.site.register(StockData, StockDataAdmin)
