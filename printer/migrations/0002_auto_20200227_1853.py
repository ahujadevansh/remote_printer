# Generated by Django 2.2.9 on 2020-02-27 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('printer', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='printrequestfile',
            old_name='print_request_id',
            new_name='print_request',
        ),
    ]
