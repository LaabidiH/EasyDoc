# Generated by Django 3.2.19 on 2023-07-02 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EasyDoc_app', '0008_alter_consultation_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='date',
            field=models.CharField(max_length=20),
        ),
    ]
