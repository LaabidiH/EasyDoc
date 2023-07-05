# Generated by Django 3.2.19 on 2023-07-04 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EasyDoc_app', '0017_delete_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medecin',
            name='service_medecin',
            field=models.CharField(choices=[('medecine', 'medecine'), ('chirurgie', 'chirurgie'), ('pediaterie', 'pediaterie'), ('maternite', 'maternite')], max_length=20),
        ),
    ]