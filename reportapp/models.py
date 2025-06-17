from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Report(models.Model):
    data = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.TextField(blank=False)
    comment = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_reports', blank=True)

    def __str__(self):
            return f"{self.data} - {self.author.username}"

class Comment(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)