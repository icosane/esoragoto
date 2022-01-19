from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class textfield(models.Model):
    N = models.CharField(max_length=3,validators=[RegexValidator(r'^\d{1,10}$')],primary_key=True)
    #K = models.CharField(max_length=3)
