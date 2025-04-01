from django import forms
from .models import Document


class DocsForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = [
            'address_and_time',
            'number_of_people',
            'date',
            'price_in_figures',
            'price_in_words',
            'time',
            'act_and_account_number',
            'number_basis_of_the_contract',
            'doer',
            'customer'
        ]
