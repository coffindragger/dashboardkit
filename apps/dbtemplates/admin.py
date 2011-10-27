from django.contrib import admin
from django import forms
from django.db import models

from dbtemplates.models import DatabaseTemplate


class DatabaseTemplateAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows':40,'cols':100})},
    }
admin.site.register(DatabaseTemplate, DatabaseTemplateAdmin)
