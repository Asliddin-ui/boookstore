from django.db import models

class Users(models.Model):
    name = models.CharField('Ismi', max_length=155)
    phone = models.CharField('Telefon nomer', max_length=13)
    telegram_id = models.IntegerField('Telegram id')
