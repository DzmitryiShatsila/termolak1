from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid
from django.core.exceptions import ValidationError

# Create your models here.


def validate_time(value):
    if value <= 0:
        raise ValidationError('Time cannot be less then 0!')


class Cases(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE, default=User)
    date = models.DateField(default=timezone.now)
    case_code = models.CharField(max_length=200)
    images_types = (('ct', 'CT'),
                    ('mri', 'MRI'))
    images = models.CharField(max_length=3, choices=images_types, default='ct')
    case_types = (('s', 'Standard'),
                  ('o', "MyOsteotomy"))
    case = models.CharField(max_length=1, choices=case_types, default='s')
    product_types = (('spine', 'Spine'),
                     ('knee', 'Knee'),
                     ('hip', 'Hip'),
                     ('shoulder', 'Shoulder'),
                     ('forearm', 'Forearm'),
                     ('wrist', 'Wrist'),
                     ('ankle', 'Ankle'),)
    product = models.CharField(max_length=30, choices=product_types)
    software_types = (('mimics', 'Mimics'),
                      ('avizo', 'Avizo'))
    software = models.CharField(max_length=10, choices=software_types)
    procedure_type = (('rec', 'Reconstruction'),
                      ('check', 'Control'))
    procedure = models.CharField(max_length=10, choices=procedure_type)
    time = models.IntegerField(validators=[validate_time])
    notes = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-date']

    @staticmethod
    def get_detail(images, case, product, software, procedure):
        return Cases.objects.filter(images=images).filter(case=case).filter(
            product=product).filter(software=software).filter(
            procedure=procedure)
