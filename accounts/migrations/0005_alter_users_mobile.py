# Generated by Django 3.2.25 on 2024-10-22 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20241022_0832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='mobile',
            field=models.BigIntegerField(),
        ),
    ]
