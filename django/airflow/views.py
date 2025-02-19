from rest_framework import viewsets
from .models import StockPrice
from .serializers import StockPriceSerializer

class StockPriceViewSet(viewsets.ModelViewSet):
    queryset = StockPrice.objects.all()
    serializer_class = StockPriceSerializer