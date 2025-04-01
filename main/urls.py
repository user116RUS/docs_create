from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('create_docs/', views.CreateDocs.as_view(), name='create_docs')
]
