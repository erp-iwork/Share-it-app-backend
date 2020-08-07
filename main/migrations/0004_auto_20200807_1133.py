# Generated by Django 2.2.13 on 2020-08-07 11:33

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200807_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategory',
            name='icon',
            field=models.ImageField(upload_to=main.models.upload_path),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='no-img.png', upload_to=main.models.upload_path),
        ),
        migrations.AlterField(
            model_name='user',
            name='cover_img',
            field=models.ImageField(default='no-img.png', upload_to=main.models.upload_path),
        ),
    ]