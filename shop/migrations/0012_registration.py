# Generated by Django 5.0.6 on 2024-10-13 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_alter_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(default='', max_length=100)),
                ('Phone', models.CharField(default='', max_length=100)),
                ('address', models.CharField(default='', max_length=500)),
                ('gender', models.CharField(default='', max_length=500)),
            ],
        ),
    ]
