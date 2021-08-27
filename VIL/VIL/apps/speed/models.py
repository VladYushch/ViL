import random
import uuid
import datetime
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

class Measurement(models.Model):
    tester = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    id = models.AutoField(primary_key=True)
    dsp = models.DecimalField(max_digits=5, decimal_places= 2,null=True )
    usp = models.DecimalField(max_digits=5, decimal_places= 2,null=True )
    ping = models.DecimalField(max_digits=5, decimal_places= 2,null=True )
    bytes_sent = models.CharField(max_length=300,null=True)
    bytes_recieve = models.CharField(max_length=300,null=True)
    servid =models.SmallIntegerField(null=True)
    testdata =models.DateTimeField(default=datetime.datetime.now())
    size = models.IntegerField(null=True)
    time=models.DecimalField(max_digits=10,decimal_places=3,null=True)
    rec=models.BooleanField(default=False)
    available=models.IntegerField(default=1)
    enddata=models.DateTimeField(default=datetime.datetime.now()+datetime.timedelta(days=random.randrange(0,1),hours=random.randrange(1,23)))

    class Meta:
        ordering =["-testdata"]


    def get_absolute_url(self):
        return reverse('measurement', args=[str(self.id)])

    def testedrecently(self):
        return self.testdata >= timezone.now()-datetime.timedelta(hours=1)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    #slug=models.SlugField(verbose_name="URL address",unique=True, blank=True, null=True, default='{}')
    def get_absolute_url(self):
        return reverse('user_url', kwargs={'slug': self.slug})

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)






