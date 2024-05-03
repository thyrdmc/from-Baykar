from django.db import models
from django.contrib.auth.models import User

from .constants import *

class MailLogs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    mail_type = models.IntegerField(choices=MAIL_TYPE)
    created_at = models.DateTimeField(null=True, auto_now_add=True, editable=False)

class Vehicle(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    weight = models.FloatField()
    category = models.IntegerField(choices=CATEGORY, default=0)
    price = models.FloatField(default=100)
    currency =  models.IntegerField(choices=CURRENCY, default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False)

    def __str__(self):
        return f"{self.name}"
    