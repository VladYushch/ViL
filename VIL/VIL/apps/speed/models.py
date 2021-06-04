import uuid

from django.db import models


class Customers(models.Model):
    nickname = models.CharField(max_length=20)
    number_of_check = models.IntegerField()
   # def __str__(self):
    #    return self.username

class Record(models.Model):

    record_id=models.UUIDField(primary_key=True, default=uuid.uuid4())
    creator = models.ForeignKey("Customers", on_delete = models.CASCADE )
    dsp = models.DecimalField(max_digits=5, decimal_places= 2 )
    usp = models.DecimalField(max_digits=5, decimal_places= 2 )
    ping = models.TimeField(auto_now=False, auto_now_add=False)
    bytes_sent = models.CharField(max_length=300)
    bytes_recieve = models.CharField(max_length=300)
    servid =models.SmallIntegerField()
    testdata =models.DateTimeField()

    class Meta:
        ordering =["-testdata"]

   # def get_absolute_url(self):
    #    return reversed('record', args=[str(self.record_id)])
    #def __str__(self):
     #   return self.record_id

