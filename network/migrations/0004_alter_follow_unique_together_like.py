# Generated by Django 4.1.7 on 2023-04-04 13:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_follow'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together={('user_f_ing', 'user_f_ed')},
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_post', to='network.post')),
                ('like_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='like_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('like_user', 'like_post')},
            },
        ),
    ]