from django.db import models

class User(models.Model):
    email        = models.CharField(max_length = 200, unique = True)
    password     = models.CharField(max_length = 200)
    phone_number = models.CharField(max_length = 20, null = True)
    name         = models.CharField(max_length = 45, null = True)
    address      = models.CharField(max_length = 300, null = True)
    
    class Meta:
        db_table = 'users'