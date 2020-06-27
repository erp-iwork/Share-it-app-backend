# Generated by Django 2.2.13 on 2020-06-27 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20200627_0754'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemmodel',
            name='sub_category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='item_sub_category', to='main.SubCategory'),
            preserve_default=False,
        ),
    ]