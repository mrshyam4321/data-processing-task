from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    role = models.CharField(max_length=50)

