# Generated by Django 3.2.7 on 2021-10-25 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0009_appointment_payment_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='test_name',
            new_name='test',
        ),
    ]
