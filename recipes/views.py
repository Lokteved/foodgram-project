from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.views import View

from .forms import RecipeForm
from .models import Recipe, IngredientRecipe, Ingredient, ShoppingList
from .services import (
    get_ingredients,
    get_ingredients_names,
    get_ingredients_values,
    assembly_ingredients,
    get_fav_list,
    get_shopping_list,
    get_follows_list,
    create_shopping_list
)


User = get_user_model()


def index(request):
    tags_values = request.GET.getlist('filters')
    recipe_list = Recipe.objects.all()
    favorites = False
    shopping_list = False
    if request.user.is_authenticated:
        favorites = get_fav_list(request)
        shopping_list = get_shopping_list(request)
    if tags_values:
        recipe_list = recipe_list.filter(
            tag__name__in=tags_values).distinct().all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, 'index.html',
        {
            'page': page,
            'paginator': paginator,
            'favorites': favorites,
            'shopping_list': shopping_list
        }
    )


@login_required
def new_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, files=request.FILES or None)
        ingredients = get_ingredients(request)
        if not bool(ingredients):
            form.add_error(None, 'Добавьте ингредиенты')

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            for item in ingredients:
                IngredientRecipe.objects.create(
                    amount=ingredients[item],
                    ingredient=Ingredient.objects.get(title=f'{item}'),
                    recipe=recipe)
            form.save_m2m()
            return redirect('index')

    else:
        form = RecipeForm(request.POST, files=request.FILES or None)

    return render(request, 'recipe_form.html', {'form': form})


class RecipeEdit(LoginRequiredMixin, View):
    def get(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if request.user != recipe.author:
            return redirect('recipe', recipe_id=recipe.id)

        form = RecipeForm(instance=recipe)
        return render(
            request,
            'recipe_form.html',
            context={'form': form, 'recipe': recipe}
        )

    def post(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if request.user != recipe.author:
            return redirect('recipe', recipe_id=recipe.id)

        ingredients = recipe.recipe_ingredients.all()
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        ingredients_names = get_ingredients_names(request)
        ingredients_values = get_ingredients_values(request)
        if form.is_valid():
            assembly_ingredients(
                ingredients_names, ingredients_values, recipe, ingredients)
            form.save()
        else:
            return render(
                request,
                'recipe_form.html',
                context={'form': form, 'recipe': recipe}
            )

        return redirect('recipe', recipe_id=recipe.id)


class RecipeDelete(LoginRequiredMixin, View):
    def get(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if request.user != recipe.author:
            return redirect('recipe', id=recipe.id)

        recipe.delete()
        return redirect('index')


@login_required
def favorite_index(request):
    tags_values = request.GET.getlist('filters')
    recipe_list = Recipe.objects.filter(
        following_recipe__user=request.user
    ).all()
    if tags_values:
        recipe_list = recipe_list.filter(
            tag__name__in=tags_values).distinct().all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    favorites = get_fav_list(request)
    shopping_list = get_shopping_list(request)

    return render(request, 'favorite_index.html', {
            'page': page,
            'paginator': paginator,
            'favorites': favorites,
            'shopping_list': shopping_list
        }
    )


@login_required
def follows_index(request):
    followed_authors = User.objects.filter(following__user=request.user)
    follows_list = get_follows_list(request)
    paginator = Paginator(followed_authors, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow_index.html', context={
            'page': page,
            'paginator': paginator,
            'follows_list': follows_list
        }
    )


@login_required
def shopping_list(request):
    purchases = Recipe.objects.filter(
        recipe_shopping_list__user=request.user
    ).all()
    return render(
        request,
        'shopping_list.html',
        context={'purchases': purchases}
    )


@login_required
def shopping_list_delete_item(request, recipe_id):
    purchase = get_object_or_404(
        ShoppingList,
        user=request.user,
        recipe=recipe_id
    )
    purchase.delete()
    purchases = Recipe.objects.filter(
        recipe_shopping_list__user=request.user
    ).all()
    return render(
        request,
        'shopping_list.html',
        context={'purchases': purchases}
    )


@login_required
def download_shopping_list(request):
    result = create_shopping_list(request)
    filename = 'ShopList.txt'
    response = HttpResponse(result, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(
        filename)
    return response


def profile(request, username):
    tags_values = request.GET.getlist('filters')
    author = get_object_or_404(User, username=username)
    recipe_list = author.recipes.all()
    favorites = False
    shopping_list = False
    if request.user.is_authenticated:
        favorites = get_fav_list(request)
        shopping_list = get_shopping_list(request)
    if tags_values:
        recipe_list = recipe_list.filter(
            tag__name__in=tags_values).distinct().all()
    paginator = Paginator(recipe_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    following = False
    if request.user.is_authenticated:
        if request.user.follower.filter(author=author).exists():
            following = True
    return render(
        request, 'profile.html',
        {
            'author': author,
            'page': page,
            'paginator': paginator,
            'following': following,
            'favorites': favorites,
            'shopping_list': shopping_list
        }
    )


def recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe_ingredients = IngredientRecipe.objects.filter(recipe=recipe)
    following = False
    favorite = False
    in_list = False
    if request.user.is_authenticated:
        following = request.user.follower.filter(author=recipe.author).exists()
        favorite = request.user.follower_recipe.filter(recipe=recipe).exists()
        in_list = request.user.user_shopping_list.filter(recipe=recipe).exists()
    return render(
        request, 'recipe.html',
        {
            'recipe': recipe,
            'recipe_ingredients': recipe_ingredients,
            'author': recipe.author,
            'following': following,
            'favorite': favorite,
            'in_list': in_list
        }
    )
