# Generated by Django 3.2.7 on 2021-11-27 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0014_alter_appointment_test_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='test_result',
            field=models.FileField(blank=True, null=True, upload_to='test_report'),
        ),
    ]