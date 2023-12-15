from django.db import models

class UrlModel(models.Model):
    original_url = models.CharField(max_length=400)
    url_id = models.CharField(max_length=5, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.original_url[:20]} - {self.url_id}"