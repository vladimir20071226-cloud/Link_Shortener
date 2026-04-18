from django.db import models
import uuid


class Link(models.Model):
    original_url=models.URLField(max_length=2000)
    created_at=models.DateTimeField(auto_now_add=True)
    click_count = models.IntegerField(default=0)
    code=models.CharField(max_length=10, blank=True)
    def save(self, *args, **kwargs):
        if not self.code:
            new_code = str(uuid.uuid4())[:8]
            while Link.objects.filter(code=new_code).exists():
                new_code = str(uuid.uuid4())[:8]
            self.code=new_code
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.code} -> {self.original_url}"
class ShortUrl(models.Model):
    link=models.ForeignKey(Link, on_delete=models.CASCADE)
    update_at=models.DateTimeField(auto_now_add=True)