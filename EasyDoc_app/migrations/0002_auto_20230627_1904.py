# Generated by Django 3.2.19 on 2023-06-27 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EasyDoc_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medecin',
            name='poste_role',
            field=models.CharField(choices=[('medecine', 'Medecine'), ('chirurgie', 'Chirurgie'), ('pediaterie', 'Pediaterie'), ('maternite', 'Maternite'), ('SAA', 'SAA')], max_length=20),
        ),
        migrations.AlterField(
            model_name='technicien',
            name='poste_role',
            field=models.CharField(choices=[('medecine', 'Medecine'), ('chirurgie', 'Chirurgie'), ('pediaterie', 'Pediaterie'), ('maternite', 'Maternite'), ('SAA', 'SAA')], max_length=20),
        ),
    ]
