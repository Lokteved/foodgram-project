from django.urls import path

from api import views

urlpatterns = [
    path('purchases', views.add_recipe_shopping_list),
    path('purchases/<int:recipe_id>', views.remove_recipe_shopping_list),

    path('subscriptions', views.following),
    path('subscriptions/<int:author_id>', views.unfollowing),

    path('favorites', views.add_favorite_recipe),
    path('favorites/<int:recipe_id>', views.remove_favorite_recipe),

    path('ingredients/', views.parse_ingredients),
]