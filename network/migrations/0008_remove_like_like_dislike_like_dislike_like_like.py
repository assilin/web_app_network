# Generated by Django 4.1.7 on 2023-04-04 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_post_number_of_dislikes_post_number_of_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='like_dislike',
        ),
        migrations.AddField(
            model_name='like',
            name='dislike',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='like',
            name='like',
            field=models.BooleanField(default=False),
        ),
    ]
