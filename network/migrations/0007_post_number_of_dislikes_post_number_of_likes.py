# Generated by Django 4.1.7 on 2023-04-04 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_alter_like_like_dislike'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='number_of_dislikes',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='number_of_likes',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
