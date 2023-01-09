from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=200)
    pubdate = models.DateTimeField()
    image = models.URLField(blank=True, null=True)
    link = models.URLField()
    source = models.CharField(max_length=100)
    guid = models.URLField(unique=True)

    def __str__(self) -> str:
        return f"{self.source}: {self.title}"