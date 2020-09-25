from django.db import models

# Create your models here.
class Test(models.Model):
    state = models.IntegerField(default=0)

class Cook(models.Model):
    link = models.TextField()
    food = models.TextField()
    img = models.TextField()
    tag = models.TextField()
    material = models.TextField()
    cooking_time = models.TextField()
    scrap = models.TextField()

class Alcohol(models.Model) :
    nation = models.TextField()
    name = models.TextField()
    alcohol_type = models.TextField()
    tag = models.TextField()
    alcohol = models.TextField()
    