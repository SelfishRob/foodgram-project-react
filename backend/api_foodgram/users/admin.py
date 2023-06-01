from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from recipes.models import (Favorite, Follow, Ingredient, Recipe,
                            RecipeIngredient, ShoppingCart, Tag)
from users.models import CustomUser


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    min_num = 1


class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name')
    search_fields = ('email', 'username', 'first_name', 'last_name')


admin.site.register(CustomUser, CustomUserAdmin)


class RecipeAdmin(ModelAdmin):
    list_display = ['id', 'name', 'author', 'favorites_count']
    search_fields = ['name', 'author__username']
    list_filter = ['tags']
    inlines = (RecipeIngredientInline, )

    def favorites_count(self, obj):
        if obj.favorites.exists():
            return obj.favorites.count()
        return 0


admin.site.register(Recipe, RecipeAdmin)


class IngredientAdmin(ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


admin.site.register(Ingredient, IngredientAdmin)


# Регистрация остальных моделей
admin.site.register(Favorite)
admin.site.register(Follow)
admin.site.register(RecipeIngredient)
admin.site.register(ShoppingCart)
admin.site.register(Tag)
