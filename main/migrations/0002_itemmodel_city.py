# Generated by Django 2.2.13 on 2020-08-08 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemmodel',
            name='city',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]