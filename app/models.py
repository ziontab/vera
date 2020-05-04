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

    STATUS_WALKING = 'W'
    STATUS_SITING = 'S'
    STATUS_BED = 'B'
    STATUSES = (
        (STATUS_WALKING, 'Ходячий'),
        (STATUS_SITING, 'Сидящий'),
        (STATUS_BED, 'Лежащий'),
    )

    first_name = models.CharField(max_length=256, verbose_name='Имя')
    middle_name = models.CharField(max_length=256, verbose_name='Отчество')
    last_name = models.CharField(max_length=256, verbose_name='Фамилия')
    birthday = models.DateField(verbose_name='Дата рождения')
    sex = models.CharField(max_length=1, choices=SEXES, verbose_name='Пол')
    address = models.CharField(max_length=1024, verbose_name='Адрес')
    phone = models.CharField(max_length=1024, verbose_name='Телефон')
    status = models.CharField(max_length=1, choices=STATUSES, verbose_name='Статус', default=STATUS_WALKING)
    doctor_description = models.TextField(verbose_name='Лечащий врач', blank=True)
    complaints = models.TextField(verbose_name='Основные жалобы', blank=True)
    recommendations = models.TextField(verbose_name='Персональные рекомендации', blank=True)
    description = models.TextField(verbose_name='Дополнительная информация', blank=True)
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE, verbose_name='Сиделка')
    disease = models.ManyToManyField(Disease, verbose_name='Заболевания')

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Подопечный'
        verbose_name_plural = 'Подопечные'


class ArticleManager(models.Manager):
    def recommend(self, nurse):
        return self.all()

    def read(self, nurse):
        read_ids = Read.objects.filter(nurse=nurse).values_list('id', flat=True)
        return self.filter(pk__in=read_ids).order_by("-id")

    def liked(self, nurse):
        liked_ids = Like.objects.filter(nurse=nurse).values_list('id', flat=True)
        return self.filter(pk__in=liked_ids).order_by("-id")

    def by_tag(self, tag):
        tag = Tag.objects.filter(slug=tag).first()
        if tag:
            return tag.article_set.all().order_by("id")
        return self.none()


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

    objects = ArticleManager()

    def __str__(self):
        return self.title

    def add_read(self, nurse):
        Read.objects.get_or_create(nurse=nurse, article=self)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Like(models.Model):
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return self.article.title

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
        return self.article.title

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
