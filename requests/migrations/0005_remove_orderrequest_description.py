# Generated by Django 3.0.6 on 2020-05-16 18:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0004_auto_20200516_1758'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderrequest',
            name='description',
        ),
    ]
