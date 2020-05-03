from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app import models

admin.site.register(models.Nurse, UserAdmin)
admin.site.register(models.Ward)
admin.site.register(models.Disease)
admin.site.register(models.Article)
admin.site.register(models.Tag)
admin.site.register(models.Event)
admin.site.register(models.Read)
admin.site.register(models.Like)
