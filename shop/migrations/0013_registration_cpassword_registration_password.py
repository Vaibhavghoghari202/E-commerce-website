# Generated by Django 5.0.6 on 2024-10-13 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_registration'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='cpassword',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='registration',
            name='password',
            field=models.CharField(default='', max_length=100),
        ),
    ]
