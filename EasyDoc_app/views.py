from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth, messages
from .models import *
import re, os, io
import zipfile
from io import BytesIO
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Value, CharField
from django.views.decorators.http import require_POST
import random
import string
from django.core.mail import send_mail
from django.db.models import Q


"""
from reportlab.pdfgen import canvas
from django.urls import reverse
from django.template.loader import get_template
from django.template import Context
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.templatetags.static import static
from django.http import FileResponse
import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter
from .models import DossierPatient
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
"""


from EasyDoc_app.models import *
from django.views.decorators.csrf import csrf_exempt

############# vues du admin

@csrf_exempt
def send_email(request):
    if request.method == 'POST':
        to = request.POST.get('to')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if send_mail(subject, message, 'hopital.provincial.berrechd@gmail.com', [to]):
            print('envoyé')

        return JsonResponse({'message': 'Email sent successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def imprimer_dossier_hospitalisation(request, ipp, cin, date):
    # Filtrer les objets Hospitalisation en fonction de l'IPP et du CIN du patient
    hospitalisations = Hospitalisation.objects.filter(ipp=ipp, cin_assurant=cin)
    dossierMedicals = DossierMedical.objects.filter(ipp=ipp, cinAssure=cin)

    zip_file = zipfile.ZipFile('{}.zip'.format(ipp), 'w')

    for hospitalisation in hospitalisations:
        hospitalisation.imprime = True
        hospitalisation.save()

    for hospitalisation in hospitalisations:
        zip_file.write(hospitalisation.facture.path, 'facture.pdf')
        zip_file.write(hospitalisation.billetHospitalisation.path, 'billet_hospitalisation.pdf')
        zip_file.write(hospitalisation.ordonnance.path, 'ordonnance.pdf')
        zip_file.write(hospitalisation.dpc.path, 'demande_pris_en_charge.pdf')
        zip_file.write(hospitalisation.pli_confidentiel.path, 'pli_confidentiel.pdf')

    for dossierMedical in dossierMedicals:
        zip_file.write(dossierMedical.phCIN.path, 'phCIN.pdf')
        zip_file.write(dossierMedical.phCNSS.path, 'phCNSS.pdf')

    zip_file.close()

    with open('{}.zip'.format(ipp), 'rb') as file:
        response = HttpResponse(file, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="{}.zip"'.format(ipp)
        return response


def imprimer_dossier_radiologie(request, ipp, cin, date):
    radiologies = Radiologie.objects.filter(ipp=ipp, cin_assurant=cin)
    dossierMedicals = DossierMedical.objects.filter(ipp=ipp, cinAssure=cin)

    zip_file = zipfile.ZipFile('{}.zip'.format(ipp), 'w')

    for radiologie in radiologies:
        radiologie.imprime = True
        radiologie.save()

    for radiologie in radiologies:
        zip_file.write(radiologie.facture.path, 'facture.pdf')
        zip_file.write(radiologie.bonRadio.path, 'bonRadio.pdf')
        zip_file.write(radiologie.ordonnance.path, 'ordonnance.pdf')

    for dossierMedical in dossierMedicals:
        zip_file.write(dossierMedical.phCIN.path, 'phCIN.pdf')
        zip_file.write(dossierMedical.phCNSS.path, 'phCNSS.pdf')

    zip_file.close()

    with open('{}.zip'.format(ipp), 'rb') as file:
        response = HttpResponse(file, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="{}.zip"'.format(ipp)
        return response


def imprimer_dossier_biologie(request, ipp, cin, date):
    biologies = Biologie.objects.filter(ipp=ipp, cin_assurant=cin)
    dossierMedicals = DossierMedical.objects.filter(ipp=ipp, cinAssure=cin)

    zip_file = zipfile.ZipFile('{}.zip'.format(ipp), 'w')

    for biologie in biologies:
        biologie.imprime = True
        biologie.save()

    for biologie in biologies:
        zip_file.write(biologie.facture.path, 'facture.pdf')
        zip_file.write(biologie.bonBio.path, 'bonBio.pdf')
        zip_file.write(biologie.ordonnance.path, 'ordonnance.pdf')

    for dossierMedical in dossierMedicals:
        zip_file.write(dossierMedical.phCIN.path, 'phCIN.pdf')
        zip_file.write(dossierMedical.phCNSS.path, 'phCNSS.pdf')

    zip_file.close()

    with open('{}.zip'.format(ipp), 'rb') as file:
        response = HttpResponse(file, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="{}.zip"'.format(ipp)
        return response
    

def imprimer_dossier_consultation(request, ipp, cin, date):
    consultations = Consultation.objects.filter(ipp=ipp, cin_assurant=cin, date=date)
    dossierMedicals = DossierMedical.objects.filter(ipp=ipp, cinAssure=cin)

    zip_file = zipfile.ZipFile('{}.zip'.format(ipp), 'w')

    for consultation in consultations:
        consultation.imprime = True
        consultation.save()

    for consultation in consultations:
        # zip_file.write(consultation.facture.path, 'facture.pdf')
        zip_file.write(consultation.ordonnance.path, 'ordonnance.pdf')

    for dossierMedical in dossierMedicals:
        zip_file.write(dossierMedical.phCIN.path, 'phCIN.pdf')
        zip_file.write(dossierMedical.phCNSS.path, 'phCNSS.pdf')

    zip_file.close()

    with open('{}.zip'.format(ipp), 'rb') as file:
        response = HttpResponse(file, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="{}.zip"'.format(ipp)
        return response


def delete_medecin(request):
    if request.method == 'POST':
        medecin_id = request.POST.get('medecin_id')

        try:
            medecin = Medecin.objects.get(id=medecin_id)
            medecin.delete()
            authentification = Authentification.objects.get(id=medecin_id)
            authentification.delete()
            return JsonResponse({'success': True})
        except Medecin.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Medecin not found'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


def delete_technicien(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')

        try:
            technicien = Technicien.objects.get(id=user_id)
            technicien.delete()
            authentification = Authentification.objects.get(id=user_id)
            authentification.delete()
            return JsonResponse({'success': True})
        except Technicien.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Technicien not found'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


def activer_medecin(request):
    if request.method == 'POST' and request.is_ajax():
        medecin_id = request.POST.get('medecin_id')
        try:
            medecin = Medecin.objects.get(id=medecin_id)
            medecin.active = not medecin.active  # Inversion de l'état actuel
            medecin.save()
            authentification = Authentification.objects.get(email=medecin.email)
            authentification.active = not authentification.active  # Inversion de l'état actuel
            authentification.save()
            return JsonResponse({'success': True})
        except Medecin.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Le médecin n\'existe pas.'})
    else:
        return JsonResponse({'success': False, 'message': 'Mauvaise méthode de requête'})
    

def activer_technicien(request):
    if request.method == 'POST' and request.is_ajax():
        user_id = request.POST.get('user_id')
        try:
            technicien = Technicien.objects.get(id=user_id)
            technicien.active = not technicien.active
            technicien.save()
            authentification = Authentification.objects.get(email=technicien.email)
            authentification.active = not authentification.active  # Inversion de l'état actuel
            authentification.save()
            return JsonResponse({'success': True})
        except Technicien.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Technicien non trouvé'})
    
    return JsonResponse({'success': False, 'message': 'Mauvaise méthode de requête'})


def home(request):
    user_id = request.session.get('user_id')
    user_service = request.session.get('user_service')
    if user_id is not None and user_service == "admin":
        user = Authentification.objects.get(id=user_id)
        data = Medecin.objects.filter(active=False)
        return render(request, 'home.html', {'data': data, 'user': user})
    else:
        return render(request, 'login.html')
    

def home2(request):
    user_id = request.session.get('user_id')
    user_service = request.session.get('user_service')
    
    if user_id is not None and user_service == "admin":
        user = Authentification.objects.get(id=user_id)
        data = Technicien.objects.filter(active=False)
        return render(request, 'home2.html', {'data': data, 'user': user})
    else:
        return render(request, 'login.html')
    

def comptes_actives(request):
    user_id = request.session.get('user_id')
    user_service = request.session.get('user_service')
    
    if user_id is not None and user_service == "admin":
        user = Authentification.objects.get(id=user_id)
        data = Medecin.objects.filter(active=True)
        return render(request, 'comptes_actives.html', {'data': data, 'user': user})
    else:
        return render(request, 'login.html')


def comptes_actives2(request):
    user_id = request.session.get('user_id')
    user_service = request.session.get('user_service')
    
    if user_id is not None and user_service == "admin":
        user = Authentification.objects.get(id=user_id)
        data = Technicien.objects.filter(active=True)
        return render(request, 'comptes_actives2.html', {'data': data, 'user': user})
    else:
        return render(request, 'login.html')


def contact(request):
    user_id = request.session.get('user_id')
    user_service = request.session.get('user_service')
    inpe = request.GET.get('medecin')
    if user_id is not None and user_service == "admin":
        user = Authentification.objects.get(id=user_id)
        try:
            medecin = Medecin.objects.get(inpe=inpe)
            return render(request, 'contact.html', {'user': user, 'medecin': medecin})
        except Medecin.DoesNotExist:
            messages.error(request, "Médecin non trouvé")
            return redirect('dossier_accomplir')
    else:
        return render(request, 'login.html')

    

def archive_dossiers(request):
    user_id = request.session.get('user_id')
    user_service = request.session.get('user_service')
    
    if user_id is not None and user_service == "admin":
        current_date = timezone.now().date()
        user = Authentification.objects.get(id=user_id)
        hospitalisations1 = Hospitalisation.objects.filter(date__lt=current_date, imprime=True)
        hospitalisations2 = Hospitalisation.objects.exclude(dpc="", pli_confidentiel="")
        data = hospitalisations1.intersection(hospitalisations2)
        
        ipp_values = data.values_list('ipp', flat=True)
        cin_assure_values = data.values_list('cin_assurant', flat=True)
        
        dossiers = DossierMedical.objects.filter(ipp__in=ipp_values, cinAssure__in=cin_assure_values)
        return render(request, 'archive_dossiers.html', {'data': data, 'dossiers': dossiers, 'user': user})
    else:
        return render(request, 'login.html')




def dossiers_consultation(request):
    user_id = request.session.get('user_id')
    user_service = request.session.get('user_service')
    
    if user_id is not None and user_service == "admin":
        user = Authentification.objects.get(id=user_id)
        current_date = timezone.now().date()
        data = Consultation.objects.filter(date__lt=current_date, action="Consultation")

        ipp_values = data.values_list('ipp', flat=True)
        cin_assure_values = data.values_list('cin_assurant', flat=True)

        dossiers = DossierMedical.objects.filter(ipp__in=ipp_values, cinAssure__in=cin_assure_values)
        return render(request, 'dossiers_consultation.html', {'data': data, 'user': user, 'dossiers':dossiers})
    else:
        return render(request, 'login.html')


def radio_dossiers(request):
    user_id = request.session.get('user_id')
    user_service = request.session.get('user_service')
    
    if user_id is not None and user_service == "admin":
        user = Authentification.objects.get(id=user_id)
        current_date = timezone.now().date()
        data = Radiologie.objects.filter(date__lt=current_date)
        
        ipp_values = data.values_list('ipp', flat=True)
        cin_assure_values = data.values_list('cin_assurant', flat=True)
        
        dossiers = DossierMedical.objects.filter(ipp__in=ipp_values, cinAssure__in=cin_assure_values)
        return render(request, 'radio_dossiers.html', {'data': data, 'user': user, 'dossiers':dossiers})
    else:
        return render(request, 'login.html')


def bio_dossiers(request):
    user_id = request.session.get('user_id')
    user_service = request.session.get('user_service')
    
    if user_id is not None and user_service == "admin":
        user = Authentification.objects.get(id=user_id)
        current_date = timezone.now().date()
        data = Biologie.objects.filter(date__lt=current_date)
                
        ipp_values = data.values_list('ipp', flat=True)
        cin_assure_values = data.values_list('cin_assurant', flat=True)
        
        dossiers = DossierMedical.objects.filter(ipp__in=ipp_values, cinAssure__in=cin_assure_values)
        return render(request, 'bio_dossiers.html', {'data': data, 'user': user, 'dossiers':dossiers})
    else:
        return render(request, 'login.html')


def get_cin(request):
    ipp = request.GET.get('ipp')
    dossier = DossierMedical.objects.filter(ipp=ipp).first()

    response = {'cin': dossier.cinAssure if dossier else "non trouvé"}
    return JsonResponse(response)


def dossiers_prets_hospitalisation(request):
    user_id = request.session.get('user_id')
    user_service = request.session.get('user_service')
    
    if user_id is not None and user_service == "admin":
        user = Authentification.objects.get(id=user_id)
        dossiers = DossierMedical.objects.filter()

        data = Hospitalisation.objects.exclude(dpc="", pli_confidentiel="").annotate(table_name=Value('Hospitalisation', output_field=CharField()))
        return render(request, 'dossiers_prets_hospitalisation.html', {'data': data, 'user': user})
    else:
        return render(request, 'login.html')


def dossiers_prets_consultation(request):
    user_id = request.session.get('user_id')
    user_service = request.session.get('user_service')
    
    if user_id is not None and user_service == "admin":
        user = Authentification.objects.get(id=user_id)
        dossiers = DossierMedical.objects.filter()

        data = Consultation.objects.filter(action="Consultation").annotate(table_name=Value('Consultation', output_field=CharField()))
        return render(request, 'dossiers_prets_consultation.html', {'data': data, 'user': user})
    else:
        return render(request, 'login.html')


def dossiers_prets_radiologie(request):
    user_id = request.session.get('user_id')
    user_service = request.session.get('user_service')
    
    if user_id is not None and user_service == "admin":
        user = Authentification.objects.get(id=user_id)
        dossiers = DossierMedical.objects.filter()

        data = Radiologie.objects.filter().annotate(table_name=Value('Radiologie', output_field=CharField()))
        return render(request, 'dossiers_prets_radiologie.html', {'data': data, 'user': user})
    else:
        return render(request, 'login.html')


def dossiers_prets_biologie(request):
    user_id = request.session.get('user_id')
    user_service = request.session.get('user_service')
    
    if user_id is not None and user_service == "admin":
        user = Authentification.objects.get(id=user_id)
        dossiers = DossierMedical.objects.filter()

        data = Biologie.objects.filter().annotate(table_name=Value('Biologie', output_field=CharField()))
        return render(request, 'dossiers_prets_biologie.html', {'data': data, 'user': user})
    else:
        return render(request, 'login.html')


def dossier_accomplir(request):
    user_id = request.session.get('user_id')
    user_service = request.session.get('user_service')
    
    if user_id is not None and user_service == "admin":
        user = Authentification.objects.get(id=user_id)
        dossiers = DossierMedical.objects.filter()
        data4 = Hospitalisation.objects.filter(
            dpc="",
            pli_confidentiel=""
        ).values('cin_assurant', 'ipp', 'date', 'service','dateSortie', 'medecin').annotate(table_name=Value('Hospitalisation', output_field=CharField()))
        return render(request, 'dossier_accomplir.html', {'data': data4, 'user': user})
    else:
        return render(request, 'login.html')

############# vues du SAA

def saa(request):
    user_id = request.session.get('user_id')
    user_service = request.session.get('user_service')
    
    if user_id is not None and user_service == "SAA":
        user = Authentification.objects.get(id=user_id)
        return render(request, 'saa.html', {'user': user})
    else:
        return render(request, 'login.html')


def saa2(request):
    user_id = request.session.get('user_id')
    user_service = request.session.get('user_service')
    
    if user_id is not None and user_service == "SAA":
        user = Authentification.objects.get(id=user_id)
        return render(request, 'saa2.html', {'user': user})
    else:
        return render(request, 'login.html')


def enregistrer_dossier(request):
    if request.method == 'POST':
        ipp = request.POST.get('ipp')
        cin_assure = request.POST.get('cin_assurant')
        cnss = request.POST.get('cnss')
        phCIN = request.FILES.get('photo_cin')
        phCNSS = request.FILES.get('photo_cnss')
        if not DossierMedical.objects.filter(ipp=ipp, cinAssure=cin_assure, cnss=cnss).exists():
            if not DossierMedical.objects.filter(ipp=ipp).exists():
                if phCIN and phCNSS:
                    dossier_medical = DossierMedical(ipp=ipp, cinAssure=cin_assure, cnss=cnss, phCIN=phCIN, phCNSS=phCNSS)
                    dossier_medical.save()
                    messages.success(request, "Le dossier médical a été ajouté avec succès.")
                    return redirect('saa2')
                else:
                    messages.error(request, "Veuillez remplir tous les champs obligatoires.")
                    return redirect('saa2')
            else:
                messages.error(request, "Le numéro IPP doit être unique, c'est-à-dire qu'il ne doit pas être répété." )
                return redirect('saa2')
        else:
            messages.error(request,  "Ce dossier existe déjà.")
            return redirect('saa2')
           
    return render(request, 'saa2')


def enregistrer_action(request):
    if request.method == 'POST':
        #général
        ipp = request.POST.get('ipp')
        cin_assure = request.POST.get('cin_assurant')
        date = request.POST.get('date')
        action = request.POST.get('actionMed') #--------testeur--------#
        ordonnance = request.FILES.get('ordonnance')
        #consultation
        service = request.POST.get('service') #service pour consultation
        #hospitalisation
        service1 = request.POST.get('service1') #service pour hospitalisation
        date_sortie = request.POST.get('date_sortie')
        facture_hosp=request.FILES.get('facture_hosp')
        billet_hospitalisation = request.FILES.get('billet_hospitalisation')
        medecin = request.POST.get('medecin_list')
        #radiologie       
        facture_radio=request.FILES.get('facture_radio')
        bon_radio = request.FILES.get('bon_radio')
        #biologie
        bon_bio=request.FILES.get('bon_bio')
        facture_bio = request.FILES.get('facture_bio')

        if (DossierMedical.objects.filter(ipp=ipp, cinAssure=cin_assure).exists()) or (cin_assure != "non trouvé"):

            if action == "Consultation":
                consultation = Consultation(
                    ipp=ipp,
                    cin_assurant=cin_assure,
                    date=date,
                    ordonnance=ordonnance,
                    service=service,
                    action="Consultation"
                )
                consultation.save()
                messages.success(request, "La consultation a été ajoutée avec succès.")
                return redirect('saa')

            elif action == "Hospitalisation":
                if date_sortie >= date:
                    hospitalisation = Hospitalisation(
                        ipp=ipp,
                        cin_assurant=cin_assure,
                        date=date,
                        ordonnance=ordonnance,
                        service=service1,
                        dateSortie=date_sortie,
                        facture=facture_hosp,
                        billetHospitalisation=billet_hospitalisation,
                        action=action,
                        medecin=medecin
                    )
                    hospitalisation.save()
                    messages.success(request,"L'hospitalisation a été ajoutée avec succès.")
                    return redirect('saa')
                else:
                    messages.error(request, "La date de sortie doit être supérieure à la date d'entrée.")
                    return redirect('saa')

            elif action == "Radiologie":
                radiologie = Radiologie(
                    ipp=ipp,
                    cin_assurant=cin_assure,
                    date=date,
                    ordonnance=ordonnance,
                    service="Radiologie",
                    facture=facture_radio,
                    bonRadio=bon_radio,
                    action=action
                )
                radiologie.save()
                messages.success(request,  "L'acte de radiologie a été ajouté avec succès.")
                return redirect('saa')

            elif action == "Biologie":
                biologie = Biologie(
                    ipp=ipp,
                    cin_assurant=cin_assure,
                    date=date,
                    ordonnance=ordonnance,
                    service="Biologie",
                    facture=facture_bio,
                    bonBio=bon_bio,
                    action=action
                )
                biologie.save()
                messages.success(request, "L'acte de biologie a été ajouté avec succès." )
                return redirect('saa')

            else:
                messages.error(request,"Vérifiez les champs.")
                return redirect('saa')

        else:
            messages.error(request, "Vérifiez le CIN ou l'IPP du patient, ou essayez d'ajouter un dossier pour ce patient.")
            return redirect('saa')
    else:
        messages.error("Erreur lors la soumission")
        return redirect('saa')


def liste_hospitalisations(request):
    user_id = request.session.get('user_id')
    user_service = request.session.get('user_service')
    if user_id is not None and user_service == "SAA":
        user = Authentification.objects.get(id=user_id)
        data = Hospitalisation.objects.filter(imprime=False)
        return render(request, 'liste_hospitalisations.html', {'data': data, 'user': user})
    else:
        return render(request, 'login.html')
    
def modifier_hospitalisation(request):
    if request.method == 'POST':
        cin_assure = request.POST.get('inputCinAssurehosp')
        ipp = request.POST.get('inputIPhosp')
        date_entree = request.POST.get('inputDatehosp')
        service = request.POST.get('inputServicehosp')
        data=Hospitalisation.objects.filter(imprime=False)
        try:
            hospitalisation = Hospitalisation.objects.get(cin_assurant=cin_assure, ipp=ipp, date=date_entree, service=service)
            hospitalisation.dateSortie = request.POST.get('inputDateSortie')
            newOrdonnance = request.FILES.get('inputOrdonnancehosp')
            newBillet = request.FILES.get('inputbillet')
            newFacture = request.FILES.get('inputFacturehosp')
            hospitalisation.service = request.POST.get('inputServicehosp')

            if newBillet:
                hospitalisation.billetHospitalisation = newBillet
            
            if newOrdonnance:
                hospitalisation.ordonnance = newOrdonnance

            if newFacture:
                hospitalisation.facture = newFacture

            if hospitalisation.save() is None:
                messages.success(request, 'Modifié avec succès')
                return redirect('liste_hospitalisations')
            else:
                messages.error(request, "Erreur lors de la modification")                
                return redirect('liste_hospitalisations')
        
        except Hospitalisation.DoesNotExist:
            pass

    return render(request, 'liste_hospitalisations.html')

def supprimer_hospitalisation(request):
    if request.method == 'POST':
        cin_assure = request.POST.get('cinAssure')
        ipp = request.POST.get('ipp')
        date= request.POST.get('date')
        service =request.POST.get('service')
        data = Hospitalisation.objects.filter()
        if Hospitalisation.objects.filter(cin_assurant=cin_assure, ipp=ipp, date=date, service=service).delete():
            messages.success(request,"Supprimé avec succées")
            return redirect('liste_hospitalisations')
        else:
            messages.error(request,'Erreur lors la suppression')
            return redirect('liste_hospitalisations')
    else:
        return redirect('liste_hospitalisations')


def liste_radiologies(request):
    user_id = request.session.get('user_id')
    user_service = request.session.get('user_service')
    if user_id is not None and user_service == "SAA":
        user = Authentification.objects.get(id=user_id)
        data = Radiologie.objects.filter(imprime=False)
        return render(request, 'liste_radiologies.html', {'data': data, 'user': user})
    else:
        return render(request, 'login.html')


def modifier_radiologie(request):
    if request.method == 'POST':
        cin_assure = request.POST.get('inputCinAssure')
        ipp = request.POST.get('inputIPP')
        date_entree = request.POST.get('inputDate')
        service = request.POST.get('inputService')
        try:
            radiologie = Radiologie.objects.get(cin_assurant=cin_assure, ipp=ipp, date=date_entree, service=service)
            newOrdonnance = request.FILES.get('inputOrdonnance')
            newFacture = request.FILES.get('inputBon')
            newBon = request.FILES.get('inputFacture')
            radiologie.service = request.POST.get('inputService')
            data = Radiologie.objects.filter(imprime=False)

            if newOrdonnance:
                radiologie.ordonnance = newOrdonnance
            if newFacture:
                radiologie.facture = newFacture
            if newBon:
                radiologie.bonRadio = newBon

            if radiologie.save() is None:
                messages.success(request, "Modifié avec succès" )
                return redirect('liste_radiologies')
            else:
                messages.error(request,"Erreur lors de la modification" )
                return redirect('liste_radiologies')

        except Radiologie.DoesNotExist:
            pass

    return redirect('liste_radiologies')


def supprimer_radiologie(request):
    if request.method == 'POST':
        cin_assure = request.POST.get('cinAssure')
        ipp = request.POST.get('ipp')
        date= request.POST.get('date')
        service =request.POST.get('service')
        data = Radiologie.objects.filter(imprime=False)
        if Radiologie.objects.filter(cin_assurant=cin_assure, ipp=ipp, date=date, service=service).delete():
            messages.success(request,"Supprimé avec succées")
            return redirect('liste_radiologies')
        else:
            messages.error(request,'Erreur lors la suppression')
            return redirect('liste_radiologies')
    else:
        return redirect('liste_radiologies')


def liste_biologies(request):
    user_id = request.session.get('user_id')
    user_service = request.session.get('user_service')
    if user_id is not None and user_service == "SAA":
        user = Authentification.objects.get(id=user_id)
        data = Biologie.objects.filter(imprime=False)
        return render(request, 'liste_biologies.html', {'data': data, 'user': user})
    else:
        return render(request, 'login.html')
    

def modifier_biologie(request):
    if request.method == 'POST':
        cin_assure = request.POST.get('inputCinAssure')
        ipp = request.POST.get('inputIPP')
        date_entree = request.POST.get('inputDate')
        service = request.POST.get('inputService')
        try:
            biologie = Biologie.objects.get(cin_assurant=cin_assure, ipp=ipp, date=date_entree, service=service)
            newOrdonnance = request.FILES.get('inputOrdonnance')
            newFacture = request.FILES.get('inputBon')
            newBon = request.FILES.get('inputFacture')
            biologie.service = request.POST.get('inputService')
            data = Biologie.objects.filter(imprime=False)

            if newOrdonnance:
                biologie.ordonnance = newOrdonnance
            if newFacture:
                biologie.facture = newFacture
            if newBon:
                biologie.bonBio = newBon

            if biologie.save() is None:
                messages.success(request,"Modifié avec succès" )
                return redirect('liste_biologies')
            else:
                messages.error(request,"Erreur lors de la modification" )
                return redirect('liste_biologies')

        except Biologie.DoesNotExist:
            pass

    return redirect('liste_biologies')

def supprimer_biologie(request):
    if request.method == 'POST':
        cin_assure = request.POST.get('cinAssure')
        ipp = request.POST.get('ipp')
        date= request.POST.get('date')
        service =request.POST.get('service')
        data = Biologie.objects.filter(imprime=False)
        if Biologie.objects.filter(cin_assurant=cin_assure, ipp=ipp, date=date, service=service).delete():
            messages.success(request,"Supprimé avec succées")
            return redirect('liste_biologies')
        else:
            messages.error(request,'Erreur lors la suppression')
            return redirect('liste_biologies')
    else:
        return redirect('liste_biologies')




def liste_consultations(request):
    user_id = request.session.get('user_id')
    user_service = request.session.get('user_service')
    if user_id is not None and user_service == "SAA":
        user = Authentification.objects.get(id=user_id)
        data = Consultation.objects.filter(action="Consultation",imprime=False)
        return render(request, 'liste_consultations.html', {'data': data, 'user': user})
    else:
        return render(request, 'login.html')


def modifier_consultation(request):
    if request.method == 'POST':
        cin_assure = request.POST.get('inputCinAssurehosp')
        ipp = request.POST.get('inputIPhosp')
        date_entree = request.POST.get('inputDatehosp')
        service = request.POST.get('inputServicehosp')
        try:
            consultation = Consultation.objects.get(cin_assurant=cin_assure, ipp=ipp, date=date_entree, service=service, action="Consultation")
            newOrdonnance = request.FILES.get('inputOrdonnancehosp')
            consultation.service = request.POST.get('inputServicehosp')
            data=Consultation.objects.filter(action="Consultation",imprime=False)

            if newOrdonnance:
                consultation.ordonnance = newOrdonnance

            if consultation.save() is None:
                messages.success(request,"Modifié avec succés" )
                return redirect('liste_consultations')
            else:
                messages.error(request, "Erreur lors la modification")
                return redirect('liste_consultations')

        except Consultation.DoesNotExist:
            pass

    return redirect('liste_consultations')

def supprimer_consultation(request):
    if request.method == 'POST':
        cin_assure = request.POST.get('cinAssure')
        ipp = request.POST.get('ipp')
        date= request.POST.get('date')
        service =request.POST.get('service')
        data = Consultation.objects.filter(action="consultation",imprime=False)
        if Consultation.objects.filter(cin_assurant=cin_assure, ipp=ipp, date=date, service=service, action="Consultation").delete():
            messages.success(request,"Supprimé avec succées")
            return redirect('liste_consultations')
        else:
            messages.error(request,'Erreur lors la suppression')
            return redirect('liste_consultations')
    else:
        return redirect('liste_consultations')

def liste_dossiers(request):
    user_id = request.session.get('user_id')
    user_service = request.session.get('user_service')
    if user_id is not None and user_service == "SAA":
        user = Authentification.objects.get(id=user_id)
        data = DossierMedical.objects.filter()
        return render(request, 'liste_dossiers.html', {'data': data, 'user': user})
    else:
        return render(request, 'login.html')
    

def modifier_dossier(request):
    if request.method == 'POST':
        cin_assure = request.POST.get('cinAssure')
        ipp = request.POST.get('ipp')
        cnss = request.POST.get('cnss')
        new_ph_cin = request.FILES.get('NewphCIN')
        new_ph_cnss = request.FILES.get('NewphCNSS')
        data = DossierMedical.objects.filter()

        dossier = get_object_or_404(DossierMedical, cinAssure=cin_assure, ipp=ipp)

        dossier.cnss = cnss
        if new_ph_cin:
            dossier.phCIN = new_ph_cin
        if new_ph_cnss:
            dossier.phCNSS = new_ph_cnss
        if dossier.save() is None :
            messages.success(request, 'Modifié avec succès')
            return redirect('liste_dossiers')
        else:
            messages.error(request, 'Erreur la modification')
            return redirect('liste_dossiers')
    else:
        return render(request, 'liste_dossiers.html', {'data': data})


def supprimer_dossier(request):
    if request.method == 'POST':
        cin_assure = request.POST.get('cinAssure')
        ipp = request.POST.get('ipp')
        data = DossierMedical.objects.filter()
        if DossierMedical.objects.filter(cinAssure=cin_assure, ipp=ipp).exists():
            if not Consultation.objects.filter(cin_assurant=cin_assure, ipp=ipp).exists():
                dossier = get_object_or_404(DossierMedical, cinAssure=cin_assure, ipp=ipp)
                dossier.delete()
                messages.success(request, "Dossier supprimer avec succès")
                return redirect('liste_dossiers')
            else :
                error_message="Vous ne pouvez pas supprimer le dossier qui a "+ipp+" comme ipp car il a des actions enregistrés"
                messages.error(request,error_message)
                return redirect('liste_dossiers')
        else:
            error_message = "Erreur lors la suppression"
            messages.error(request,error_message)
            return redirect('liste_dossiers')
    else:
        return redirect('liste_dossiers')


def get_medecins(request, service):
    medecins = Medecin.objects.filter(service_medecin=service, active =True).values('nom_complet', 'inpe')
    return JsonResponse({'medecins': list(medecins)})

############## vues du connexion
def validate_email(email):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_regex, email)


def validate_phone(phone):
    phone_regex = r'^(\+212|00212|0)(6|7)[0-9]{8}$'
    return re.match(phone_regex, phone)


def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


from django.core.mail import send_mail, BadHeaderError

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            auth = Authentification.objects.get(email=email)
        except Authentification.DoesNotExist:
            messages.error(request, "Cet e-mail n'est associé à aucun compte.")
            return redirect('login')
        
        # Génération d'un nouveau mot de passe aléatoire
        new_password = generate_random_password()
        auth.password = new_password
        auth.save()
        
        # Envoi de l'e-mail avec le nouveau mot de passe
        try:
            if send_mail(
                'Réinitialisation du mot de passe',
                f'Bonjour, votre nouveau mot de passe est : {new_password}',
                'noreply@example.com',
                [email],
                fail_silently=False,
            ):
                    messages.success(request, "Un e-mail contenant le nouveau mot de passe a été envoyé à votre adresse.")
                    return redirect('login')
        except BadHeaderError:
            messages.error(request, "Erreur lors de l'envoi de l'e-mail.")
            return redirect('login')
    
    return render(request, 'login.html')

def signup(request):
    poste = Personne._meta.get_field('poste_role').choices
    roles = Technicien._meta.get_field('service_role').choices
    serviceMedecin = Medecin._meta.get_field('service_medecin').choices

    if request.method == 'POST':
        nom = request.POST['nom']
        password = request.POST['password']
        adresse = request.POST['adresse']
        email = request.POST['email']
        tele = request.POST['tele']
        service = request.POST['roles']
        service1 = request.POST['roles1'] 
        inpe= request.POST['inpe']
        poste = request.POST['poste']

        if not validate_email(email):
            error_message = "Format d'email non valide"
            return render(request, 'signup.html', {'roles': roles, 'error_message': error_message})
            
            # Valider le format du téléphone
        if not validate_phone(tele):
            error_message = "Format de téléphone non valide"
            return render(request, 'signup.html', {'roles': roles, 'error_message': error_message})
        
        if poste =="medecin":
            if nom and password and adresse and email and tele and service1:
                respo = request.POST.get('respo')
                if respo == "on":
                    respo = True
                else :
                    respo = False

                medecin = Medecin(
                    nom_complet=nom,
                    password=password,
                    adresse=adresse,
                    email=email,
                    tele=tele, 
                    inpe =inpe,
                    poste_role=poste,
                    service_medecin=service1,
                    responsable=respo
                )
                medecin.save()

                authentification = Authentification(
                    nom_complet = nom,
                    email = email,
                    password = password,
                    service = service1
                )
                authentification.save()
                success_message= 'ajouté avec succés'
                messages.success(request,success_message)
                return redirect('login')
            else:
                error_message = "Tous les champs doivent être remplis"
                return render(request, 'signup.html', {'roles': roles, 'error_message': error_message,'poste':poste, 'serviceMedecin':serviceMedecin})

        
        if poste == "technicien" :
            if nom and password and adresse and email and tele and service:
                personnel = Technicien(
                    nom_complet=nom,
                    password=password,
                    adresse=adresse,
                    email=email,
                    tele=tele, 
                    poste_role=poste,
                    service_role=service
                )
                personnel.save()
                authentification = Authentification(
                    nom_complet = nom,
                    email = email,
                    password = password,
                    service = service
                )
                authentification.save()
                messages.success(request,'ajouté avec succès')
                return redirect('login')
            else:
                error_message = "Tous les champs doivent être remplis"
                return render(request, 'signup.html', {'roles': roles, 'error_message': error_message,'poste':poste, 'serviceMedecin':serviceMedecin})
            
    return render(request, 'signup.html', {'roles':roles,'poste':poste,'serviceMedecin':serviceMedecin})


@never_cache
def login(request):
    request.session.flush()
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        if Authentification.objects.filter(email=username, password=password).exists():
            user = Authentification.objects.filter(email=username, password=password).first()
            if user.active :
                if user.service == "admin":
                    request.session['user_id'] = user.id
                    request.session['user_service'] = user.service
                    return redirect('home')
                elif user.service == "pediaterie":
                    request.session['user_id'] = user.id
                    request.session['user_service'] = user.service
                    return redirect('pediaterie')
                elif user.service == "SAA" :
                        request.session['user_id'] = user.id
                        request.session['user_service'] = user.service
                        return redirect('saa')
                else:
                    messages.error(request, 'Identifiants invalides')
                    return render(request, 'login.html')
            else:
                messages.error(request, 'Compte non activé')
                return render(request, 'login.html')
        else:
            messages.error(request, 'Identifiants invalides')
            return render(request, 'login.html')

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    request.session.flush()
    return redirect('login')

####################################################################
########################################################## 

# """def home_M(request):
#     return render(request , 'home_M.html')

# def scan_M(request):
#     return render(request , 'scan_M.html')

# def prischarge(request):
#     return render(request, 'prischarge.html')   

# def contact_M(request):
#     return render(request, 'contact_M.html') 
# def archive_P(request):
#     return render(request, 'archive_P.html') 
# def archive_CH(request):
#     return render(request, 'archive_CH.html') 

# header_image = "testme/static/img/header.png"
# footer_image = "testme/static/img/footer.png"
# #generate pdf pli confidentiel
# from reportlab.lib.pagesizes import letter
# from reportlab.lib.units import inch
# from reportlab.pdfgen import canvas
# from reportlab.pdfbase import pdfmetrics
# from io import BytesIO
# from django.http import HttpResponse

# def generate_pdf(request):
#     # Retrieve form data
#     nom_prenom = request.POST.get('NomPrenom')
#     date_entree = request.POST.get('DateEntree')
#     date_sortie = request.POST.get('DateSortie')
#     admission = request.POST.get('Admission')
#     service = request.POST.get('Service')
#     motif_hospitalisation = request.POST.get('Motif')
#     compte_rendu_hospitalisation = request.POST.get('CompteRendu')
#     compte_rendu_operatoire = request.POST.get('CompteOperatoire')

#     # Create a BytesIO buffer to store the PDF content
#     buffer = BytesIO()

#     # Create the PDF object
#     p = canvas.Canvas(buffer, pagesize=letter)

#     # Set the font and font size for the header and footer
#     p.setFont("Helvetica-Bold", 12)
#     # Split the text into lines based on the line width
#     text = f"Objet: PI Confidentiel"
#     text_width = pdfmetrics.stringWidth(text, "Helvetica", 14)
#     center_x = (letter[0] - text_width) / 2

#     # Load and draw the header image
#     header_image = "testme/static/img/header.png"  # Replace with your own image file
#     header_width = 4.5 * inch
#     header_height = 1.0 * inch
#     header_x = 150
#     header_y = 700
#     p.drawImage(header_image, header_x, header_y, width=header_width, height=header_height)

#     # Load and draw the footer image
#     footer_image = "testme/static/img/footer.png"  # Replace with your own image file
#     footer_width = 2.5 * inch
#     footer_height = 0.5 * inch
#     footer_x = 200
#     footer_y = 20
#     p.drawImage(footer_image, footer_x, footer_y, width=footer_width, height=footer_height)

#     # Write the form data to the PDF body
#     body_x = 100
#     body_y = 600

# # Write the form data to the PDF
#     p.setFont("Helvetica", 12)
#     p.drawString(100, 600, f"Nom et prénom du patient: {nom_prenom}")
#     p.setFont("Helvetica", 12)
#     p.drawString(100, 580, f"Date d'entrée: {date_entree}")
#     p.drawString(300, 580, f"Date de sortie: {date_sortie}")
#     p.drawString(100, 560, f"N°d'Admission: {admission}")
#     p.drawString(300, 560, f"Service: {service}")
#     p.setFont("Helvetica", 12)
#     p.drawString(center_x, 520, text)
#     p.drawString(100, 500, f"Motif d'hospitalisation: {motif_hospitalisation}")
#     p.drawString(100, 400, f"Compte rendu d'hospitalisation : {compte_rendu_hospitalisation}")
#     p.drawString(100, 350, f"Compte rendu Opératoire: {compte_rendu_operatoire}")
#     p.setFont("Helvetica", 10)
#     p.drawString(400, 300, f"Signature et cachet du mdecin")

#     # Save the PDF
#     p.showPage()
#     p.save()

#     # Set the filename of the generated PDF with the patient's name
#     filename = f"{nom_prenom}_fichier.pdf"

#     # Create the HTTP response with the PDF content
#     buffer.seek(0)
#     response = HttpResponse(buffer, content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="{filename}"'
#     return response



# def liste_dossiers_patients(request):
#     dossiers = DossierPatient.objects.all()
#     return render(request, 'testme/liste_dossiers_patients.html', {'dossiers': dossiers})



# def generate_pdf_pris(request):
#     if request.method == 'POST':
#         immatriculation = request.POST.get('immatriculation', '')
#         nomPrenomAssure = request.POST.get('nomPrenomAssure', '')

#         # Data for the table
#         data = [
#             ["Frals de séjour", "Séjour normal", "Solns intensils", "Réanimation", "Couveuse"],
#             ["Nbre jours", "", "", "", ""],
#             ["Tarif unitaire", "", "", "", ""],
#             ["Total", "", "", "", ""],
#         ]
#         style = TableStyle([
#             ("BACKGROUND", (0, 0), (0, 3), colors.grey),
#             ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
#             ("ALIGN", (0, 0), (-1, -1), "CENTER"),
#             ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
#             ("FONTSIZE", (0, 0), (-1, 0), 12),
#             ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
#             ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
#             ("GRID", (0, 0), (-1, -1), 1, colors.black),
#         ])

#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="report.pdf"'

#         # Create the PDF document
#         doc = SimpleDocTemplate(response, pagesize=letter)

#         # Create the table
#         table = Table(data)

#         # Apply the style to the table
#         table.setStyle(style)

#         # Build the story and add the table
#         story = []
#         story.append(table)
#         doc.build(story)

#         return response

#     return render(request, 'prischarge.html')
#     """
