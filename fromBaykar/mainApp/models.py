from django.db import models
from django.contrib.auth.models import User

from .constants import *

class MailLogs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    mail_type = models.IntegerField(choices=MAIL_TYPE)
    created_at = models.DateTimeField(null=True, auto_now_add=True, editable=False)
