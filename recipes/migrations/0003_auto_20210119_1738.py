# Generated by Django 2.2 on 2021-01-19 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_followrecipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_recipe', to='recipes.Recipe'),
        ),
    ]