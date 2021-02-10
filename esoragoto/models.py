from django.db import models

# Create your models here.

class textfield(models.Model):
    N = models.IntegerField(max_length=3)
    #K = models.CharField(max_length=3)
