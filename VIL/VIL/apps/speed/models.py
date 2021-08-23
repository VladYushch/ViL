import uuid
import datetime
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

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
    rec=models.BooleanField(default=False)

    class Meta:
        ordering =["-testdata"]


    def get_absolute_url(self):
        return reverse('measurement', args=[str(self.id)])

    def testedrecently(self):
        return self.testdata >= timezone.now()-datetime.timedelta(hours=1)


class Mstats(models.Model):
    count = models.IntegerField(null=True)





