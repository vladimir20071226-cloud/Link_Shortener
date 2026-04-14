from django.db import models


class Link(models.Model):
    original_url=models.URLField(max_length=2000)
    created_at=models.DateTimeField(auto_now_add=True)
    click_count = models.IntegerField(default=0)
class ShortUrl(models.Model):
    link=models.ForeignKey(Link, on_delete=models.CASCADE)
    update_at=models.DateTimeField(auto_now_add=True)