import json

from django.db.models import Sum

from .models import (
    IngredientRecipe,
    FollowRecipe,
    Ingredient,
    Recipe,
    ShoppingList,
    FollowUser
)


def get_ingredients(request):
    """Получение списка ингредиентов из запроса"""
    ingredients = {}
    for key in request.POST:

        if key.startswith('nameIngredient'):
            value_ingredient = key[15:]
            ingredients[request.POST[key]] = request.POST[
                'valueIngredient_' + value_ingredient
            ]
    return ingredients


def get_ingredients_names(request):
    """Получение списка названий ингредиентов из запроса"""
    ingredients = get_ingredients(request)
    return list(ingredients.keys())


def get_ingredients_values(request):
    """Получение списка количеств ингредиентов из запроса"""
    ingredients = get_ingredients(request)
    return list(ingredients.values())


def get_id_recipe(request):
    """Функция получает id рецепта из тела запроса."""
    body = json.loads(request.body)
    return body.get('id')


def get_fav_list(request):
    """Получение списка id избранных рецептов"""
    fav_list = []
    if request.user.is_authenticated:
        fav_list = FollowRecipe.objects.select_related('recipe').filter(
            user=request.user).values_list('recipe__id', flat=True)

    return fav_list


def get_follows_list(request):
    """Получение списка id избранных авторов"""
    follows_list = []
    if request.user.is_authenticated:
        follows_list = FollowUser.objects.select_related('author').filter(
            user=request.user).values_list('author__id', flat=True)

    return follows_list


def get_shopping_list(request):
    """Получение списка id рецептов, добавленных в список покупок"""
    buying_list = []
    if request.user.is_authenticated:
        buying_list = ShoppingList.objects.select_related('recipe').filter(
            user=request.user).values_list('recipe__id', flat=True)

    return buying_list


def assembly_ingredients(ingr_names, ingr_values, recipe, ingredients):
    """Удаление ингредиентов из поста и установка новых, полученных с request."""
    ingredients_list = []
    if not ingr_names:
        return ingredients_list

    ingredients.delete()
    for n, name in enumerate(ingr_names):
        try:
            ingredient = Ingredient.objects.get(title=name)
        except Ingredient.DoesNotExist:
            continue
        ingr_quan, created = IngredientRecipe.objects.get_or_create(
            defaults={
                'ingredient': ingredient,
                'amount': ingr_values[n],
                'recipe': recipe,
            },
            ingredient=ingredient,
            amount=ingr_values[n],
            recipe=recipe,
        )
        ingr_quan.save()
        ingredients_list.append(ingr_quan)

    return ingredients_list


def create_shopping_list(request):
    """Создание списка покупок для скачивания"""
    recipes = Recipe.objects.filter(
        recipe_shopping_list__user=request.user
    ).all()
    result = []
    ingredient_list = recipes.values(
        'ingredients__title', 'ingredients__dimension',
    ).annotate(
        Sum('recipe_ingredients__amount')).order_by()
    for i in ingredient_list:
        item = (
            i.get('ingredients__title'),
            str(i.get('recipe_ingredients__amount__sum')),
            i.get('ingredients__dimension')
        )
        result += (' '.join(item)) + '\n'
    return result