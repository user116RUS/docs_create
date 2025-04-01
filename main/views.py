from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from main.models import Document, Organisation

from .forms import DocsForm

from django.views.generic.edit import CreateView


def index(request):
    return render(request, template_name='main/index.html')


class CreateDocs(CreateView):
    form_class = DocsForm
    template_name = 'main/create_docs.html'
    success_url = '/'
