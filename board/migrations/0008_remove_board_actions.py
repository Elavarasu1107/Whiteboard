# Generated by Django 4.2.4 on 2023-08-21 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0007_alter_boarddetails_current_pointer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='board',
            name='actions',
        ),
    ]