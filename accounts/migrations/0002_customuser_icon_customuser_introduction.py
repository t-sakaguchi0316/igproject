# Generated by Django 4.2 on 2024-12-25 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='icons/'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='introduction',
            field=models.TextField(blank=True, null=True),
        ),
    ]
