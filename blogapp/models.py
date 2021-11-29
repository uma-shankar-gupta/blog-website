from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})


class Comment(models.Model):
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE)
    for_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    date_cmt = models.DateTimeField(default=timezone.now)
    msg = models.CharField(max_length=160, null=True)
    def __str__(self):
        return f'Comment By {self.comment_by.username} on {self.for_post.title}' 


class Like(models.Model):
    like_by = models.ForeignKey(User, on_delete=models.CASCADE)
    for_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    date_cmt = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Like By {self.like_by.username} on {self.for_post.title}'