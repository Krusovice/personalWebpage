from django.shortcuts import render
from .models import News  # Import the News model

# View for the front page
def home(request):
    # Fetch the latest 5 news items (or adjust as needed)
    news_items = News.objects.all().order_by('-id')[:5]  # This will give you the latest news
    return render(request, 'frontpage/home.html', {'news_items': news_items})
