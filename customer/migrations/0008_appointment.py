# Generated by Django 3.2.7 on 2021-10-19 05:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0005_alter_test_test_name'),
        ('customer', '0007_auto_20211005_2331'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('amount', models.IntegerField()),
                ('status', models.CharField(default='live', max_length=20)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('test_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.test')),
            ],
        ),
    ]
