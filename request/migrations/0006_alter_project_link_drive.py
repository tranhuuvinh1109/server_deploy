# Generated by Django 4.2.7 on 2023-11-02 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0005_alter_project_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='link_drive',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]