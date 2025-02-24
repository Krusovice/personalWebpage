from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to='frontpage_pdfs/', null=True, blank=True)
    # You can add other fields like video_url, pdf_file, etc., if needed.

    def __str__(self):
        return self.title