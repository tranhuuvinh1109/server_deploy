# Generated by Django 4.2.7 on 2023-11-02 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0002_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='link_drive',
            field=models.CharField(default='', max_length=255),
        ),
    ]