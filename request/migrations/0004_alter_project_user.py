# Generated by Django 4.2.7 on 2023-11-02 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0003_alter_project_link_drive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='user',
            field=models.IntegerField(),
        ),
    ]