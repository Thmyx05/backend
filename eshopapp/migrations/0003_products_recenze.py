# Generated by Django 5.1.7 on 2025-03-15 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshopapp', '0002_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='recenze',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
