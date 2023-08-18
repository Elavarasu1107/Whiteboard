from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Board(models.Model):
    content = models.CharField(max_length=255, null=True, blank=True)
    actions = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
