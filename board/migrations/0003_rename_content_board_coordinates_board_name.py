# Generated by Django 4.2.4 on 2023-08-19 09:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_alter_board_actions_alter_board_content'),
    ]

    operations = [
        migrations.RenameField(
            model_name='board',
            old_name='content',
            new_name='coordinates',
        ),
        migrations.AddField(
            model_name='board',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]
