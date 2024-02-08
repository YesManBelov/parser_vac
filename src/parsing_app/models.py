import json

from django.db import models

from parsing_app.utils import from_cyrillic_to_eng


def defaults_urls():
    return {"head_hunter": '', 'superjob': ''}


# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name="Название населенного пункта",
                            unique=True)
    slug = models.CharField(max_length=50,
                            blank=True,
                            unique=True)  # blank - можно не заполнять

    class Meta:
        verbose_name = "Название населенного пункта"
        verbose_name_plural = "Названия населенных пунктов"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        else:
            self.slug = self.slug.lower()
        super().save(*args, **kwargs)


class Language(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name="Язык программирования",
                            unique=True)
    slug = models.CharField(max_length=50,
                            blank=True,
                            unique=True)  # blank - можно не заполнять

    class Meta:
        verbose_name = "Язык программирования"
        verbose_name_plural = "Языки программирования"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        else:
            self.slug = self.slug.lower()
        super().save(*args, **kwargs)


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Заголовок вакансии')
    company = models.CharField(max_length=250, verbose_name='Компания')
    description = models.TextField(verbose_name='Описание вакансии')
    city = models.ForeignKey('City', on_delete=models.CASCADE,
                             verbose_name='Город', related_name='vacancies')
    language = models.ForeignKey('Language', on_delete=models.CASCADE,
                                 verbose_name='Язык программирования')
    timestamp = models.DateField(auto_now_add=True)  # автодата

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-timestamp']

    def __str__(self):
        return self.title


class Error(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    url = models.URLField(null=True, editable=False)
    error = models.CharField(max_length=100,
                             blank=True,
                             editable=False)

    def __str__(self):
        return f"{str(self.timestamp)} | {str(self.error)}"


class Url(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE,
                             verbose_name='Город')
    language = models.ForeignKey('Language', on_delete=models.CASCADE,
                                 verbose_name='Язык программирования')
    url_data = models.JSONField(default=defaults_urls)
    
    class Meta:
        unique_together = ('city', 'language')
