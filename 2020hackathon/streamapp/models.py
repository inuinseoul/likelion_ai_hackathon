from django.db import models

# Create your models here.
class Test(models.Model):
    state = models.IntegerField(default=0)

class Alcohol(models.Model) :
    nation = models.TextField()
    name = models.TextField()
    alcohol_type = models.TextField()
    tag = models.TextField()
    alcohol = models.TextField()
