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
    
class Vehicle(models.Model): 
    vehicle_id=models.AutoField(primary_key = True)
    vehicle_no=models.CharField(max_length=50,default=None)
    vehicle_own_name = models.CharField(max_length=50,default=None)
    vehicle_own_contact=models.IntegerField(default=None)
    vehicle_own_add=models.CharField(max_length=100,default=None)
    vehicle_own_email=models.CharField(max_length=50, default=None)
    vehicle_company_name=models.CharField(max_length=50,default=None)
    # vehicle_class=models.CharField(max_length=50,default=None)
    vehicle_date_reg=models.DateField(default=None)
    vehicle_chassics_no=models.CharField(max_length=30,default=None)
    vehicle_eng_no=models.CharField(max_length=30,default=None)
    vehicle_own_srno=models.IntegerField(default=None)
    vehicle_fuel_use=models.CharField(max_length=30,default=None)
    vehicle_Seat_cap=models.IntegerField(default=None)
    vehicle_model_name=models.CharField(max_length=50,default=None)
    vehicle_created_date=models.DateField(auto_now_add=True)  
    vehicle_last_login=models.CharField(max_length=30,default=None)

    def __str__(self):  
        return self.vehicle_no

class Rules(models.Model):
    rule_id=models.AutoField(primary_key= True)
    rule_code=models.CharField(max_length=50)
    rule_desc=models.CharField(max_length=100,blank=True)
    rule_sect = models.CharField(max_length=50,null=True)
    rule_pen=models.CharField(max_length=100,null=True)
    # rule_date=models.DateField(default=None)
    def __str__(self):  
        return self.rule_code