from django.contrib import admin

from .models import (
    Ingredient,
    IngredientRecipe,
    Tag,
    Recipe,
    FollowRecipe,
    FollowUser,
    ShoppingList
)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'dimension')


class IngredientRecipeInline(admin.StackedInline):
    model = IngredientRecipe


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'title', 'cooking_time')
    list_filter = ('author', 'title', 'tag')
    inlines = (IngredientRecipeInline,)


class FollowUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')


class FollowRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')


admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(FollowUser, FollowUserAdmin)
admin.site.register(FollowRecipe, FollowRecipeAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
