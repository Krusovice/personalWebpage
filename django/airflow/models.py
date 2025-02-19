from django.db import models

class StockPrice(models.Model):
    ticker = models.CharField(max_length=10, db_column='ticker')
    date = models.DateField(db_column='date')
    closing_price = models.DecimalField(max_digits=10, decimal_places=2, db_column='close')

    class Meta:
        db_table = 'stock_prices'

    def __str__(self):
        return f'{self.ticker} - {self.date}'