from django.db import models
from django.conf import settings

class Link(models.Model):
    id = models.AutoField(primary_key=True)
    actual_url = models.TextField(default="")
    shorten_url = models.URLField(blank=True, default="")
    hit_count = models.BigIntegerField(default=0)


