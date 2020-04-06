from django.db import models
from django.urls import reverse

from users.models import Profile


class PostCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    category = models.ForeignKey(PostCategory, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='post_pics')
    source_link = models.URLField(max_length=200)
    date_posted = models.DateTimeField(auto_now_add=True, auto_now=False)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    liked = models.ManyToManyField(Profile, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'pk': self.author.pk})
