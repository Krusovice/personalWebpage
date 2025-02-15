from django import forms
from .models import Item

class ItemUploadForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'title',
            'author',
            'description',
            'content'
        ]