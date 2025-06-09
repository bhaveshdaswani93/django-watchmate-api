from django.db import models

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
