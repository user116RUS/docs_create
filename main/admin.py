from django.contrib import admin
from .models import Organisation, Document

@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('name', 'inn', 'kpp', 'is_our')
    list_filter = ('is_our',)
    search_fields = ('name', 'inn', 'kpp', 'address')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'short_name', 'is_our')
        }),
        ('Реквизиты', {
            'fields': ('inn', 'kpp', 'requisites')
        }),
        ('Банковские реквизиты', {
            'fields': ('bik', 'bank_name', 'bank_account', 'correspondent_bank_account')
        }),
        ('Дополнительная информация', {
            'fields': ('fio', 'address')
        }),
    )

@admin.register(Document)
class DocumentsAdmin(admin.ModelAdmin):
    list_display = ('act_and_account_number', 'date', 'time', 'price_in_figures', 'doer', 'customer')
    list_filter = ('date', 'doer', 'customer')
    search_fields = ('act_and_account_number', 'number_basis_of_the_contract', 'address_and_time')
    fieldsets = (
        ('Основная информация', {
            'fields': ('act_and_account_number', 'number_basis_of_the_contract', 'date', 'time')
        }),
        ('Стоимость', {
            'fields': ('price_in_figures', 'price_in_words')
        }),
        ('Детали проведения', {
            'fields': ('address_and_time', 'number_of_people')
        }),
        ('Участники', {
            'fields': ('doer', 'customer')
        }),
    )
