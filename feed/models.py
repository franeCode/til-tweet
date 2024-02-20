from django.db import models
from django.contrib.auth.models import User
from .templatetags.custom_filters import custom_timesince


class Post(models.Model):
    text = models.CharField(max_length=240)
    date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    def get_comment_count(self):
        return Comment.objects.filter(post=self).count()
    
    def formatted_date(self):
        return custom_timesince(self.date)
    
    def __str__(self):
        return self.text[0:100]
    
class Comment(models.Model):
    text = models.CharField(max_length=240)
    date = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def formatted_date(self):
        return custom_timesince(self.date)
    
    def __str__(self):
        return f"{self.author.username} - {self.text[:50]}"
