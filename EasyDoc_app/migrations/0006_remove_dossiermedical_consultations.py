# Generated by Django 3.2.19 on 2023-07-01 21:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EasyDoc_app', '0005_authentification_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dossiermedical',
            name='consultations',
        ),
    ]