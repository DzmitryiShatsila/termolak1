from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


# class DoneTasksManager(models.Manager):
#     def get_queryset(self):
#         queryset = super.get_queryset().filter(status='d')
#         if len(queryset) == 4:
#             queryset[-1].delete()
#         return queryset


class Tasks(models.Model):
    casecode = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    deadline = models.DateTimeField(default=timezone.now)
    STATUS = (('r', 'rec'),
              ('d', 'done'))
    status = models.CharField(max_length=1, choices=STATUS, default='r')

    def get_queryset(self):
        queryset = super.get_queryset().filter(status='d')
        if len(queryset) == 4:
            queryset[-1].delete()
        return queryset

    class Meta:
        ordering = ['deadline', '-author']

    def __str__(self):
        return self.casecode
