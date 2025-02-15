from django.db import models
from django.urls import reverse

class Item(models.Model):
    title = models.CharField(max_length=200, default='', null=False, blank=False)
    author = models.CharField(max_length=200, default='', null=False, blank=False)
    description = models.TextField(default='', null=True, blank=True)
    content = models.FileField(upload_to='literature/', blank=False)
    date_added = models.DateField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('literature:literature-detail', kwargs={'item_id': self.id})

    def __str__(self):
        return f"{self.author} - {self.title}"