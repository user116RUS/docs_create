from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse, FileResponse
from django.template.loader import get_template
import os
import io
from docx import Document as DocxDocument
from docx.shared import Pt
from docxtpl import DocxTemplate
from django.forms import modelformset_factory

from main.models import Document, Organisation, Service, ViewerCategory

from .forms import DocsForm, OrganisationForm, ServiceForm, ViewerCategoryForm, ViewerCategoryFormset

from django.views.generic.edit import CreateView


def index(request):
    print('> tested')
    return render(request, template_name='main/index.html')


class CreateDocs(CreateView):
    form_class = DocsForm
    template_name = 'main/create_docs.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        services = Service.objects.all()
        
        # Добавляем отладочную информацию
        for service in services:
            print(f"Service: {service.name}")
            print(f"Total viewers: {service.total_viewers}")
            print(f"Total price: {service.total_price}")
            print("Categories:")
            for category in service.viewer_categories.all():
                print(f"  - {category.viewers} viewers, {category.price} rub")
            print("---")
        
        context['services'] = services
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        
        # Проверяем, что форма валидна
        if form.is_valid():
            try:
                # Создаем и сохраняем объект
                self.object = form.save()
                print(f"Document created: {self.object.id}")
                
                # Явно указываем перенаправление на страницу загрузки документов
                success_url = reverse('main:document_detail', kwargs={'document_id': self.object.id})
                return redirect(success_url)
            except Exception as e:
                print(f"Error saving document: {e}")
                form.add_error(None, f"Ошибка при сохранении документа: {e}")
                return self.form_invalid(form)
        else:
            # Проверяем, есть ли услуги в запросе
            if 'services' not in request.POST and not request.POST.getlist('services'):
                form.add_error(None, "Пожалуйста, выберите хотя бы одну услугу.")
                
            # Проверяем, заполнено ли поле количества зрителей
            if not request.POST.get('viewers', '').strip():
                form.add_error('viewers', "Пожалуйста, укажите количество зрителей.")
                
            # Проверяем, заполнено ли поле суммы прописью
            if not request.POST.get('price_in_words', '').strip():
                form.add_error('price_in_words', "Пожалуйста, укажите сумму прописью.")
            
            print(f"Form is invalid: {form.errors}")
            return self.form_invalid(form)
    
    def get_success_url(self):
        return reverse('main:document_detail', kwargs={'document_id': self.object.id})


class OrganisationView(CreateView):
    form_class = OrganisationForm
    template_name = 'main/create_organisation.html'
    success_url = '/'


def create_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save()
            
            # Обработка формсета с категориями зрителей
            formset = ViewerCategoryFormset(request.POST, instance=service)
            if formset.is_valid():
                formset.save()
                return redirect('main:create_docs')
    else:
        form = ServiceForm()
        formset = ViewerCategoryFormset()
    
    return render(request, 'main/create_service.html', {
        'form': form,
        'formset': formset
    })


def edit_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            service = form.save()
            
            # Обработка формсета с категориями зрителей
            formset = ViewerCategoryFormset(request.POST, instance=service)
            if formset.is_valid():
                formset.save()
                return redirect('main:create_docs')
    else:
        form = ServiceForm(instance=service)
        formset = ViewerCategoryFormset(instance=service)
    
    return render(request, 'main/create_service.html', {
        'form': form,
        'formset': formset,
        'service': service
    })


def document_detail(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    return render(request, 'main/download_docs.html', {'document': document})


def download_act(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    
    # Получаем путь к шаблону акта приемки
    template_path = os.path.join(os.path.dirname(__file__), 'document_templates', 'act_priemki.docx')
    
    # Получаем все услуги
    services = document.services.all()
    # Создаем строку с именами услуг через запятую
    services_text = ", ".join([service.name for service in services])
    
    # Создаем строку с датами через запятую
    dates = ", ".join([service.date for service in services])
    
    # Создаем строку, содержащую название услуги и дату
    service_date = ", ".join([f'{service.name} - {service.date}' for service in services])
    
    # Создаем структуру данных для таблицы с услугами и категориями зрителей
    services_table = []
    total_sum = 0
    total_viewers = 0
    
    for i, service in enumerate(services, 1):
        # Если у услуги есть категории зрителей, создаем строки для каждой категории
        if service.viewer_categories.exists():
            for j, category in enumerate(service.viewer_categories.all(), 1):
                category_total = category.viewers * category.price
                total_sum += category_total
                total_viewers += category.viewers
                
                services_table.append({
                    'num': i if j == 1 else '',  # Номер услуги только для первой категории
                    'service_name': service.name if j == 1 else '',  # Название услуги только для первой категории
                    'service_date': service.date if j == 1 else '',  # Дата услуги только для первой категории
                    'category': True,  # Это категория зрителей
                    'viewers': category.viewers,
                    'price': category.price,
                    'total': category_total,
                    'is_first_category': j == 1,  # Флаг первой категории для форматирования
                    'is_last_category': j == service.viewer_categories.count(),  # Флаг последней категории
                    'category_name': f"{category.viewers} чел. по {category.price} руб."
                })
        else:
            # Если у услуги нет категорий, создаем одну строку
            services_table.append({
                'num': i,
                'service_name': service.name,
                'service_date': service.date,
                'category': False,
                'viewers': 0,
                'price': 0,
                'total': 0
            })
    
    # Создаем список категорий зрителей для всех услуг (для обратной совместимости)
    viewer_categories = []
    for service in services:
        for category in service.viewer_categories.all():
            viewer_categories.append({
                'service_name': service.name,
                'viewers': category.viewers,
                'price': category.price,
                'total': category.viewers * category.price
            })
    
    # Создаем контекст с данными для рендеринга шаблона
    context = {
        'act_and_account_number': document.act_and_account_number,
        'customer': document.customer,
        'doer': document.doer,
        'services': services,
        'services_text': services_text,
        'service_date': service_date,
        'service': services.first() if services.exists() else None,
        'address_and_time': document.address_and_time,
        'price_in_figures': document.price_in_figures,
        'price_in_words': document.price_in_words,
        'date': document.date,
        'dates': dates,
        'viewer_categories': viewer_categories,
        'number_basis_of_the_contract': document.number_basis_of_the_contract,
        'services_table': services_table,  # Новая структура для таблицы
        'services_table_total': total_sum,  # Общая сумма для итоговой строки
        'services_table_total_viewers': total_viewers  # Общее количество зрителей
    }
    
    # Используем DocxTemplate для рендеринга
    doc = DocxTemplate(template_path)
    doc.render(context)
    
    # Сохраняем во временный буфер
    f = io.BytesIO()
    doc.save(f)
    f.seek(0)
    
    # Отправляем файл пользователю
    response = HttpResponse(f.read())
    response['Content-Disposition'] = f'attachment; filename=Акт_приемки_{document.act_and_account_number}.docx'
    response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    
    return response


def download_invoice(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    
    # Получаем путь к шаблону счета
    template_path = os.path.join(os.path.dirname(__file__), 'document_templates', 'schet.docx')
    
    # Получаем все услуги
    services = document.services.all()
    # Создаем строку с именами услуг через запятую
    services_text = ", ".join([service.name for service in services])
    
    # Создаем строку с датами через запятую
    dates = ", ".join([service.date for service in services])
    
    # Создаем строку, содержащую название услуги и дату
    service_date = ", ".join([f'{service.name} - {service.date}' for service in services])
    
    # Создаем структуру данных для таблицы с услугами и категориями зрителей
    services_table = []
    total_sum = 0
    total_viewers = 0
    
    for i, service in enumerate(services, 1):
        # Если у услуги есть категории зрителей, создаем строки для каждой категории
        if service.viewer_categories.exists():
            for j, category in enumerate(service.viewer_categories.all(), 1):
                category_total = category.viewers * category.price
                total_sum += category_total
                total_viewers += category.viewers
                
                services_table.append({
                    'num': i if j == 1 else '',  # Номер услуги только для первой категории
                    'service_name': service.name if j == 1 else '',  # Название услуги только для первой категории
                    'service_date': service.date if j == 1 else '',  # Дата услуги только для первой категории
                    'category': True,  # Это категория зрителей
                    'viewers': category.viewers,
                    'price': category.price,
                    'total': category_total,
                    'is_first_category': j == 1,  # Флаг первой категории для форматирования
                    'is_last_category': j == service.viewer_categories.count(),  # Флаг последней категории
                    'category_name': f"{category.viewers} чел. по {category.price} руб."
                })
        else:
            # Если у услуги нет категорий, создаем одну строку
            services_table.append({
                'num': i,
                'service_name': service.name,
                'service_date': service.date,
                'category': False,
                'viewers': 0,
                'price': 0,
                'total': 0
            })
    
    # Создаем список категорий зрителей для всех услуг (для обратной совместимости)
    viewer_categories = []
    for service in services:
        for category in service.viewer_categories.all():
            viewer_categories.append({
                'service_name': service.name,
                'viewers': category.viewers,
                'price': category.price,
                'total': category.viewers * category.price
            })
    
    # Создаем контекст с данными для рендеринга шаблона
    context = {
        'act_and_account_number': document.act_and_account_number,
        'customer': document.customer,
        'doer': document.doer,
        'services': services,
        'services_text': services_text,
        'service_date': service_date,
        'service': services.first() if services.exists() else None,  # Для совместимости с шаблоном
        'address_and_time': document.address_and_time,
        'price_in_figures': document.price_in_figures,
        'price_in_words': document.price_in_words,
        'date': document.date,
        'time': document.time,
        'dates': dates,
        'viewer_categories': viewer_categories,
        'services_table': services_table,  # Новая структура для таблицы
        'services_table_total': total_sum,  # Общая сумма для итоговой строки
        'services_table_total_viewers': total_viewers,  # Общее количество зрителей
        'number_basis_of_the_contract': document.number_basis_of_the_contract  # Добавляем номер договора
    }
    
    # Используем DocxTemplate для рендеринга
    doc = DocxTemplate(template_path)
    doc.render(context)
    
    # Сохраняем во временный буфер
    f = io.BytesIO()
    doc.save(f)
    f.seek(0)
    
    # Отправляем файл пользователю
    response = HttpResponse(f.read())
    response['Content-Disposition'] = f'attachment; filename=Счет_{document.act_and_account_number}.docx'
    response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    
    return response


def download_contract(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    
    # Получаем путь к шаблону договора
    template_path = os.path.join(os.path.dirname(__file__), 'document_templates', 'dogovor.docx')
    
    # Получаем все услуги
    services = document.services.all()
    # Создаем строку с именами услуг через запятую
    services_text = ", ".join([service.name for service in services])
    
    # Создаем строку с датами через запятую
    dates = ", ".join([service.date for service in services])
    
    # Создаем строку, содержащую название услуги и дату
    service_date = ", ".join([f'{service.name} - {service.date}' for service in services])
    
    # Создаем структуру данных для таблицы с услугами и категориями зрителей
    services_table = []
    total_sum = 0
    total_viewers = 0
    
    for i, service in enumerate(services, 1):
        # Если у услуги есть категории зрителей, создаем строки для каждой категории
        if service.viewer_categories.exists():
            for j, category in enumerate(service.viewer_categories.all(), 1):
                category_total = category.viewers * category.price
                total_sum += category_total
                total_viewers += category.viewers
                
                services_table.append({
                    'num': i if j == 1 else '',  # Номер услуги только для первой категории
                    'service_name': service.name if j == 1 else '',  # Название услуги только для первой категории
                    'service_date': service.date if j == 1 else '',  # Дата услуги только для первой категории
                    'category': True,  # Это категория зрителей
                    'viewers': category.viewers,
                    'price': category.price,
                    'total': category_total,
                    'is_first_category': j == 1,  # Флаг первой категории для форматирования
                    'is_last_category': j == service.viewer_categories.count(),  # Флаг последней категории
                    'category_name': f"{category.viewers} чел. по {category.price} руб."
                })
        else:
            # Если у услуги нет категорий, создаем одну строку
            services_table.append({
                'num': i,
                'service_name': service.name,
                'service_date': service.date,
                'category': False,
                'viewers': 0,
                'price': 0,
                'total': 0
            })
    
    # Создаем список категорий зрителей для всех услуг (для обратной совместимости)
    viewer_categories = []
    for service in services:
        for category in service.viewer_categories.all():
            viewer_categories.append({
                'service_name': service.name,
                'viewers': category.viewers,
                'price': category.price,
                'total': category.viewers * category.price
            })
    
    # Создаем контекст с данными для рендеринга шаблона
    context = {
        'number_basis_of_the_contract': document.number_basis_of_the_contract,
        'customer': document.customer,
        'doer': document.doer,
        'services': services,
        'services_text': services_text,
        'service_date': service_date,
        'service': services.first() if services.exists() else None,  # Для совместимости с шаблоном
        'address_and_time': document.address_and_time,
        'price_in_figures': document.price_in_figures,
        'price_in_words': document.price_in_words,
        'total_viewers': document.viewers,
        'time': document.time,
        'date': document.date,
        'dates': dates,
        'viewer_categories': viewer_categories,
        'services_table': services_table,  # Новая структура для таблицы
        'services_table_total': total_sum,  # Общая сумма для итоговой строки
        'services_table_total_viewers': total_viewers  # Общее количество зрителей
    }
    
    # Используем DocxTemplate для рендеринга
    doc = DocxTemplate(template_path)
    doc.render(context)
    
    # Сохраняем во временный буфер
    f = io.BytesIO()
    doc.save(f)
    f.seek(0)
    
    # Отправляем файл пользователю
    response = HttpResponse(f.read())
    response['Content-Disposition'] = f'attachment; filename=Договор_{document.number_basis_of_the_contract}.docx'
    response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    
    return response


def download_all_docs(request, document_id):
    """Функция для скачивания всех документов в одном ZIP-архиве"""
    import zipfile
    from io import BytesIO
    
    document = get_object_or_404(Document, id=document_id)
    
    # Создаем ZIP-архив в памяти
    zip_buffer = BytesIO()
    
    # Создаем безопасное имя папки из short_name клиента для использования внутри архива
    try:
        # Получаем короткое имя организации
        short_name = document.customer.short_name
        # Берём первые 10 символов и убираем небезопасные символы
        folder_name = short_name[:20].strip().replace(' ', '_').replace('"', '').replace("'", "").replace('/', '_')
        # Проверяем, что имя не пустое
        if not folder_name:
            folder_name = f"Документы_{document.act_and_account_number}"
    except (AttributeError, TypeError):
        # Если произошла ошибка (например, short_name не существует)
        folder_name = f"Документы_{document.act_and_account_number}"
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Подготавливаем и добавляем акт приемки
        act_buffer = BytesIO()
        act_template_path = os.path.join(os.path.dirname(__file__), 'document_templates', 'act_priemki.docx')
        
        # Получаем все услуги и готовим данные (как в функции download_act)
        services = document.services.all()
        services_text = ", ".join([service.name for service in services])
        dates = ", ".join([service.date for service in services])
        service_date = ", ".join([f'{service.name} - {service.date}' for service in services])
        
        # Создаем структуру данных для таблицы с услугами и категориями зрителей
        services_table = []
        total_sum = 0
        total_viewers = 0
        
        for i, service in enumerate(services, 1):
            if service.viewer_categories.exists():
                for j, category in enumerate(service.viewer_categories.all(), 1):
                    category_total = category.viewers * category.price
                    total_sum += category_total
                    total_viewers += category.viewers
                    
                    services_table.append({
                        'num': i if j == 1 else '',
                        'service_name': service.name if j == 1 else '',
                        'service_date': service.date if j == 1 else '',
                        'category': True,
                        'viewers': category.viewers,
                        'price': category.price,
                        'total': category_total,
                        'is_first_category': j == 1,
                        'is_last_category': j == service.viewer_categories.count(),
                        'category_name': f"{category.viewers} чел. по {category.price} руб."
                    })
            else:
                services_table.append({
                    'num': i,
                    'service_name': service.name,
                    'service_date': service.date,
                    'category': False,
                    'viewers': 0,
                    'price': 0,
                    'total': 0
                })
        
        # Создаем список категорий зрителей (для обратной совместимости)
        viewer_categories = []
        for service in services:
            for category in service.viewer_categories.all():
                viewer_categories.append({
                    'service_name': service.name,
                    'viewers': category.viewers,
                    'price': category.price,
                    'total': category.viewers * category.price
                })
        
        # Создаем контекст для акта
        act_context = {
            'act_and_account_number': document.act_and_account_number,
            'customer': document.customer,
            'doer': document.doer,
            'services': services,
            'services_text': services_text,
            'service_date': service_date,
            'service': services.first() if services.exists() else None,
            'address_and_time': document.address_and_time,
            'price_in_figures': document.price_in_figures,
            'price_in_words': document.price_in_words,
            'date': document.date,
            'dates': dates,
            'viewer_categories': viewer_categories,
            'number_basis_of_the_contract': document.number_basis_of_the_contract,
            'services_table': services_table,
            'services_table_total': total_sum,
            'services_table_total_viewers': total_viewers
        }
        
        # Рендерим акт и добавляем в архив
        act_doc = DocxTemplate(act_template_path)
        act_doc.render(act_context)
        act_doc.save(act_buffer)
        act_buffer.seek(0)
        zip_file.writestr(f'{folder_name}/Акт_приемки_{document.act_and_account_number}.docx', act_buffer.getvalue())
        
        # Подготавливаем и добавляем счет
        invoice_buffer = BytesIO()
        invoice_template_path = os.path.join(os.path.dirname(__file__), 'document_templates', 'schet.docx')
        
        # Контекст для счета
        invoice_context = {
            'act_and_account_number': document.act_and_account_number,
            'customer': document.customer,
            'doer': document.doer,
            'services': services,
            'services_text': services_text,
            'service_date': service_date,
            'service': services.first() if services.exists() else None,
            'address_and_time': document.address_and_time,
            'price_in_figures': document.price_in_figures,
            'price_in_words': document.price_in_words,
            'date': document.date,
            'time': document.time,
            'dates': dates,
            'viewer_categories': viewer_categories,
            'services_table': services_table,
            'services_table_total': total_sum,
            'services_table_total_viewers': total_viewers,
            'number_basis_of_the_contract': document.number_basis_of_the_contract
        }
        
        # Рендерим счет и добавляем в архив
        invoice_doc = DocxTemplate(invoice_template_path)
        invoice_doc.render(invoice_context)
        invoice_doc.save(invoice_buffer)
        invoice_buffer.seek(0)
        zip_file.writestr(f'{folder_name}/Счет_{document.act_and_account_number}.docx', invoice_buffer.getvalue())
        
        # Подготавливаем и добавляем договор
        contract_buffer = BytesIO()
        contract_template_path = os.path.join(os.path.dirname(__file__), 'document_templates', 'dogovor.docx')
        
        # Контекст для договора
        contract_context = {
            'number_basis_of_the_contract': document.number_basis_of_the_contract,
            'customer': document.customer,
            'doer': document.doer,
            'services': services,
            'services_text': services_text,
            'service_date': service_date,
            'service': services.first() if services.exists() else None,
            'address_and_time': document.address_and_time,
            'price_in_figures': document.price_in_figures,
            'price_in_words': document.price_in_words,
            'total_viewers': document.viewers,
            'time': document.time,
            'date': document.date,
            'dates': dates,
            'viewer_categories': viewer_categories,
            'services_table': services_table,
            'services_table_total': total_sum,
            'services_table_total_viewers': total_viewers
        }
        
        # Рендерим договор и добавляем в архив
        contract_doc = DocxTemplate(contract_template_path)
        contract_doc.render(contract_context)
        contract_doc.save(contract_buffer)
        contract_buffer.seek(0)
        zip_file.writestr(f'{folder_name}/Договор_{document.number_basis_of_the_contract}.docx', contract_buffer.getvalue())
    
    # Готовим ZIP-архив для отправки
    zip_buffer.seek(0)
    
    # Создаем безопасное имя файла для zip-архива (аналогично имени папки внутри)
    safe_name = folder_name
    
    # Отправляем архив пользователю
    response = HttpResponse(zip_buffer.getvalue())
    response['Content-Type'] = 'application/zip'
    response['Content-Disposition'] = f'attachment; filename="{safe_name}.zip"'
    
    return response