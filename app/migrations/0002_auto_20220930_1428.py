# Generated by Django 3.1.4 on 2022-09-30 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='box',
            name='Area',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='box',
            name='Volume',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
