from django.db import models

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class Anime(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='anime_images/')
    year = models.IntegerField(null=True, blank=True)
    genres = models.ManyToManyField('Genre', related_name='animes')
    slug = models.SlugField(unique=True)

    episodes_count = models.PositiveIntegerField(default=12)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('anime_detail', kwargs={'slug': self.slug})


class UserAnimeProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    watched_episodes = models.PositiveIntegerField(default=0)
    current_episode = models.PositiveIntegerField(default=0)
    
    STATUS_CHOICES = [
        ('watching', 'Смотрю'),
        ('completed', 'Просмотрено'),
        ('planned', 'В планах'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='watching')

    class Meta:
        unique_together = ('user', 'anime')

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Comment(models.Model):
    anime = models.ForeignKey('Anime', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:30]}"


# Create your models here.
