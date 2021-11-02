from django.db import models
from django.db import models

# Create your models here.
class Comment(models.Model):
    name = models.CharField(max_length=127)
    comment_text = models.TextField()
