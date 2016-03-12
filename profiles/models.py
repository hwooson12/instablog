from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    _genders = (
        ('M', 'Male',),
        ('F', 'Female',),
    )
    gender = models.CharField(max_length=1, choices=_genders)