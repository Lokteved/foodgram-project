from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipes/new/', views.new_recipe, name='new_recipe'),
    path('favorite/', views.favorite_index, name='favorite_index'),
    path('follows/', views.follows_index, name='follows_index'),
    path('shopping_list/', views.shopping_list, name="shopping_list"),
    path(
        'shopping_list/<int:recipe_id>/',
        views.shopping_list_delete_item,
        name="shopping_list_delete_item"
    ),
    path(
        'shopping_list/download/',
        views.download_shopping_list,
        name="download_shopping_list"
    ),
    path('<str:username>/', views.profile, name='profile'),
    path('recipes/<int:recipe_id>/', views.recipe_view, name='recipe'),
    path(
        'recipes/<int:recipe_id>/edit/',
        views.RecipeEdit.as_view(),
        name='recipe_edit'
    ),
    path(
        'recipes/<int:recipe_id>/delete/',
        views.RecipeDelete.as_view(),
        name='recipe_delete'
    ),
]