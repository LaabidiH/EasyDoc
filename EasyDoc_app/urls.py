from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
"""
from testme.views import generate_pdf
from testme.views import liste_dossiers_patients
from testme.views import generate_pdf_pris
"""

urlpatterns = [
    path("",views.login, name="login"),
    path("home/",views.home, name="home"),
    path('home2/', views.home2, name='home2'),
    path("comptes_actives",views.comptes_actives, name="comptes_actives"),
    path("comptes_actives2",views.comptes_actives2, name="comptes_actives2"),
    path("contact",views.contact, name="contact"),
    path('signup/', views.signup, name='signup'),
    path('dossiers_consultation/', views.dossiers_consultation, name='dossiers_consultation'),
    path('archive_dossiers/', views.archive_dossiers, name='archive_dossiers'),
    path('radio_dossiers/', views.radio_dossiers, name='radio_dossiers'),
    path('bio_dossiers/', views.bio_dossiers, name='bio_dossiers'),
    path('saa/', views.saa, name='saa'),
    path('saa2/', views.saa2, name='saa2'),
    path('user_login/', views.login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('activer-medecin/', views.activer_medecin, name='activer_medecin'),
    path('activer-technicien/', views.activer_technicien, name='activer_technicien'),
    path('desactiver-medecin/', views.activer_medecin, name='desactiver_medecin'),
    path('desactiver-technicien/', views.activer_technicien, name='desactiver_technicien'),
    path('delete-medecin/', views.delete_medecin, name='delete_medecin'),
    path('delete-technicien/', views.delete_technicien, name='delete_technicien'),
    path('enregistrer_dossier/', views.enregistrer_dossier, name='enregistrer_dossier'),
    path('enregistrer_action/', views.enregistrer_action,name='enregistrer_action'),
    path('dossiers_prets_hospitalisation/', views.dossiers_prets_hospitalisation,name='dossiers_prets_hospitalisation'),
    path('dossiers_prets_consultation/', views.dossiers_prets_consultation,name='dossiers_prets_consultation'),
    path('dossiers_prets_biologie/', views.dossiers_prets_biologie,name='dossiers_prets_biologie'),
    path('dossiers_prets_radiologie/', views.dossiers_prets_radiologie,name='dossiers_prets_radiologie'),
    path('dossier_accomplir/', views.dossier_accomplir,name='dossier_accomplir'),
    path('get_cin/', views.get_cin, name='get_cin'),
    path('liste_dossiers/', views.liste_dossiers, name='liste_dossiers'),
    path('modifier-dossier/<int:dossier_id>/', views.modifier_dossier, name='modifier_dossier'),
    path('modifier_dossier/', views.modifier_dossier, name='modifier_dossier'),
    path('supprimer-dossier/', views.supprimer_dossier, name='supprimer_dossier'),
    path('imprimer-dossier-hospitalisation/<str:ipp>/<str:cin>/<str:date>/', views.imprimer_dossier_hospitalisation, name='imprimer_dossier_hospitalisation'),
    path('imprimer-dossier-biologie/<str:ipp>/<str:cin>/<str:date>/', views.imprimer_dossier_biologie, name='imprimer_dossier_biologie'),
    path('imprimer-dossier-radiologie/<str:ipp>/<str:cin>/<str:date>/', views.imprimer_dossier_radiologie, name='imprimer_dossier_radiologie'),
    path('imprimer-dossier-consultation/<str:ipp>/<str:cin>/<str:date>/', views.imprimer_dossier_consultation, name='imprimer_dossier_consultation'),
    path('get_medecins/<str:service>/', views.get_medecins, name='get_medecins'),
    path('reset_password/', views.reset_password, name='reset_password'),

    # path('home_M/', views.home_M, name="home_M"),
    # path('generate-pdf/', generate_pdf, name='generate_pdf'),
    # path('scan_M/', views.scan_M, name='scan_M'),
    # path('prischarge/', views.prischarge, name='prischarge'),
    # path('contact_M/', views.contact_M, name='contact_M'),
    # path('archive_CH/', views.archive_CH, name='archive_CH'),
    # path('archive_P/', views.archive_P, name='archive_P'),
    # path('dossiers/', liste_dossiers_patients, name='liste_dossiers_patients'),
    # path('generate-pdf_pris/', generate_pdf_pris, name='generate_pdf_pris'),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)