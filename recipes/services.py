import json

from django.shortcuts import get_object_or_404

from .models import IngredientRecipe, FollowRecipe, Ingredient, Recipe, ShoppingList


def get_ingredients(request):
    ingredients = {}
    for key in request.POST:

        if key.startswith('nameIngredient'):
            value_ingredient = key[15:]
            ingredients[request.POST[key]] = request.POST[
                'valueIngredient_' + value_ingredient
            ]
    return ingredients


def get_ingredients_names(request):
    ingredients = get_ingredients(request)
    return list(ingredients.keys())


def get_ingredients_values(request):
    ingredients = get_ingredients(request)
    return list(ingredients.values())


def get_id_recipe(request):
    """Функция получает id рецепта из тела запроса."""
    body = json.loads(request.body)
    return body.get('id')


def get_fav_list(request):
    fav_list = []
    if request.user.is_authenticated:
        fav_list = FollowRecipe.objects.select_related('recipe').filter(
            user=request.user).values_list('recipe__id', flat=True)

    return fav_list


def get_shopping_list(request):
    if request.user.is_authenticated:
        buying_list = ShoppingList.objects.select_related('recipe').filter(
            user=request.user).values_list('recipe__id', flat=True)

    return buying_list


def create_buy(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = request.user
    obj, created = ShoppingList.objects.get_or_create(
        defaults={
            'user': user,
            'recipe': recipe,
        },
        user=user,
        recipe=recipe,
    )

    return {'success': bool(created)}


def assembly_ingredients(ingredients_names, ingredients_values, recipe, ingredients):
    """Удаление ингредиентов из поста и установка новых, полученных с request."""
    ingredients_list = []
    if len(ingredients_names):
        ingredients.delete()
        for n, name in enumerate(ingredients_names):
            try:
                ingredient = Ingredient.objects.get(title=name)
            except Ingredient.DoesNotExist:
                return []
            ingr_quan, created = IngredientRecipe.objects.get_or_create(
                defaults={
                    'ingredient': ingredient,
                    'amount': ingredients_values[n],
                    'recipe': recipe,
                },
                ingredient=ingredient,
                amount=ingredients_values[n],
                recipe=recipe,
            )
            ingr_quan.save()
            ingredients_list.append(ingr_quan)

    return ingredients_list

def create_shopping_list(request):
    recipes = Recipe.objects.filter(
        recipe_shopping_list__user=request.user
    ).all()
    ingredients = []
    for recipe in recipes:
        ingredient_list = IngredientRecipe.objects.filter(recipe=recipe)
        for i in ingredient_list:
            new = [i.ingredient.title, i.amount, i.ingredient.dimension]
            ingredients.append(new)
    result = {}
    for i in ingredients:
        if not i[0] in result:
            result[i[0]] = i[1]
        else:
            result[i[0]] += i[1]

    content = []
    for key, value in result.items():
        for i in ingredients:
            if i[0] == key:
                ing = f'{key} - {value} {i[2]}\n'
                content.append(ing)
                break

    return content