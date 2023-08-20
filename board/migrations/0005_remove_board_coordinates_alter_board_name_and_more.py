# Generated by Django 4.2.4 on 2023-08-20 10:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0004_board_collaborators'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='board',
            name='coordinates',
        ),
        migrations.AlterField(
            model_name='board',
            name='name',
            field=models.CharField(default='Board', max_length=255),
        ),
        migrations.AlterModelTable(
            name='board',
            table='board',
        ),
        migrations.CreateModel(
            name='BoardDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coordinates', models.TextField(blank=True, null=True)),
                ('line_width', models.IntegerField()),
                ('color', models.CharField(max_length=100)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.board')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
