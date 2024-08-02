from django.db import models

class StockData(models.Model):
    ticker = models.CharField(max_length=10)
    date = models.DateTimeField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.BigIntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['ticker', 'date']),
        ]
        ordering = ['-date']
