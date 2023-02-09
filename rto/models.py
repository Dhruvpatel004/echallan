from django.db import models

# Create your models here.
class RTOadmin(models.Model):
    admin_id=models.AutoField(primary_key = True)
    admin_username=models.CharField(max_length=50)
    # authentication/forms.py
    admin_password = models.CharField(max_length=50)
    # desc=models.CharField(max_length=300)
    admin_created_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.admin_username