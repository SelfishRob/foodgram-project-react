from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7, null=True)
    slug = models.SlugField(max_length=200, unique=True, null=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return f'{self.name} ({self.measurement_unit})'
