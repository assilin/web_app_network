# Generated by Django 4.1.7 on 2023-04-07 13:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0012_alter_post_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinformation',
            name='userinfo_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
