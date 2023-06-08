from django.db import models

class Users(models.Model):
    full_name = models.CharField(max_length=155)
    telegram_id = models.IntegerField()
    language = models.CharField(max_length=10)
    username = models.CharField(max_length=120,unique=True)