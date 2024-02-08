from django.contrib import admin
from .models import City, Language, Vacancy, Error, Url

class MyModelAdminError(admin.ModelAdmin):
    readonly_fields = ('url', 'error')


# Register your models here.
admin.site.register(City)
admin.site.register(Language)
admin.site.register(Vacancy)
admin.site.register(Error, MyModelAdminError)
admin.site.register(Url)
