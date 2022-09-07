# Generated by Django 3.2 on 2022-08-31 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0005_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='message',
            name='status',
            field=models.SmallIntegerField(blank=True, default=0, null=True),
        ),
    ]
