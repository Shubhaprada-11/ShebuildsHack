from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserPeriod(models.Model):
    uid = models.ForeignKey(User,related_name='user_id',on_delete=models.CASCADE)
    lasperioddate = models.DateField('%Y-%m-%d')
    duration = models.IntegerField()