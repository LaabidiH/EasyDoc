from django.contrib import admin
from .models import *

admin.site.register(Technicien)
admin.site.register(Medecin)
admin.site.register(DossierMedical)
admin.site.register(Authentification)
admin.site.register(Consultation)
admin.site.register(Hospitalisation)
admin.site.register(Biologie)
admin.site.register(Radiologie)