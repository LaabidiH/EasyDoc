from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Authentification(models.Model):
    nom_complet = models.CharField(max_length=100, null= True)
    email = models.EmailField(null= True)
    password = models.CharField(max_length=100 , null= True)
    active = models.BooleanField(default=False)
    service = models.CharField(
        max_length=20,
        choices=[
            ("medecine", "Medecine"),
            ("chirurgie", "Chirurgie"),
            ("pediaterie", "Pediaterie"),
            ("maternite", "Maternite"),
            ("SAA","SAA"),
            ("admin", "admin")
        ], 
        null= True
    )
    def delete(self, *args, **kwargs):
        super(Authentification, self).delete(*args, **kwargs)

class Personne(models.Model):
    nom_complet = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    tele = models.CharField(max_length=15)
    adresse = models.CharField(max_length=100)
    active = models.BooleanField(default=False)

    poste_role = models.CharField(
        max_length=20,
        choices=[
            ("medecin", "medecin"),
            ("technicien", "technicien")
        ]
    )


    class Meta:
        abstract = True


class Medecin(Personne):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    service_medecin = models.CharField(
        max_length=20,
        choices=[
            ("medecine", "medecine"),
            ("chirurgie", "chirurgie"),
            ("pediaterie", "pediaterie"),
            ("maternite", "maternite")
        ]
    )
    inpe = models.CharField(max_length=10)
    responsable = models.BooleanField(default=False)
    def delete(self, *args, **kwargs):
        super(Medecin, self).delete(*args, **kwargs)
        
class Technicien(Personne):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    service_role = models.CharField(
        max_length=20,
        choices=[
                ("SAA", "SAA")
            ]
    )
    def delete(self, *args, **kwargs):
        super(Technicien, self).delete(*args, **kwargs)
   
def validate_file_extension(value):
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
    extension = str(value.name).lower().split('.')[-1]
    if extension not in allowed_extensions:
        raise ValidationError("Seules les extensions .jpg, .jpeg, .png et .pdf sont autorisées.")

class Consultation(models.Model):
    ipp = models.CharField(max_length=12)
    cin_assurant = models.CharField(max_length=12)
    ordonnance = models.FileField(upload_to='ordonnance/')
    date = models.CharField(max_length=20)
    imprime = models.BooleanField(default=False)
    SERVICE_CHOICES = [
        ('Medecine', 'Medecine'),
        ('chirurgie', 'Chirurgie'),
        ('pediaterie', 'Pediaterie'),
        ('maternite', 'Maternite'),
        ('centreDC', 'CentreDC'),
        ('Radiologie', 'Radiologie'),
        ('Biologie', 'Biologie')
    ]
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES, default=('Medecine', 'Medecine'))
    action_choices = [
        ('Consultation', 'Consultation'),
        ('Radiologie', 'Radiologie'),
        ('Biologie', 'Biologie'),
        ('Hospitalisation', 'Hospitalisation'),
    ]
    action = models.CharField(max_length=50, choices=action_choices,default=("Consultation", "Consultation"))


class Hospitalisation(Consultation):
    dateSortie = models.CharField(max_length=100)
    billetHospitalisation = models.FileField(upload_to='billet_hosp/')
    facture = models.FileField(upload_to='facture/')
    dpc = models.FileField(upload_to='facture/', null=True)
    pli_confidentiel = models.FileField(upload_to='facture/', null =True)
    medecin = models.CharField(max_length=100, default="0000000")

class Radiologie(Consultation):
    bonRadio = models.FileField(upload_to='bonRadio/')
    facture = models.FileField(upload_to='facture/')


class Biologie(Consultation):
    bonBio = models.FileField(upload_to='bonBio/', validators=[validate_file_extension])
    facture = models.FileField(upload_to='facture/', validators=[validate_file_extension])


class DossierMedical(models.Model):
    # consultations = models.ManyToManyField(Consultation)
    cinAssure = models.CharField(max_length=12)
    ipp = models.CharField(max_length=12, unique=True)
    cnss = models.CharField(max_length=12)
    phCIN = models.FileField(upload_to='phCIN/')
    phCNSS = models.FileField(upload_to='phCNSS/')

    class Meta:
        unique_together = (("cinAssure", "ipp", "cnss"),)
    
    def delete(self, *args, **kwargs):
        self.phCIN.delete()
        self.phCNSS.delete()
        super().delete(*args, **kwargs)

"""
class DossierPatient(models.Model):
    nom = models.CharField(max_length=100)
    ipp = models.IntegerField()
    cin = models.CharField(max_length=20)

    def __str__(self):
     return f"{self.ipp} - {self.nom} - {self.cin}"
"""