from django import forms
from django.forms.widgets import CheckboxSelectMultiple

from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'description', 'cooking_time', 'tag', 'image')
        widgets = {
            "tag": CheckboxSelectMultiple(),
        }
