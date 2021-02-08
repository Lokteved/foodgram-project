from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator


User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=200, verbose_name='Ингредиент')
    dimension = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )

    def __str__(self):
        return f'{self.title}, {self.dimension}'


class Tag(models.Model):
    name = models.CharField(max_length=10)
    slug = models.SlugField(
        unique=True,
        max_length=100,
        blank=True,
        null=True
    )
    color = models.CharField(
        verbose_name='check box style',
        max_length=50,
        null=True
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes')
    title = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='recipes/',
        blank=True,
        null=True)
    description = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        through_fields=('recipe', 'ingredient')
    )
    tag = models.ManyToManyField(Tag, related_name='recipe_tag')
    cooking_time = models.IntegerField()
    pub_date = models.DateTimeField(
        'date published',
        auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients')
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipes')
    amount = models.IntegerField(
        validators=(
            MinValueValidator(1, message='Значение должно быть больше 1'),
        )
    )


class FollowRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower_recipe')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='following_recipe')

    class Meta:
        unique_together = [['user', 'recipe']]

    def __str__(self):
        return f'follower - {self.user} following recipe - {self.recipe}'


class FollowUser(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following')

    class Meta:
        unique_together = [['user', 'author']]

    def __str__(self):
        return f'follower - {self.user} following - {self.author}'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_shopping_list')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_shopping_list')

    class Meta:
        unique_together = [['user', 'recipe']]
