import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from recipes.models import (
    Recipe,
    ShoppingList,
    FollowRecipe,
    FollowUser,
    Ingredient
)


@require_http_methods(["POST"])
def add_recipe_shopping_list(request):
    if request.user.is_anonymous:
        return JsonResponse({'success': False}, status=400)

    json_data = json.loads(request.body)
    recipe = get_object_or_404(Recipe, pk=json_data.get('id'))
    shopping_obj, created = ShoppingList.objects.get_or_create(
        recipe=recipe, user=request.user)
    if created:
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


@require_http_methods(["DELETE"])
def remove_recipe_shopping_list(request, recipe_id):
    num, deleted = get_object_or_404(
        ShoppingList, recipe_id=recipe_id, user=request.user).delete()
    if num != 0:
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


@require_http_methods(["POST"])
def following(request):
    if request.user.is_anonymous:
        return JsonResponse({'success': False}, status=400)

    json_data = json.loads(request.body)
    subscriptions_obj, created = FollowUser.objects.get_or_create(
        author_id=json_data.get('id'), user_id=request.user.id)
    if created:
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


@require_http_methods(["DELETE"])
def unfollowing(request, author_id):
    num, deleted = get_object_or_404(
        FollowUser,
        author_id=author_id, user_id=request.user.id).delete()
    if num != 0:
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


@require_http_methods(["POST"])
def add_favorite_recipe(request):
    json_data = json.loads(request.body)
    favorites_obj, created = FollowRecipe.objects.get_or_create(
        recipe_id=json_data.get('id'),
        user_id=request.user.id)
    if created:
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


@require_http_methods(["DELETE"])
def remove_favorite_recipe(request, recipe_id):
    num, deleted = get_object_or_404(FollowRecipe, recipe_id=recipe_id,
                                     user_id=request.user.id).delete()
    if num != 0:
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


@require_http_methods(["GET"])
def parse_ingredients(request):
    query = request.GET.get('query', [])
    ingredients_query = Ingredient.objects.filter(
        title__istartswith=query
    ).values('title', 'dimension')

    response = list(ingredients_query)
    return JsonResponse(response, safe=False)
