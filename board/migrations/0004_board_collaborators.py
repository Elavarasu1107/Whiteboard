# Generated by Django 4.2.4 on 2023-08-19 13:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0003_rename_content_board_coordinates_board_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='collaborators',
            field=models.ManyToManyField(related_name='collaborators', to=settings.AUTH_USER_MODEL),
        ),
    ]
