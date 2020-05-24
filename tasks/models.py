from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Tasks(models.Model):
    casecode = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    deadline_date = models.DateField(default=timezone.now)
    deadline_time = models.CharField(max_length=25)
    STATUS = (('r', 'rec'),
              ('d', 'done'))
    status = models.CharField(max_length=1, choices=STATUS, default='r')

    class Meta:
        ordering = ['deadline_date', 'deadline_time', '-author']

    def __str__(self):
        return self.casecode
