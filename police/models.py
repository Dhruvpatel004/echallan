from django.db import models

# Create your models here.
class Police(models.Model):
    police_id=models.AutoField(primary_key = True)
    police_username=models.CharField(max_length=50,default=None)
    police_password = models.CharField(max_length=50)
    police_firstname=models.CharField(max_length=50,default=None)
    police_lastname=models.CharField(max_length=50,default=None)
    # desc=models.CharField(max_length=300)
    police_age=models.IntegerField(default=None)
    police_birth_date=models.DateField(default=None)
    police_joing_date=models.DateField(default=None)
    police_address=models.CharField(max_length=100,default=None)
    police_gender=models.CharField(max_length=20,default=None)
    police_last_login=models.CharField(max_length=30,default=None)
    police_created_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.police_username
    
