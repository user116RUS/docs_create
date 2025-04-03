from django.contrib.auth.views import LoginView
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
        'create_docs/',
        views.CreateDocs.as_view(template_name='main/create_docs.html'),
        name='create_docs'
    ),
]
