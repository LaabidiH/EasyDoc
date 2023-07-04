# Generated by Django 3.2.19 on 2023-07-03 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EasyDoc_app', '0010_alter_dossiermedical_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dossiermedical',
            name='ipp',
            field=models.CharField(max_length=12, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='dossiermedical',
            unique_together={('cinAssure', 'ipp', 'cnss')},
        ),
    ]