# Generated by Django 4.1.7 on 2023-04-07 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_userinformation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinformation',
            old_name='name',
            new_name='userinfo_id',
        ),
    ]
