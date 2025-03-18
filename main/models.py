from django.db import models

class Organisation(models.Model):
    name = models.TextField(
        max_length=100,
        verbose_name="Название организации",
        help_text='Индивидуальный предприниматель Мотыгуллин Айрат Маратович',
    )
    requisites = models.TextField(
        max_length=10000,
        verbose_name="Реквизиты",
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
    address = models.CharField(
        max_length=200,
        verbose_name="Адрес",
        help_text="423822, Республика Татарстан, г. Набережные Челны, проспект Чулман, д. 8, пом. 4",
    )


