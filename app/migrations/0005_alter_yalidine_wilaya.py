# Generated by Django 4.2.14 on 2024-09-30 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_wilaya'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yalidine',
            name='wilaya',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.wilaya'),
        ),
    ]
