# Generated by Django 3.2.7 on 2021-10-02 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_auto_20211002_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='pic',
            field=models.FileField(blank=True, null=True, upload_to='profile'),
        ),
    ]
