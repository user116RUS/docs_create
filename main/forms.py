from django import forms
from .models import Documents


class DocsForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = ('address_and_time')
