# Generated by Django 4.2.14 on 2024-09-30 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_order_delivery_order_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='adress',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
