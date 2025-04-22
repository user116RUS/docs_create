from django import forms
from django.forms import inlineformset_factory
from .models import Document, Organisation, Service, ViewerCategory


class DateInput(forms.DateInput):
    """Кастомный виджет для выбора даты с календарем"""
    input_type = 'date'
    
    def __init__(self, attrs=None, format=None):
        default_attrs = {'class': 'form-control minecraft-datepicker'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs, format)


class DocsForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = (
            'address_and_time',
            'date',
            'price_in_figures',
            'price_in_words',
            'time',
            'act_and_account_number',
            'number_basis_of_the_contract',
            'doer',
            'customer',
            'services',
            'viewers',
        )
        widgets = {
            'date': DateInput(),
        }


class OrganisationForm(forms.ModelForm):
    class Meta:
        model = Organisation
        fields = (
            'name',
            'requisites',
            'fio',
            'function',
            'inn',
            'bik',
            'bank_name',
            'short_name',
            'correspondent_bank_account',
            'bank_account',
            'kpp',
            'address',
            'is_our',
        )


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('name', 'date')
        

class ViewerCategoryForm(forms.ModelForm):
    class Meta:
        model = ViewerCategory
        fields = ('viewers', 'price')


# Создаем формсет для категорий зрителей внутри услуги
ViewerCategoryFormset = inlineformset_factory(
    Service, 
    ViewerCategory,
    form=ViewerCategoryForm,
    extra=1,  # Количество пустых форм
    can_delete=True
)
