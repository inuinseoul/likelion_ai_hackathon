from django.db import models

# Create your models here.
class Test(models.Model):
    state = models.IntegerField(default=0)
