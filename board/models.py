from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Board(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, default='Board')
    actions = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    collaborators = models.ManyToManyField(User, related_name='collaborators')

    class Meta:
        db_table = 'board'


class BoardDetails(models.Model):
    coordinates = models.TextField(null=True, blank=True)
    line_width = models.IntegerField(null=False, blank=False)
    color = models.CharField(max_length=100, null=False, blank=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
