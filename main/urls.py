from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from main import views

app_name = 'main'

urlpatterns = [
    path(
        '',
        views.index, name='index'
    ),
    path(
        'login/',
        LoginView.as_view(template_name='main/login.html'),
        name='login'
    ),
    path(
        'logout/',
        LogoutView.as_view(template_name='main/logged_out.html'),
        name='logout'
    ),
    path(
        'create_docs/',
        views.CreateDocs.as_view(template_name='main/create_docs.html'),
        name='create_docs'
    ),
    path(
        'create_organisation/',
        views.OrganisationView.as_view(),
        name='create_organisation'
    ),
    path(
        'organisations/',
        views.organisations_list,
        name='organisations_list'
    ),
    path(
        'organisations/edit/<int:pk>/',
        views.OrganisationUpdateView.as_view(),
        name='edit_organisation'
    ),
    path(
        'organisations/delete/<int:pk>/',
        views.delete_organisation,
        name='delete_organisation'
    ),
    path(
        'create_service/',
        views.create_service,
        name='create_service'
    ),
    path(
        'edit_service/<int:service_id>/',
        views.edit_service,
        name='edit_service'
    ),
    path(
        'documents/<int:document_id>/',
        views.document_detail,
        name='document_detail'
    ),
    path(
        'documents/<int:document_id>/act/',
        views.download_act,
        name='download_act'
    ),
    path(
        'documents/<int:document_id>/invoice/',
        views.download_invoice,
        name='download_invoice'
    ),
    path(
        'documents/<int:document_id>/contract/',
        views.download_contract,
        name='download_contract'
    ),
    path(
        'documents/<int:document_id>/all/',
        views.download_all_docs,
        name='download_all_docs'
    ),
    path(
        'documents/',
        views.documents_list,
        name='documents_list'
    ),
    path(
        'documents/edit/<int:pk>/',
        views.DocumentUpdateView.as_view(),
        name='edit_document'
    ),
    path('service-ajax/', views.service_ajax, name='service_ajax'),
    path('extract-organisation-data/', views.extract_organisation_data, name='extract_organisation_data'),
    path('get-organisations-data/', views.get_organisations_data, name='get_organisations_data'),
]
