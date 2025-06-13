from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class StreamPlatform(models.Model):
    name = models.CharField(max_length=100)
    about = models.CharField(max_length=255)
    website = models.URLField()

    def __str__(self):
        return f"{self.name} ({self.website})"

class WatchList(models.Model):
    title = models.CharField(max_length=100)
    storyline = models.TextField()
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    platform = models.ForeignKey(StreamPlatform, related_name='watchlist', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.title}"

class Review(models.Model):
    # review_user = models.CharField(max_length=50)
    rating = models.FloatField()
    description = models.TextField()
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    watchlist = models.ForeignKey(WatchList, related_name='reviews', on_delete=models.CASCADE, null=True)
    review_user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE, null=True)
    class Meta:
        unique_together = ('watchlist', 'review_user')

    def __str__(self):
        return f"{self.rating} - {self.watchlist.title} ({self.created})"
