# Generated by Django 4.1.5 on 2023-03-15 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rto', '0002_rules_vehicle'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challan',
            fields=[
                ('challan_no', models.AutoField(primary_key=True, serialize=False)),
                ('cpolice', models.CharField(default=None, max_length=50)),
                ('name', models.CharField(default=None, max_length=50)),
                ('offence_date', models.DateField(default=None)),
                ('offence_time', models.TimeField(default=None)),
                ('license_no', models.CharField(blank=True, default=None, max_length=50)),
                ('vehicle_no', models.CharField(default=None, max_length=50)),
                ('offender_mobile_no', models.IntegerField(default=None)),
                ('fine', models.IntegerField(default=None)),
                ('sections', models.CharField(default=None, max_length=50)),
                ('offense', models.CharField(default=None, max_length=50)),
                ('evidence', models.ImageField(blank=True, upload_to='')),
                ('status', models.CharField(default='Pending', max_length=15)),
            ],
        ),
    ]
