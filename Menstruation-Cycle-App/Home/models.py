from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class UserPeriod(models.Model):
    uid = models.ForeignKey(User,related_name='user_id',on_delete=models.CASCADE)
    lasperioddate = models.DateField('%Y-%m-%d')
    duration = models.IntegerField()

class Event(models.Model):
    description = models.CharField(max_length=500)
    start_time = models.DateTimeField()
    userid = models.ForeignKey(User,related_name="user_identity",on_delete=models.CASCADE)
    mood = models.CharField(max_length=100)
    moodscore = models.IntegerField()

    @property
    def get_html_url(self):
        url = reverse('Home:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'