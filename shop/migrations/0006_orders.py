# Generated by Django 5.0.6 on 2024-09-24 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_delete_orders'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('items_json', models.CharField(max_length=5000)),
                ('fname', models.CharField(max_length=111)),
                ('lname', models.CharField(max_length=111)),
                ('phone_Number', models.CharField(max_length=99)),
                ('gender', models.CharField(max_length=111)),
                ('address', models.CharField(max_length=111)),
                ('city', models.CharField(max_length=111)),
                ('county', models.CharField(max_length=111)),
                ('zip_code', models.CharField(max_length=111)),
            ],
        ),
    ]
