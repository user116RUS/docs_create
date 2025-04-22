from django.db import models

class Organisation(models.Model):
    name = models.TextField(
        max_length=1000,
        verbose_name="Название организации полностью",
        help_text=(
            'Муниципальное бюджетное общеобразовательное учреждение «Гимназия №54», в лице директора Исаева Рамиля Робертовича'
            'Индивидуальный предприниматель Мотыгуллин Айрат Маратович, действующего на основании ОГРНИП №323169000037033/'
        )
    )
    requisites = models.TextField(
        max_length=10000,
        verbose_name="Реквизиты (Карта партенра)",
        help_text=(
            'ООО «Алгарыш»'
            '423822, Республика Татарстан, г. Набережные Челны, проспект Чулман, д. 8, пом. 4'
            'ИНН 1650343159 ...'
        ),
    )
    fio = models.TextField(
        max_length=100,
        verbose_name="ФИО руководителя",
        help_text="А.М. Мотыгуллин, И.Ф. Шайхутдинов",
    )
    function = models.CharField(
        max_length=100,
        verbose_name='Должность',
        choices=[
            ('Директор', 'Директор'),
            ('Индивидуальный предприниматель', 'ИП'),
        ],
    )
    inn = models.CharField(
        max_length=100,
        verbose_name="ИНН",
        help_text="165204115017",

    )
    bik = models.CharField(
        max_length=100,
        verbose_name="БИК",
        help_text="044525104",

    )
    bank_name = models.TextField(
        max_length=100,
        verbose_name="Имя банка",
        help_text="ООО «Банк Точка»",

    )
    short_name = models.TextField(
        max_length=100,
        verbose_name="Короткое имя",
        help_text="ИП Мотыгуллин Айрат Маратович",

    )
    correspondent_bank_account = models.CharField(
        max_length=100,
        verbose_name="кор. счет",
        help_text="30101810745374525104",

    )
    bank_account = models.CharField(
        max_length=100,
        verbose_name="Р/С",
        help_text="40802810101500493834",
    )
    kpp = models.CharField(
        max_length=100,
        verbose_name="КПП",
        help_text="165001001",
    )
    address = models.TextField(
        max_length=200,
        verbose_name="Адрес",
        help_text="423822, Республика Татарстан, г. Набережные Челны, проспект Чулман, д. 8, пом. 4",
    )
    is_our = models.BooleanField(
        default=False,
        verbose_name="Наша организация?",
    )
    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.TextField(
        max_length=200,
        verbose_name='Название услуги',
        help_text='Проведение культурно-массового мероприятия: "Соревнования роботов"'
    )
    date = models.CharField(
        max_length=15,
        verbose_name='Срок оказания услуг',
        help_text='28.05.2025 г.',
    )
    
    def __str__(self):
        return self.name
    
    @property
    def total_viewers(self):
        return sum(category.viewers for category in self.viewer_categories.all())
    
    @property
    def total_price(self):
        return sum(category.viewers * category.price for category in self.viewer_categories.all())


class ViewerCategory(models.Model):
    service = models.ForeignKey(
        Service, 
        on_delete=models.CASCADE,
        related_name='viewer_categories',
        verbose_name='Услуга'
    )
    viewers = models.IntegerField(
        verbose_name='Кол-во зрителей',
        help_text='100'
    )
    price = models.FloatField(
        verbose_name='Цена за единицу',
        help_text='200.5'
    )
    
    def __str__(self):
        return f"{self.service.name}: {self.viewers} чел. по {self.price} руб."
    
    class Meta:
        verbose_name = 'Категория зрителей'
        verbose_name_plural = 'Категории зрителей'


class Document(models.Model):
    address_and_time = models.CharField(
        max_length=150,
        verbose_name='адрес и время проведения',
        help_text='(<i>г. Набережные Челны, ул. Шамиля Усманова, д.19. Время проведения: с 09:30</i>)',
    )
    date = models.CharField(
        max_length=100,
        verbose_name='дата',
        help_text='(<i>15 июня 2023</i>)'
    )
    price_in_figures = models.CharField(
        max_length=100,
        verbose_name='цена(цифрами)',
        help_text='(<i>17 000</i>)'
    )
    price_in_words = models.CharField(
        max_length=100,
        verbose_name="цена(словами)",
        help_text='(<i>семнадцать тысяч рублей 00 копеек</i>)',
    )
    time = models.CharField(
        max_length=100,
        verbose_name='время проведения',
        help_text='(<i>09:30-10:30</i>)',
    )
    act_and_account_number = models.CharField(
        max_length=100,
        verbose_name='номер акта',
        help_text='(<i>50/1</i>)',
    )
    number_basis_of_the_contract = models.CharField(
        max_length=100,
        verbose_name='номер основание договора',
        help_text='(<i>Nº 50/23-11 от 18.05.2023 г.</i>)'
    )
    doer = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        verbose_name='Исполнитель (мы)',
        related_name='documents_as_doer',
        limit_choices_to={'is_our': True},
    )
    customer = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        verbose_name='Заказчик (не мы)',
        related_name='documents_as_customer',
        limit_choices_to={'is_our': False},
    )
    services = models.ManyToManyField(
        Service,
        related_name='document',
        verbose_name='Услуги',
    )
    viewers = models.CharField(
        max_length=50,
        verbose_name='Кол-во зрителей ',
        help_text='180 (Сто восемьдесят)',
        blank=False,
        null=False,
    )
