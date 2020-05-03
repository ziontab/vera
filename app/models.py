from django.db import models
from django.contrib.auth.models import AbstractUser


class Tag(models.Model):
    title = models.CharField(max_length=256, verbose_name='Полное название', unique=True)
    slug = models.CharField(max_length=256, verbose_name='Название', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Disease(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название', unique=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Заболевание'
        verbose_name_plural = 'Заболевания'


class Nurse(AbstractUser):
    PROFESSIONAL = 'P'
    RELATIVE = 'R'
    ROLES = (
        (PROFESSIONAL, 'Профессиональная сиделка'),
        (RELATIVE, 'Родственник'),
    )
    first_name = models.CharField(max_length=256, verbose_name='Имя')
    last_name = models.CharField(max_length=256, verbose_name='Фамилия')
    role = models.CharField(max_length=1, choices=ROLES, verbose_name='Роль')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Сиделка'
        verbose_name_plural = 'Сиделки'


class Ward(models.Model):
    SEX_MALE = 'M'
    SEX_FEMALE = 'F'
    SEX_OTHER = 'F'
    SEXES = (
        (SEX_MALE, 'Мужской'),
        (SEX_FEMALE, 'Женский'),
        (SEX_OTHER, 'Другой'),
    )

    STATUS_INDEPENDENT = 'I'
    STATUS_WEEKLY = 'W'
    STATUS_DAILY = 'D'
    STATUS_FULL = 'F'
    STATUSES = (
        (STATUS_INDEPENDENT, 'Не нуждается в помощи'),
        (STATUS_WEEKLY, 'Нуждается в помощи несколько раз в неделю'),
        (STATUS_DAILY, 'Нуждается в помощи несколько раз в день'),
        (STATUS_FULL, 'Нуждается в постоянной помощи'),
    )

    first_name = models.CharField(max_length=256, verbose_name='Имя')
    last_name = models.CharField(max_length=256, verbose_name='Фамилия')
    sex = models.CharField(max_length=1, choices=SEXES, verbose_name='Пол')
    status = models.CharField(max_length=1, choices=STATUSES, verbose_name='Статус', default=STATUS_INDEPENDENT)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    disease = models.ManyToManyField(Disease)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Подопечный'
        verbose_name_plural = 'Подопечные'


class Article(models.Model):
    TYPE_TEXT = 'T'
    TYPE_INSTRUCTION = 'I'
    TYPE_AD = 'A'
    TYPES = (
        (TYPE_TEXT, 'Текст'),
        (TYPE_INSTRUCTION, 'Инструкция'),
        (TYPE_AD, 'Реклама'),
    )

    title = models.CharField(max_length=256, verbose_name='Заголовок', unique=True)
    text = models.TextField(verbose_name='Текст', null=True, blank=True)
    type = models.CharField(max_length=1, choices=TYPES, verbose_name='Тип', default=TYPES)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Like(models.Model):
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return self.article

    class Meta:
        unique_together = (
            ('nurse', 'article'),
        )
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class Read(models.Model):
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return self.article

    class Meta:
        unique_together = (
            ('nurse', 'article'),
        )
        verbose_name = 'Прочитанное'
        verbose_name_plural = 'Прочитанное'


class Event(models.Model):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст', null=True, blank=True)
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    date_planned = models.DateTimeField(verbose_name='Дата запланированная', null=True, blank=True)
    date_close = models.DateTimeField(verbose_name='Дата закрытия', null=True, blank=True)
    is_complete = models.BooleanField(verbose_name='Завершено', blank=True, default=False)

    def __str__(self):
        return self.title

    class Meta:
        index_together = (
            ('nurse', 'date_planned'),
        )
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
